import os

from dotenv import load_dotenv

load_dotenv(override=True)
API_URL = os.getenv("API_URL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

MODEL_WEIGHTS_DIR = "weights/"
PERSIST_DIR = "data/store/chroma_db"
if not os.path.exists(PERSIST_DIR):
    os.makedirs(PERSIST_DIR)
