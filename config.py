import os
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = "cohere/command-r-plus"
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_data")

print(f"API Key Loaded in config.py: {OPENROUTER_API_KEY}")
print(f"Redis Config: {REDIS_HOST}:{REDIS_PORT}, DB {REDIS_DB}")
print(f"ChromaDB Path: {CHROMA_PATH}")