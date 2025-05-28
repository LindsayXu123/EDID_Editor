import struct

class EDID:
    def __init__(self, raw_bytes: bytes):
        if len(raw_bytes) != 128:
            raise ValueError("EDID must be exactly 128 bytes")
        self.raw = bytearray(raw_bytes)
        self.fields = self.parse_fields()
