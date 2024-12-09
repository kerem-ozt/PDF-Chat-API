import re
import unicodedata

def preprocess_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text
