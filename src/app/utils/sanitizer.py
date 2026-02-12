import bleach

ALLOWED_TAGS = {
    'p', 'br', 'strong', 'em', 'ul', 'ol', 'li',
    'a', 'h1', 'h2', 'h3', 'h4', 'blockquote', 'code', 'pre'
}

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    '*': ['alt']
}

def sanitize_html(content: str):
    if not content:
        return ""
    
    cleaned = bleach.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )
    return cleaned