import os
import logging
import ocrmypdf
from pathlib import Path
from . import config

logger = logging.getLogger(__name__)   # logging setup


def ocr_pdf(input_path: str) -> str:    # if file contains images it converts pdf using ocr
    input_file = Path(input_path)

    output_filename = f"{input_file.stem}_ocr{input_file.suffix}"   # saves file after ocr completes
    output_path = config.CACHE_DIR / output_filename

    if output_path.exists():   # checks output file exists or not
        logger.info(f"Found cached OCR file: {output_path}")
        return str(output_path)

    logger.info(f"Starting OCR for: {input_file.name}")
    print(f"⏳ Running OCR on {input_file.name}... this usually takes 30-60 seconds.")

    try:     # reads the pdffrom output file generated from ocr
        result = ocrmypdf.ocr(
            input_file=input_path,
            output_file=output_path,
            deskew=True,  # Fixes crooked pages (e.g., photo of a book)
            force_ocr=True,  # Force text recognition even if it sees noise
            output_type='pdf',  # Standard PDF output
            optimize=1,  # Light compression to keep file size down
            progress_bar=False  # We disable the bar to keep logs clean
        )

        if result == 0:
            logger.info("OCR Complete.")
            return str(output_path)
        else:
            raise Exception(f"OCR failed with return code {result}")

    except ocrmypdf.exceptions.MissingDependencyError:
        error_msg = (
            "CRITICAL: OCR tools missing.\n"
            "If local: Install Tesseract & Ghostscript.\n"
            "If on Cloud: Ensure 'packages.txt' contains 'tesseract-ocr'."
        )
        logger.error(error_msg)
        raise EnvironmentError(error_msg)

    except Exception as e:
        logger.error(f"OCR Error: {e}")
        if output_path.exists(): # if same file exists then it removes partially loaded
            os.remove(output_path)
        raise e