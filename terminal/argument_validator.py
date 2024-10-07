def is_valid_int(input: str) -> bool:
    if not is_valid_str(input):
        return False

    try:
        _ = int(input)
        return True
    except ValueError:
        return False


def is_valid_dimension(input: str) -> bool:
    if not is_valid_str(input):
        return False

    try:
        input = input.lower()

        if "x" not in input:
            return False

        width, length = input.lower().split("x")
        if not is_valid_float(width) or not is_valid_float(length):
            return False

        return True
    except (ValueError, AttributeError):
        print("error")
        return False


def is_valid_float(input: str) -> bool:
    if not is_valid_str(input):
        return False

    try:
        _ = float(input)
        return True
    except ValueError:
        return False


def is_valid_str(input: str):
    if isinstance(input, str) and len(input) > 0:
        return True
    return False
