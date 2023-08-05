"""
Serialize data by casting it to a plain string
"""
import ast

__virtualname__ = "str"


def dump(hub, data) -> bytes:
    return str(data).encode()


def load(hub, data: bytes):
    data = data.decode()
    try:
        return ast.literal_eval(data)
    except:
        return data
