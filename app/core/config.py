from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    hf_token: str = os.getenv("HF_TOKEN")
    hf_model_id: str = os.getenv("HF_MODEL_ID")
    embedding_model: str = os.getenv("EMBEDDING_MODEL")
    data_dir: str = os.getenv("DATA_DIR", "app/data")
    index_path: str = os.getenv("INDEX_PATH", "app/data/faiss_index")

settings = Settings()
