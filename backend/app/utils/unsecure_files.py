from utils.constants import FORBIDDEN_EXTENSIONS


def is_forbidden_filetype(file_ext: str) -> bool:
    ext = file_ext.lower()
    if ext in FORBIDDEN_EXTENSIONS:
        return True
    return False
