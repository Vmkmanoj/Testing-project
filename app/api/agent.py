from PIL import ImageColor
from PIL import ImageColor
from fastapi import File
from fastapi import UploadFile
from app.database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from langchain_core.vectorstores import VectorStore
from pypdf import PdfReader
from fastapi import APIRouter, Depends
from app.agent.graph import sql_agent_graph
from app.schema.chat import ChatRequest, ChatResponse
from app.models.user_model import User
from app.common.deps import get_authenticated_user
from fastapi.responses import StreamingResponse
from sqlalchemy import select, delete
from app.agent.state import AgentState
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter

from sentence_transformers import SentenceTransformer
from app.models.company_policy_model import CompanyPolicy
from app.models.company_policy_chunk_model import CompanyPolicyChunk


splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


router = APIRouter(prefix="/agent", tags=["AI Agent"])


async def async_generator(agent, state, config):
    try:
        async for event in agent.astream_events(state, config, version="v2"):
            kind = event["event"]
            if kind == "on_chat_model_stream":
                node_name = event.get("metadata", {}).get("langgraph_node")
                if node_name == "generate_sql":
                    continue

                chunk = event["data"]["chunk"]
                if chunk.content:
                    data_str = json.dumps({"token": chunk.content})
                    yield f"data: {data_str}\n\n"
            elif kind == "on_chain_end" and event["name"] == "LangGraph":
                final_state = event["data"].get("output")
                if final_state:
                    data_str = json.dumps({"final_state": final_state}, default=str)
                    yield f"data: {data_str}\n\n"
    except Exception as e:
        import traceback

        traceback.print_exc()
        yield f'data: {{"error": "{str(e)}"}}\n\n'


@router.post("/chat")
async def chat_with_agent(
    payload: ChatRequest, user: User = Depends(get_authenticated_user)
):

    config = {
        "configurable": {
            "thread_id": str(user.id),
        },
        "run_name": "employee_sql_agent",
        "tags": [
            "employee-management",
            "sql-agent",
        ],
        "metadata": {
            "user_id": str(user.id),
            "role": user.roles[0].name if user.roles else "EMPLOYEE",
        },
    }

    sql_initial_state = {
        "question": payload.message,
        "user_id": str(user.id),
        "role": user.roles[0].name if user.roles else "EMPLOYEE",
    }

    return StreamingResponse(
        async_generator(sql_agent_graph, sql_initial_state, config),
        media_type="text/event-stream",
    )


@router.post("/upload-pdf")
async def uploadPdf(db: AsyncSession = Depends(get_db), file: UploadFile = File(...)):
    import io

    content = await file.read()
    pdf = PdfReader(io.BytesIO(content))
    chunks = []
    for page in pdf.pages:
        chunks.append(page.extract_text())
    text = "\n\n".join(chunks)
    split_text = splitter.split_text(text)
    embeddings = embedding_model.encode(split_text)

    policy = CompanyPolicy(
        title=file.filename or "Uploaded PDF",
        policy_type="general",
        file_name=file.filename or "unknown.pdf",
        file_url="",
    )
    db.add(policy)
    await db.commit()
    await db.refresh(policy)

    policy_chunks = []
    for i, (chunk_text, embedding) in enumerate(zip(split_text, embeddings)):
        policy_chunk = CompanyPolicyChunk(
            policy_id=policy.id,
            chunk_index=i,
            content=chunk_text,
            embedding=embedding.tolist(),
        )
        policy_chunks.append(policy_chunk)

    db.add_all(policy_chunks)
    await db.commit()

    return {"message": "PDF uploaded successfully"}


@router.get("/policies")
async def get_policies(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CompanyPolicy))
    policies = result.scalars().all()
    return policies


@router.delete("/policies/{policy_id}")
async def delete_policy(policy_id: str, db: AsyncSession = Depends(get_db)):
    # CompanyPolicyChunk should be cascaded if configured, otherwise we delete them manually
    await db.execute(delete(CompanyPolicyChunk).where(CompanyPolicyChunk.policy_id == policy_id))
    result = await db.execute(delete(CompanyPolicy).where(CompanyPolicy.id == policy_id))
    if result.rowcount == 0:
        return {"error": "Policy not found"}
    await db.commit()
    return {"message": "Policy deleted successfully"}
