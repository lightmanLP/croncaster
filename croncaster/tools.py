import math


def to_bytes(value: int) -> bytes:
    return value.to_bytes(math.ceil(value.bit_length() / 8), "big")


def to_int(value: bytes) -> int:
    return int.from_bytes(value, "big")
