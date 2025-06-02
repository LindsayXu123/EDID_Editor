
def encode_manufacturer_id(manufacturer: str) -> str:
    """
    Convert a 3-letter manufacturer ID into 2 encoded bytes
    """
    if len(manufacturer) != 3 or not manufacturer.isalpha():
        raise ValueError("Manufacturer ID must be 3 alphabetic characters.")

    manufacturer = manufacturer.upper()
    c1 = ord(manufacturer[0]) - ord('A') + 1
    c2 = ord(manufacturer[1]) - ord('A') + 1
    c3 = ord(manufacturer[2]) - ord('A') + 1

    b1 = (c1 << 2) | (c2 >> 3)
    b2 = ((c2 & 0x07) << 5) | c3

    return f"{b1:02X} {b2:02X}"


def encode_product_id(product_id: int) -> str:
    """
    Convert product ID to 2 bytes in little endian format.
    """
    if not (0 <= product_id <= 0xFFFF):
        raise ValueError("Product ID must be a 16-bit unsigned integer.")
    
    b = product_id.to_bytes(2, byteorder='little')
    return f"{b[0]:02X} {b[1]:02X}"


def encode_serial_number(serial: int) -> str:
    """
    Convert serial number (int) to 4 bytes in little endian format.
    """
    if not (0 <= serial <= 0xFFFFFFFF):
        raise ValueError("Serial number must be a 32-bit unsigned integer.")
    
    b = serial.to_bytes(4, byteorder='little')
    return " ".join(f"{byte:02X}" for byte in b)


def encode_manufacture_date(week: int, year: int) -> str:
    """
    Convert manufacture week and year into EDID hex string
    """
    if not (1 <= week <= 53):
        raise ValueError("Invalid week")
    if not (1990 <= year <= 1990 + 254):
        raise ValueError("Invalid year")
    
    week_byte = week
    year_byte = year - 1990
    return f"{week_byte:02X} {year_byte:02X}"

def encode_edid_version(version: int, revision: int) -> str:
    """
    Encode EDID version and revision into a hex string
    """
    if not (0 <= version <= 255):
        raise ValueError("Version must be a valid byte (0-255).")
    if not (0 <= revision <= 255):
        raise ValueError("Revision must be a valid byte (0-255).")
    
    return f"{version:02X} {revision:02X}"

def build_video_input(
    input_type: str,
    bits_per_color: str = None,
    interface: str = None,
    signal_level: str = None,
    setup: bool = False,
    sync_hv: bool = False,
    sync_comp: bool = False,
    sync_green: bool = False,
    sync_serration: bool = False
) -> str:

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
        byte |= (level_index & 0x03) << 5
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

    return f"{byte:02X}"

def encode_screen_size(horizontal_cm: int, vertical_cm: int) -> str:
    """
    Encode screen dimensions in centimeters to EDID format.
    """
    if not (0 <= horizontal_cm <= 255 and 0 <= vertical_cm <= 255):
        raise ValueError("Screen dimensions must be 0–255 cm.")

    return f"{horizontal_cm:02X} {vertical_cm:02X}"

def encode_display_gamma(gamma: float) -> str:
    """
    Encode display gamma into EDID format
    """
    if gamma <= 1.0 or gamma > 3.54:
        raise ValueError("Gamma must be in range (1.0, 3.54]")

    encoded = int(round(gamma * 100)) - 100
    return f"{encoded:02X}"

def encode_supported_features(
    standby: bool,
    suspend: bool,
    active_off: bool,
    display_type: int,
    srgb: bool,
    preferred_timing: bool,
    continuous_timing: bool,
    digital: bool
) -> str:

    if not (0 <= display_type <= 3):
        raise ValueError("display_type must be between 0 and 3")

    features = 0
    if standby:
        features |= 0b01000000  # Bit 5
    if suspend:
        features |= 0b00100000  # Bit 4
    if active_off:
        features |= 0b00010000  # Bit 3

    features |= (display_type & 0b11) << 3

    if srgb:
        features |= 0b00000100  # Bit 2
    if preferred_timing:
        features |= 0b00000010  # Bit 1
    if continuous_timing:
        features |= 0b00000001  # Bit 0

    return f"{features:02X}"

def encode_colour_characteristics(
    red_x, red_y, green_x, green_y,
    blue_x, blue_y, white_x, white_y
):
    rx = int(red_x * 1024 + 0.5)
    ry = int(red_y * 1024 + 0.5)
    gx = int(green_x * 1024 + 0.5)
    gy = int(green_y * 1024 + 0.5)
    bx = int(blue_x * 1024 + 0.5)
    by = int(blue_y * 1024 + 0.5)
    wx = int(white_x * 1024 + 0.5)
    wy = int(white_y * 1024 + 0.5)

    red_green_lo = ((rx & 0x03) << 6) | ((ry & 0x03) << 4) | ((gx & 0x03) << 2) | (gy & 0x03)
    blue_white_lo = ((bx & 0x03) << 6) | ((by & 0x03) << 4) | ((wx & 0x03) << 2) | (wy & 0x03)

    edid_bytes = [
        red_green_lo,        # byte 25
        blue_white_lo,       # byte 26
        (rx >> 2) & 0xFF,    # byte 27
        (ry >> 2) & 0xFF,    
        (gx >> 2) & 0xFF,    
        (gy >> 2) & 0xFF,    
        (bx >> 2) & 0xFF,    
        (by >> 2) & 0xFF,    
        (wx >> 2) & 0xFF,    
        (wy >> 2) & 0xFF     
    ]

    return " ".join(f"{b:02X}" for b in edid_bytes)

def encode_established_timings(selected_timings, manufacturer_byte=0x00):
    established_timings = [
        "720x400 @ 70Hz", "720x400 @ 88Hz", "640x480 @ 60Hz", "640x480 @ 67Hz",
        "640x480 @ 72Hz", "640x480 @ 75Hz", "800x600 @ 56Hz", "800x600 @ 60Hz",
        "800x600 @ 72Hz", "800x600 @ 75Hz", "832x624 @ 75Hz", "1024x768 @ 87Hz (interlaced)",
        "1024x768 @ 60Hz", "1024x768 @ 70Hz", "1024x768 @ 75Hz", "1280x1024 @ 75Hz"
    ]

    timing1 = 0
    timing2 = 0

    for i, name in enumerate(established_timings):
        if name in selected_timings:
            if i < 8:
                timing1 |= (1 << (7 - i))
            else:
                timing2 |= (1 << (15 - i))

    return f"{timing1:02X} {timing2:02X} {manufacturer_byte:02X}"

def encode_standard_timings(timings):
    
    aspect_map = {
        "16:10": 0b00,
        "4:3":   0b01,
        "5:4":   0b10,
        "16:9":  0b11
    }

    result_bytes = []

    for i in range(8):
        if i >= len(timings) or timings[i] is None:
            result_bytes.extend([0x01, 0x01])
        else:
            hres, aspect_str, refresh_rate = timings[i]

            if aspect_str not in aspect_map:
                raise ValueError(f"Unknown aspect ratio: {aspect_str}")

            byte1 = (hres // 8) - 31
            aspect_code = aspect_map[aspect_str]
            vfreq_offset = refresh_rate - 60

            byte2 = (aspect_code << 6) | (vfreq_offset & 0x3F)

            result_bytes.extend([byte1, byte2])

    return ' '.join(f"{b:02X}" for b in result_bytes)



def calculate_checksum(edid_data: bytearray) -> int:
    """
    Calculate EDID checksum (last byte such that sum of 128 bytes == 0 mod 256).
    """
    if len(edid_data) != 128:
        raise ValueError("EDID data must be 128 bytes")
    checksum = (256 - (sum(edid_data[:127]) % 256)) % 256
    return checksum

def generate_all(manufacturer:str, product:int, serial: int, week: int, year: int, version:int, revision: int, input_type: str,
    bits_per_color: str, interface: str, signal_level: str, setup: bool, sync_hv: bool, sync_comp: bool, sync_green: bool, sync_serration: bool, 
    horizontal:int, vertical:int, gamma: float, standby: bool, suspend: bool, active_off: bool, display_type: int, srgb: bool, preferred_timing: bool, 
    continuous_timing: bool, digital: bool, red_x, red_y, green_x, green_y, blue_x, blue_y, white_x, white_y, selected_timings, manufacturer_byte, timings
):
    encode_manufacturer_id(manufacturer)
    encode_product_id(product)
    encode_serial_number(serial)
    encode_manufacture_date(week, year)
    encode_edid_version(version, revision)
    build_video_input(input_type, bits_per_color, interface, signal_level, setup, sync_hv, sync_comp, sync_green, sync_serration)
    encode_screen_size(horizontal, vertical)
    encode_display_gamma(gamma)
    encode_supported_features(standby, suspend, active_off, display_type, srgb, preferred_timing, continuous_timing, digital)
    encode_colour_characteristics(red_x, red_y, green_x, green_y, blue_x, blue_y, white_x, white_y)
    encode_established_timings(selected_timings, manufacturer_byte)
    encode_standard_timings(timings)