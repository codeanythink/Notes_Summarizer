import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, parent_dir)

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from src import preprocess

raw_messy_text = """
This is a test of the Enviro- 
ment. Page 1 of 50.
We are testing Fig. 1 and [12] citations.
"""

print("--- RAW ---")
print(raw_messy_text)

cleaned = preprocess.clean_text(raw_messy_text)
print("\n--- CLEANED ---")
print(cleaned)

sentences = preprocess.split_into_sentences(cleaned)
print("\n--- SENTENCES ---")
print(sentences)