import msgpack

__virtualname__ = "msgpack"


def _default(data):
    if isinstance(data, set):
        return sorted(data)
    elif hasattr(data, "__iter__"):
        return list(data)
    else:
        return repr(data)


def dump(hub, data) -> bytes:
    return msgpack.packb(data, datetime=True, default=_default)


def load(hub, data: bytes):
    return msgpack.unpackb(data, strict_map_key=False)
