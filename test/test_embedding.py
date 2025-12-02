import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, parent_dir)

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  #OMP fix

from src import embeddings

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import numpy as np
from src import embeddings


def test_embedding_generation():
    sample_sentences = [
        "The environment is crucial for human survival.",
        "Pollution damages the ecosystem.",
        "I like to eat pizza for dinner.",
        "Climate change is a global issue."
    ]

    print("\n--- 1. Testing Model Loading ---")
    vectors = embeddings.embed_sentences(sample_sentences)

    assert vectors is not None
    assert vectors.shape == (4, 384), f"Expected shape (4, 384), got {vectors.shape}"
    print("✅ Embeddings generated successfully.")

    print("\n--- 2. Testing Centroid Logic ---")
    centroid = embeddings.get_document_centroid(vectors)

    assert centroid.shape == (1, 384), f"Expected centroid (1, 384), got {centroid.shape}"
    print("✅ Centroid calculated correctly.")

# To run this, type in terminal: pytest -s test_embedding.py
# The -s flag tells pytest to show the 'print' statements