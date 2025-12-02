import os
import shutil
import hashlib
import torch
import logging
from pathlib import Path
import config

logger = logging.getLogger(__name__)  #setup logging


def save_uploaded_file(uploaded_file) -> str:
    file_path = config.DATA_DIR / uploaded_file.name

    try:    #handles uploaded file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        logger.info(f"File saved to: {file_path}")
        return str(file_path)

    except Exception as e:
        logger.error(f"Failed to save file: {e}")
        raise IOError(f"Could not save file to disk: {e}")


def get_device() -> str:
    if torch.cuda.is_available():    # detects hardware to return best compatible model
        return "cuda"  # NVIDIA
    elif torch.backends.mps.is_available():
        return "mps"  #APPLE SILICON
    else:
        return "cpu"  #device cpu


def get_content_hash(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()   # returns stored same content


def ensure_directory(path: Path):    #if file does not exists creates it
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)