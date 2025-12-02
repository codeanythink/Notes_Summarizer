import os
import logging
import pdfplumber
from pathlib import Path
import config



class FileLoaderError(Exception): pass  # Custom Exception for handling File loading error


class FileSizeError(FileLoaderError): pass   # Custom Exception for handling File size error


class FileExtensionError(FileLoaderError): pass    # Custom Exception for handling File extension error


class ScannedPDFError(FileLoaderError): pass     # Custom Exception for handling pdf scanned error


def _is_scanned_heuristic(text: str, num_pages: int) -> bool:  # it checks the scanned pdf is not empty or low in characters
    if num_pages == 0: return False
    avg_chars = len(text) / num_pages
    return avg_chars < 50


def validate_file(file_path: str):
    path = Path(file_path)

    if not path.exists():   #check path exists or not
        raise FileNotFoundError(f"File not found at: {file_path}")

    if path.suffix.lower() not in config.VALID_EXTENSIONS:    # checks file extension only .pdf and .txt supported
        raise FileExtensionError(f"File extension {path.suffix} is not supported. Check src/config.py")

    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > config.MAX_FILE_SIZE_MB:    # checks file size supported file size is 200 MB
        raise FileSizeError(f"File too large ({size_mb:.2f}MB). Max is {config.MAX_FILE_SIZE_MB}MB.")


def read_text_file(file_path: str) -> dict:    # reads text file
    validate_file(file_path)
    path = Path(file_path)
    try:     # if file contains unicodes decodes in latin-1 and utf-8 format to reduce errors
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except UnicodeDecodeError:
        with open(path, "r", encoding="latin-1") as f:
            text = f.read()

    return {     #returns metadata of file
        "text": text,
        "pages": [],
        "metadata": {"source": path.name, "type": "txt"}
    }


def read_pdf(file_path: str) -> dict:    # reads pdf file
    validate_file(file_path)
    path = Path(file_path)
    full_text = ""
    pages_list = []

    try:      # if file is pdf without images it reads text from pdf
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                pages_list.append(text)
                full_text += text + "\n"
    except Exception as e:
        raise FileLoaderError(f"PDF Error: {e}")

    if _is_scanned_heuristic(full_text, len(pages_list)):   # tells pdf has images
        raise ScannedPDFError(f"Scanned PDF detected: {path.name}")

    return {  #returns metadat of pdf
        "text": full_text.strip(),
        "pages": pages_list,
        "metadata": {
            "source": path.name,
            "num_pages": len(pages_list),
            "type": "pdf"
        }
    }


def load_from_string(raw_text: str) -> dict:    # reads pasted text
    if not raw_text or not raw_text.strip():
        raise ValueError("Empty text.")

    return {     # returns metadat of pasted text
        "text": raw_text.strip(),
        "pages": [],
        "metadata": {
            "source": "User Paste",
            "type": "paste",
            "num_pages": 0
        }
    }