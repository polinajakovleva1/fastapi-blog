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
    """
    Очистка HTML-контента от XSS-уязвимостей

    удаляет все теги и атрибуты, кроме разрешенных
        теги: перечислены в ALLOWED_TAGS
        атрибуты: перечислены в ALLOWED_ATTRIBUTES
    """
    if not content:
        return ""
    
    cleaned = bleach.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )
    return cleaned