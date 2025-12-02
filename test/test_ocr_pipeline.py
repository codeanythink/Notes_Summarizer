import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, parent_dir)

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from src import ocr_pipeline, config

scanned_pdf = "data/lecture.pdf"

try:
    print(f"Testing OCR on: {scanned_pdf}")
    output_path = ocr_pipeline.ocr_pdf(scanned_pdf)

    print("\n--- SUCCESS ---")
    print(f"OCR file saved at: {output_path}")
    print("You can now open that file and try to select the text!")

except EnvironmentError as e:
    print("\n--- SETUP ERROR ---")
    print(e)
except Exception as e:
    print(f"\n--- ERROR ---")
    print(e)