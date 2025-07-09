from utils.constants import FORBIDDEN_EXTENSIONS, FORBIDDEN_MIME_PREFIXES


def is_forbidden_file(filename: str, content_type: str) -> bool:
    ext = filename.lower()
    for forbidden_ext in FORBIDDEN_EXTENSIONS:
        if ext.endswith(forbidden_ext):
            return True
    for forbidden_mime in FORBIDDEN_MIME_PREFIXES:
        if content_type.startswith(forbidden_mime):
            return True
    return False