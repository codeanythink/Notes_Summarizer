import numpy as np
import logging
from sklearn.metrics.pairwise import cosine_similarity
from . import config, embeddings, preprocess


logger = logging.getLogger(__name__)   #logging setup


def summarize(text: str, top_n: int = 5) -> dict:
    clean_text = preprocess.clean_text(text)  # clean text
    sentences = preprocess.split_into_sentences(clean_text)   # tokenize sentences

    logger.info(f"Summarizing document with {len(sentences)} sentences...")

    if len(sentences) <= top_n:  # if file contains too low sentences returns everything
        return {
            "summary_text": text,
            "method": "extractive_fallback",
            "sentence_count": len(sentences),
            "selected_indices": list(range(len(sentences)))
        }

    sentence_vectors = embeddings.embed_sentences(sentences)  #embedding

    centroid = embeddings.get_document_centroid(sentence_vectors)  #centroid

    scores = cosine_similarity(sentence_vectors, centroid).flatten()  #calculates similarity
    ranked_indices = np.argsort(scores)[::-1]


    selected_indices = []
    redundancy_threshold = 0.85

    for idx in ranked_indices:
        if len(selected_indices) >= top_n:
            break

        if not selected_indices:
            selected_indices.append(idx)
            continue

        candidate_vector = sentence_vectors[idx].reshape(1, -1)
        selected_vectors = sentence_vectors[selected_indices]

        sims = cosine_similarity(candidate_vector, selected_vectors)

        if np.max(sims) > redundancy_threshold:
            continue

        selected_indices.append(idx)

    selected_indices = sorted(selected_indices)

    final_sentences = [sentences[i] for i in selected_indices]  #summary construction
    summary_text = " ".join(final_sentences)

    return {
        "summary_text": summary_text,
        "method": "extractive_centroid",
        "sentence_count": len(sentences),
        "selected_indices": selected_indices
    }