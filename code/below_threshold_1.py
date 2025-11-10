def below_threshold(l: list, t: int) -> bool:
    if not isinstance(l, list):
        raise ValueError("Input must be a list")
    if len(l) < 1:
        return False
    if l[0] >= t:
        return False
    for i in range(1, len(l)):
        if l[i] >= t:
            return False
    return True