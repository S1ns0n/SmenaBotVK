import re

def remove_brackets_text(text: str) -> str:
    result = re.sub(r'\[[^\]]*\]', '', text)
    result = re.sub(r'(?<!\n)[ ]{2,}(?!\n)', ' ', result)
    return result.strip()