import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

DATA_DIR = BASE_DIR / "data"

CACHE_DIR = BASE_DIR / "cache"

LOGS_DIR = BASE_DIR / "logs"

DATA_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

MAX_FILE_SIZE_MB = 200

VALID_EXTENSIONS = {'.pdf', '.txt'}

CHUNK_SIZE = 3000

CHUNK_OVERLAP = 500

MIN_SENTENCE_LENGTH = 20

EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'

ABSTRACTIVE_MODEL_NAME = 'sshleifer/distilbart-cnn-12-6'

SIMILARITY_THRESHOLD = 0.75

MMR_LAMBDA = 0.6