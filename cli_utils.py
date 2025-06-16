def encode_manufacturer_id(edid: bytearray, manufacturer: str) -> None:
    if len(manufacturer) != 3 or not manufacturer.isalpha() or not manufacturer.isupper():
        raise ValueError("Manufacturer must be 3 uppercase letters")
    val = 0
    for c in manufacturer:
        val <<= 5
        val += (ord(c) - ord('A') + 1)
    edid[8] = (val >> 8) & 0xFF
    edid[9] = val & 0xFF

def encode_product_id(edid: bytearray, product_code: int) -> None:
    if not (0 <= product_code <= 0xFFFF):
        raise ValueError("Product code must be a 16-bit integer")
    edid[10] = product_code & 0xFF
    edid[11] = (product_code >> 8) & 0xFF

def encode_serial_number(edid: bytearray, serial: int) -> None:
    if not (0 <= serial <= 0xFFFFFFFF):
        raise ValueError("Serial number must be a 32-bit integer")
    for i in range(4):
        edid[12 + i] = (serial >> (8 * i)) & 0xFF

def encode_manufacture_date(edid: bytearray, week: int, year: int) -> None:
    if not (1 <= week <= 53):
        raise ValueError("Week must be between 1 and 53")
    if not (1990 <= year <= 2090):
        raise ValueError("Year must be between 1990 and 2090")
    edid[16] = week
    edid[17] = year - 1990

def encode_edid_version(edid: bytearray, version: int, revision: int) -> None:
    if not (0 <= version <= 255):
        raise ValueError("Version must be 0-255")
    if not (0 <= revision <= 255):
        raise ValueError("Revision must be 0-255")
    edid[18] = version
    edid[19] = revision

def encode_input_type(edid: bytearray, input_type: str,
                      bits_per_color: str = None, interface: str = None,
                      signal_level: str = None, setup: bool = False,
                      sync_hv: bool = False, sync_comp: bool = False,
                      sync_green: bool = False, sync_serration: bool = False) -> None:
    byte = 0
    if input_type.lower() == "digital":
        byte |= 0x80
        bits = ["Undefined", "6", "8", "10", "12", "14", "16", "Reserved"]
        interfaces = ["Undefined", "DVI", "HDMIa", "HDMIb", "MDDI", "DisplayPort"]
        bit_index = bits.index(bits_per_color) if bits_per_color in bits else 0
        interface_index = interfaces.index(interface) if interface in interfaces else 0
        byte |= (bit_index & 0x07) << 4
        byte |= interface_index & 0x0F
    elif input_type.lower() == "analog":
        levels = [
            "0.700, 0.300 (1.0 V p-p)",
            "0.714, 0.286 (1.0 V p-p)",
            "1.000, 0.286 (1.0 V p-p)",
            "0.700, 0.000 (0.7 V p-p)",
        ]
        level_index = levels.index(signal_level) if signal_level in levels else 0
        byte |= (level_index & 0x03) << 4
        byte |= 0x10 if setup else 0
        if sync_hv:
            byte |= 0x08
        if sync_comp:
            byte |= 0x04
        if sync_green:
            byte |= 0x02
        if sync_serration:
            byte |= 0x01
    else:
        raise ValueError("Input type must be either 'Digital' or 'Analog'")
    edid[20] = byte

def encode_screen_size(edid: bytearray, horizontal: int, vertical: int) -> None:
    if not (0 <= horizontal <= 255) or not (0 <= vertical <= 255):
        raise ValueError("Screen size must be 0-255 cm")
    edid[21] = horizontal
    edid[22] = vertical

def encode_display_gamma(edid: bytearray, gamma: float) -> None:
    if not (1.0 <= gamma <= 3.0):
        raise ValueError("Gamma must be between 1.0 and 3.0")
    val = int(gamma * 100) - 100
    edid[23] = val & 0xFF

def encode_supported_features(edid: bytearray, display_type: int,
                              standby=False, suspend=False, active_off=False,
                              srgb=False, preferred_timing=False, continuous_timing=False,
                              digital=False) -> None:
    byte = 0
    if standby:
        byte |= 0x80
    if suspend:
        byte |= 0x40
    if active_off:
        byte |= 0x20
    if display_type not in {0,1,2,3}:
        raise ValueError("Display type must be 0,1,2, or 3")
    byte |= (display_type & 0x03) << 3
    if srgb:
        byte |= 0x04
    if preferred_timing:
        byte |= 0x02
    if continuous_timing:
        byte |= 0x01
    if digital:
        byte |= 0x08
    edid[24] = byte

def encode_colour_characteristics(edid: bytearray,
                                  red_x: float, red_y: float,
                                  green_x: float, green_y: float,
                                  blue_x: float, blue_y: float,
                                  white_x: float, white_y: float) -> None:
    
    def to_10bit(val):
        if not 0 <= val <= 1:
            raise ValueError("Color coordinates must be between 0 and 1")
        return int(val * 1023)
    
    rx = to_10bit(red_x)
    ry = to_10bit(red_y)
    gx = to_10bit(green_x)
    gy = to_10bit(green_y)
    bx = to_10bit(blue_x)
    by = to_10bit(blue_y)
    wx = to_10bit(white_x)
    wy = to_10bit(white_y)
    
    edid[25] = ((rx >> 8) << 6) | ((ry >> 8) << 4) | ((gx >> 8) << 2) | ((gy >> 8) << 0)
    
    edid[26] = rx & 0xFF
    edid[27] = ry & 0xFF
    edid[28] = gx & 0xFF
    edid[29] = gy & 0xFF
    
    edid[30] = ((bx >> 8) << 6) | ((by >> 8) << 4) | ((wx >> 8) << 2) | ((wy >> 8) << 0)
    
    edid[31] = bx & 0xFF
    edid[32] = by & 0xFF
    edid[33] = wx & 0xFF
    edid[34] = wy & 0xFF

def encode_established_timings(edid: bytearray, selected_timings: list, manufacturer_byte: int) -> None:
    # Clear established timings block
    edid[35] = 0
    edid[36] = 0
    edid[37] = manufacturer_byte if manufacturer_byte is not None else 0

    timing_map = {
        "720x400@70Hz": (35, 0b10000000),
        "720x400@88Hz": (35, 0b01000000),
        "640x480@60Hz": (35, 0b00100000),
        "640x480@67Hz": (35, 0b00010000),
        "640x480@72Hz": (35, 0b00001000),
        "640x480@75Hz": (35, 0b00000100),
        "800x600@56Hz": (35, 0b00000010),
        "800x600@60Hz": (35, 0b00000001),
        "800x600@72Hz": (36, 0b10000000),
        "800x600@75Hz": (36, 0b01000000),
        "832x624@75Hz": (36, 0b00100000),
        "1024x768@87Hz (interlaced)": (36, 0b00010000),
        "1024x768@60Hz": (36, 0b00001000),
        "1024x768@70Hz": (36, 0b00000100),
        "1024x768@75Hz": (36, 0b00000010),
        "1280x1024@75Hz": (36, 0b00000001),
    }

    for timing in selected_timings:
        if timing not in timing_map:
            raise ValueError(f"Unknown established timing: {timing}")
        byte_index, bit_mask = timing_map[timing]
        edid[byte_index] |= bit_mask


def encode_standard_timings(edid: bytearray, timings: list) -> None:
    aspect_map = {
        "16:10": 0b00,
        "4:3":   0b01,
        "5:4":   0b10,
        "16:9":  0b11
    }
    for i in range(38, 54):
        edid[i] = 0x01

    for i in range(min(8, len(timings))):
        timing = timings[i]
        if timing is None:
            edid[38 + 2*i] = 0x01
            edid[39 + 2*i] = 0x01
            continue
        hres, aspect_str, refresh_rate = timing
        hres = int(hres)
        refresh_rate = int(refresh_rate)
        if aspect_str not in aspect_map:
            raise ValueError(f"Unknown aspect ratio: {aspect_str}")
        byte1 = (hres // 8) - 31
        aspect_code = aspect_map[aspect_str]
        vfreq_offset = refresh_rate - 60
        byte2 = (aspect_code << 6) | (vfreq_offset & 0x3F)
        edid[38 + 2*i] = byte1 & 0xFF
        edid[39 + 2*i] = byte2 & 0xFF

def update_checksum(edid: bytearray) -> None:
    checksum = (256 - (sum(edid[:127]) % 256)) % 256
    edid[127] = checksum

def generate_all(
    manufacturer: str, product: int, serial: int, week: int, year: int,
    version: int, revision: int, input_type: str,
    bits_per_color: str, interface: str, signal_level: str,
    setup: bool, sync_hv: bool, sync_comp: bool, sync_green: bool, sync_serration: bool,
    horizontal: int, vertical: int, gamma: float,
    standby: bool, suspend: bool, active_off: bool, display_type: int,
    srgb: bool, preferred_timing: bool, continuous_timing: bool, digital: bool,
    red_x: float, red_y: float, green_x: float, green_y: float,
    blue_x: float, blue_y: float, white_x: float, white_y: float,
    selected_timings, manufacturer_byte, timings
):
    edid = bytearray(128)
    
    header_bytes = [0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00]
    for i, b in enumerate(header_bytes):
        edid[i] = b
    
    encode_manufacturer_id(edid, manufacturer)
    encode_product_id(edid, product)
    encode_serial_number(edid, serial)
    encode_manufacture_date(edid, week, year)
    encode_edid_version(edid, version, revision)
    encode_input_type(edid, input_type, bits_per_color, interface, signal_level, setup, sync_hv, sync_comp, sync_green, sync_serration)
    encode_screen_size(edid, horizontal, vertical)
    encode_display_gamma(edid, gamma)
    encode_supported_features(edid, display_type, standby, suspend, active_off, srgb, preferred_timing, continuous_timing, digital)
    encode_colour_characteristics(edid, red_x, red_y, green_x, green_y, blue_x, blue_y, white_x, white_y)
    encode_established_timings(edid, selected_timings, manufacturer_byte)
    encode_standard_timings(edid, timings)
        
    all_bytes = [f"{b:02X}" for b in edid]
    lines = [" ".join(all_bytes[i:i+16]) for i in range(0, len(all_bytes), 16)]
    
    return "\n".join(lines)
