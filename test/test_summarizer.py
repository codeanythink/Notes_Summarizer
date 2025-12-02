import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from src import summarizer_extractive


def test_summarization_logic():
    print("\n--- Starting Summarization Test ---")

    lecture_text = """
    The environment is the sum total of all surroundings of a living organism.
    The environment provides conditions for development and growth.
    Pollution is the introduction of contaminants into the natural environment.
    Pollution can take the form of chemical substances or energy, such as noise, heat, or light.
    The environment is crucial for life.
    Pollutants are the components of pollution.
    """

    result = summarizer_extractive.summarize(lecture_text, top_n=2)

    print(f"Summary Output: {result['summary_text']}")

    assert result is not None
    assert "summary_text" in result
    assert result["method"] == "extractive_centroid"
    assert len(result["selected_indices"]) <= 2

    print("✅ Summarizer test passed!")