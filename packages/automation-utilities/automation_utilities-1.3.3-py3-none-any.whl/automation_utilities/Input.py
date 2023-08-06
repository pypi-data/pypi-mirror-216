def int_input(prompt: str, default: int) -> int:
    try:
        return int(input(prompt))
    except ValueError:
        return default
