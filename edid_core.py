import struct

from utils import (
    encode_manufacturer_id,
    encode_product_id,
    encode_serial_number,
    encode_manufacture_date,
    encode_edid_version,
    build_video_input,
    encode_screen_size,
    encode_display_gamma,
    encode_supported_features,
    encode_colour_characteristics,
    encode_established_timings,
    encode_standard_timings
)

class EDID:
    def __init__(self, raw_bytes: bytes):
        if len(raw_bytes) != 128:
            raise ValueError("EDID must be exactly 128 bytes")
        self.raw = bytearray(raw_bytes)
        self.fields = self.parse_fields()
