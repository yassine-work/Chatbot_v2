import re

def sanitize_input(text, max_length=100):
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Allow letters, numbers, spaces, and apostrophes
    text = re.sub(r'[^a-zA-Z0-9\s\']', '', text)
    return text[:max_length]