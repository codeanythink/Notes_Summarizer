import logging
import numpy as np
from sentence_transformers import SentenceTransformer
import config
import utils


logger = logging.getLogger(__name__) # Looging setup

_MODEL_INSTANCE = None # Loads the model in RAM to prevent reloading


def load_model():
    global _MODEL_INSTANCE

    if _MODEL_INSTANCE is None:
        model_name = config.EMBEDDING_MODEL_NAME
        device = utils.get_device()  # 'cuda', 'mps', or 'cpu'

        logger.info(f"Loading embedding model: {model_name} on {device}...")
        print(f"Loading AI Model ({model_name})... this happens only once.")

        try:
            _MODEL_INSTANCE = SentenceTransformer(model_name, device=device) #Model Loading
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise e

    return _MODEL_INSTANCE


def embed_sentences(sentences: list) -> np.ndarray: # Embedds the sentences in vectors
    if not sentences:
        return np.array([])

    model = load_model()

    embeddings = model.encode(  # Sentence embedding
        sentences,
        batch_size=32,
        show_progress_bar=True,
        convert_to_numpy=True
    )
    return embeddings


def get_document_centroid(embeddings: np.ndarray) -> np.ndarray:
    if embeddings.size == 0: # if not embedding found it handles
        return np.array([])

    centroid = np.mean(embeddings, axis=0) # Calculates the mean
    return centroid.reshape(1, -1)