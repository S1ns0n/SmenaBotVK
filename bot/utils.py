import re
import random

def remove_brackets_text(text: str) -> str:
    result = re.sub(r'\[[^\]]*\]', '', text)
    result = re.sub(r'(?<!\n)[ ]{2,}(?!\n)', ' ', result)
    return result.strip()

def get_random_text(text_list: list):
    return random.choice(text_list)