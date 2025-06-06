EDID_LENGTH = 128

def check_header(edid: bytes) -> bool:
    if (len(edid) < 8 or
        edid[0] != 0x00 or edid[1] != 0xFF or edid[2] != 0xFF or edid[3] != 0xFF or
        edid[4] != 0xFF or edid[5] != 0xFF or edid[6] != 0xFF or edid[7] != 0x00):
        return False 
    return True

def parse_manufacturer_id(edid: bytes) -> str:
    manufacturer = (edid[8] << 8) | edid[9]
    manufacturer_id = ''.join([
        chr(((manufacturer >> 10) & 0x1F) + ord('A') - 1),
        chr(((manufacturer >> 5) & 0x1F) + ord('A') - 1),
        chr((manufacturer & 0x1F) + ord('A') - 1)
    ])
    return manufacturer_id

def parse_product_code(edid: bytes) -> int:
    return edid[10] | (edid[11] << 8)

def parse_serial_number(edid: bytes) -> int:
    return int.from_bytes(edid[12:16], byteorder='little')

def parse_week(edid: bytes) -> int:
    return edid[16]

def parse_year(edid: bytes) -> int:
    return edid[17] + 1990

def parse_edid_version(edid: bytes) -> int:
    return edid[0x12]

def parse_edid_revision(edid: bytes) -> int:
    return edid[0x13]

def parse_screen_size(edid: bytes) -> list[tuple[str, str]]:
    horizontal_size = edid[21]
    vertical_size = edid[22]

    text = f"Screen Size: {horizontal_size} cm x {vertical_size} cm"
    return [(text, "guidef")]


def parse_video_input(edid: bytes) -> dict:
    result = {}
    input_byte = edid[20]

    if input_byte & 0x80:
        result["signal_type"] = "Digital"
        bit = (input_byte >> 4) & 0x07
        interface = input_byte & 0x0F

        bits = ["Undefined", "6", "8", "10", "12", "14", "16", "Reserved"]
        interfaces = ["Undefined", "DVI", "HDMIa", "HDMIb", "MDDI", "DisplayPort"]

        result["bits"] = bits[bit]
        result["interface"] = interfaces[interface] if interface < len(interfaces) else "Reserved or Unknown"
    else:
        result["signal_type"] = "Analog"
        level = (input_byte >> 5) & 0x03
        setup = (input_byte >> 4) & 0x01
        sync = input_byte & 0x0F

        video_levels = [
            "0.700, 0.300 (1.0 V p-p)",
            "0.714, 0.286 (1.0 V p-p)",
            "1.000, 0.286 (1.0 V p-p)",
            "0.700, 0.000 (0.7 V p-p)",
        ]
        result["level"] = video_levels[level]
        result["setup"] = (
            "Blank-to-Black setup or pedestal" if setup else "Blank level = Black level"
        )

        result["sync_separate"] = bool(sync & 0x08)
        result["sync_composite"] = bool(sync & 0x04)
        result["sync_on_green"] = bool(sync & 0x02)

    return result

def parse_display_gamma(edid: bytes) -> list[tuple[str, str]]:
    gamma_encoded = edid[23]
    gamma = (gamma_encoded + 100) / 100.0
    return [(f"Display Gamma: {gamma:.2f}", "guidef")]

def parse_supported_features(edid: bytes) -> list[tuple[str, str]]:
    features = edid[24]
    input_type = edid[20]
    power = (features >> 5) & 0x03

    result = [("Supported Features:", "guidef")]

    if power & 0x04:
        result.append((" - Standby Supported", "guidef"))
    if features & 0x02:
        result.append((" - Suspend Supported", "guidef"))
    if features & 0x01:
        result.append((" - Active-Off Supported", "guidef"))

    display_type = (features >> 3) & 0x03

    display_types_digital = [
        "RGB 4:4:4",
        "RGB 4:4:4 & YCrCb 4:4:4",
        "RGB 4:4:4 & YCrCb 4:2:2",
        "RGB 4:4:4 & YCrCb 4:4:4 & YCrCb 4:2:2"
    ]
    display_types_analog = [
        "Monochrome or Grayscale",
        "RGB Color",
        "Non-RGB Color",
        "Undefined"
    ]

    if input_type & 0x80:
        display = display_types_digital[display_type]
    else:
        display = display_types_analog[display_type]

    result.append((f" - Display Type: {display}", "guidef"))

    if features & 0x04:
        result.append((" - sRGB Color Space Default", "guidef"))
    if features & 0x02:
        result.append((" - Preferred Timing Mode", "guidef"))
    if features & 0x01:
        result.append((" - Continuous Timing Support", "guidef"))

    return result

def parse_colour_characteristics(edid: bytes) -> dict[str, float]:
    red_green_lo = edid[25]
    blue_white_lo = edid[26]

    red_x = (edid[27] << 2) | ((red_green_lo >> 6) & 0x03)
    red_y = (edid[28] << 2) | ((red_green_lo >> 4) & 0x03)
    green_x = (edid[29] << 2) | ((red_green_lo >> 2) & 0x03)
    green_y = (edid[30] << 2) | (red_green_lo & 0x03)

    blue_x = (edid[31] << 2) | ((blue_white_lo >> 6) & 0x03)
    blue_y = (edid[32] << 2) | ((blue_white_lo >> 4) & 0x03)
    white_x = (edid[33] << 2) | ((blue_white_lo >> 2) & 0x03)
    white_y = (edid[34] << 2) | (blue_white_lo & 0x03)

    return {
        "red_x": red_x / 1024,
        "red_y": red_y / 1024,
        "green_x": green_x / 1024,
        "green_y": green_y / 1024,
        "blue_x": blue_x / 1024,
        "blue_y": blue_y / 1024,
        "white_x": white_x / 1024,
        "white_y": white_y / 1024,
    }

def parse_established_timings(edid: bytes) -> tuple[list[bool], int]:
    byte35 = edid[35]
    byte36 = edid[36]
    byte37 = edid[37]
    byte38 = edid[38]  # Manufacturer timings byte

    flags = [
        bool(byte35 & 0x80),  # 720x400 @ 70Hz
        bool(byte35 & 0x40),  # 720x400 @ 88Hz
        bool(byte35 & 0x20),  # 640x480 @ 60Hz
        bool(byte35 & 0x10),  # 640x480 @ 67Hz
        bool(byte35 & 0x08),  # 640x480 @ 72Hz
        bool(byte35 & 0x04),  # 640x480 @ 75Hz
        bool(byte35 & 0x02),  # 800x600 @ 56Hz
        bool(byte35 & 0x01),  # 800x600 @ 60Hz
        bool(byte36 & 0x80),  # 800x600 @ 72Hz
        bool(byte36 & 0x40),  # 800x600 @ 75Hz
        bool(byte36 & 0x20),  # 832x624 @ 75Hz
        bool(byte36 & 0x10),  # 1024x768 @ 87Hz interlaced
        bool(byte36 & 0x08),  # 1024x768 @ 60Hz
        bool(byte36 & 0x04),  # 1024x768 @ 70Hz
        bool(byte36 & 0x02),  # 1024x768 @ 75Hz
        bool(byte36 & 0x01),  # 1280x1024 @ 75Hz
        bool(byte37 & 0x80),  # 1152x870 @ 75Hz
    ]

    return flags, byte37


def parse_standard_timings(edid: bytes) -> list[str]:
    output = []

    aspect_ratios = ["16:10", "4:3", "5:4", "16:9"]

    for i in range(8):
        byte1 = edid[38 + i * 2]
        byte2 = edid[39 + i * 2]

        if byte1 == 0x01 and byte2 == 0x01:
            continue

        horizontal_resolution = (byte1 + 31) * 8
        aspect = (byte2 >> 6) & 0x03
        vertical_frequency = (byte2 & 0x3F) + 60

        if aspect == 0:
            vertical_resolution = horizontal_resolution * 10 // 16  # 16:10
        elif aspect == 1:
            vertical_resolution = horizontal_resolution * 3 // 4     # 4:3
        elif aspect == 2:
            vertical_resolution = horizontal_resolution * 4 // 5     # 5:4
        elif aspect == 3:
            vertical_resolution = horizontal_resolution * 9 // 16    # 16:9
        else:
            vertical_resolution = 0 

        label = f"{horizontal_resolution} x {vertical_resolution} ({aspect_ratios[aspect]}) @ {vertical_frequency}Hz"
        output.append(label)

    return output

def verify_edid_checksum(edid: bytes) -> bool:
    return sum(edid) % 256 == 0





