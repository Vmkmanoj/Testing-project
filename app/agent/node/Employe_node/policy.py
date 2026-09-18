import asyncio
import logging

from app.agent.state import SQLAgentState
from app.database.database import AsyncSessionLocal
from app.models.company_policy_chunk_model import CompanyPolicyChunk

from sqlalchemy import select
from sentence_transformers import SentenceTransformer
from app.agent.llm import get_llm

from langchain_core.messages import SystemMessage, HumanMessage


logger = logging.getLogger(__name__)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


async def policy(state: SQLAgentState):
    print("--- ENTERING NODE: policy ---")

    question = state.get("question", "")

    # 1. Run synchronous embedding generation in a worker thread
    question_vector = await asyncio.to_thread(
        embedding_model.encode,
        question
    )

    question_vector = question_vector.tolist()

    # 2. Query PostgreSQL using async SQLAlchemy
    async with AsyncSessionLocal() as session:

        stmt = (
            select(CompanyPolicyChunk)
            .order_by(
                CompanyPolicyChunk.embedding.cosine_distance(
                    question_vector
                )
            )
            .limit(3)
        )

        result = await session.execute(stmt)

        chunks = result.scalars().all()

    # 3. Format retrieved policy text
    if chunks:
        context_text = "\n\n".join(
            f"Chunk {i + 1}:\n{chunk.content}"
            for i, chunk in enumerate(chunks)
        )
    else:
        context_text = "No relevant policy documents found."

    # 4. Generate answer
    llm = get_llm()

    if llm:

        system_prompt = (
            "You are an HR Assistant. Answer the employee's question "
            "using the provided company policy excerpts.\n\n"

            "Your task is to identify and summarize the MOST IMPORTANT "
            "information from the policy that is relevant to the employee's question.\n"

            "Do not simply copy or repeat the entire context. "
            "Summarize it in a clear, concise, and easy-to-understand way.\n"

            "Focus only on information relevant to the employee's question, "
            "including important rules, eligibility, limits, deadlines, "
            "exceptions, and required actions.\n"

            "If the policy contains multiple relevant points, "
            "present them as short bullet points.\n"

            "Do not make assumptions or add information that is not present "
            "in the provided policies.\n"

            'If the answer is not contained in the provided excerpts, say: '
            '"I don\'t have enough information in the company policies '
            'to answer this question."\n\n'

            f"Company Policy Context:\n{context_text}"
        )

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=question),
        ]

        # Async LLM call
        response = await llm.ainvoke(messages)

        final_answer = response.content

    else:
        final_answer = (
            f"Here is what I found in the policies:\n{context_text}"
        )

    return {
        "final_answer": final_answer
    }