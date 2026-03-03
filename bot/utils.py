import re

def remove_brackets_text(text: str) -> str:
    result = re.sub(r'\[[^\]]*\]', '', text)
    result = re.sub(r'\s+', ' ', result).strip()
    return result