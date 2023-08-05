def shorten(text: str, width: int, placeholder: str = "...", end: bool = False) -> str:
    """Truncate text

    used for repr() of models
    """

    width = max(width, len(placeholder))
    if len(text) <= width:
        return text
    pos = width - len(placeholder)
    if pos == 0:
        return placeholder
    if end:
        return placeholder + text[-pos:]
    return text[:pos] + placeholder
