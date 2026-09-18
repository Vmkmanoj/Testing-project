


from pydantic import BaseSettings
from typing_extensions import Optional
import os
from dotenv import load_dotenv
load_dotenv()



class Settings(BaseSettings):
    groq_api_key : Optional[str] = os.getenv("GROQ_API_KEY")
    llm_model : Optional[str] = os.getenv("LLM_MODEL")
    class Config:
        env_file = ".env"
