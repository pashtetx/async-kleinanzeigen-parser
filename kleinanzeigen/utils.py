from typing import List

def clear_string(string: str, chars: List[str]) -> str:
    return "".join([char for char in string if char not in chars])