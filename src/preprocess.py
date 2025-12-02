import re
import spacy
import logging
import config

logger = logging.getLogger(__name__)   # logging setup

try:   # SpaCy model loading
    nlp = spacy.load("en_core_web_sm", disable=['ner', 'tagger'])
    nlp.max_length = 3000000  # Increase limit for large PDFs
except OSError:
    logger.error("SpaCy model 'en_core_web_sm' not found.")
    logger.error("Please run: python -m spacy download en_core_web_sm")
    raise ImportError("Missing spaCy model. Run: python -m spacy download en_core_web_sm")


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)   # fixes   "Enviro- \n ment" -> "Environment"


    text = re.sub(r'(Page|Pg\.)\s*\d+(?:\s*of\s*\d+)?', '', text, flags=re.IGNORECASE) #removes page number etc.

    text = re.sub(r'(Fig\.|Figure|Table)\s*\d+', '', text, flags=re.IGNORECASE) #removes figures and tables

    text = re.sub(r'\[\d+(?:-\d+)?\]', '', text) # removes citation like [1]

    text = re.sub(r'http\S+', '', text) #removes the url
    text = re.sub(r'\S+@\S+', '', text)  #removes the emails


    text = text.replace('\n', ' ')  #replces newlines

    text = re.sub(r'\s+', ' ', text) #collapse multiple spaces

    return text.strip()


def split_into_sentences(text: str) -> list:   #tokenization
    if not text:
        return []

    doc = nlp(text)   #pipeline converts into sentences

    sentences = []

    for sent in doc.sents:
        clean_sent = sent.text.strip()

        if len(clean_sent) > config.MIN_SENTENCE_LENGTH:
            sentences.append(clean_sent)

    return sentences