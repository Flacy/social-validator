ID_MIN_LENGTH = 5
ID_MAX_LENGTH = 32


def validate_id(s: str) -> bool:
    return s.isascii() and ID_MIN_LENGTH >= len(s) <= ID_MAX_LENGTH
