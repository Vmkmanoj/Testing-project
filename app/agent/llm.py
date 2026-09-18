from functools import lru_cache

from app.core.config import settings

# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq
from openai import OpenAI





@lru_cache
def get_llm():

    if settings.GROQ_API_KEY:
        return  ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.LLM_MODEL or "openai/gpt-oss-20b",
        )



    return None  # no key configured -> nodes use their rule-based fallback
