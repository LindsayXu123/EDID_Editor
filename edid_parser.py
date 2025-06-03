EDID_LENGTH = 128  # Typical EDID length
def check_header(edid: bytes) -> bool:
    if (len(edid) < 8 or
        edid[0] != 0x00 or edid[1] != 0xFF or edid[2] != 0xFF or edid[3] != 0xFF or
        edid[4] != 0xFF or edid[5] != 0xFF or edid[6] != 0xFF or edid[7] != 0x00):
        return False 
    return True

def parse_edid_version(edid: bytes, output: list, offset: list):
    version = edid[0x12]  # EDID version byte
    revision = edid[0x13]  # EDID revision byte
    print(f"EDID Version: {version}.{revision}")

    text = f"EDID Version: {version}.{revision}\n"
    output[offset[0]:offset[0]] = [text]
    offset[0] += 1
    
def parse_manufacturer_id(edid: bytes, output: str, offset: list) -> str:
    manufacturer = (edid[8] << 8) | edid[9]

    manufacturer_id = ''.join([
        chr(((manufacturer >> 10) & 0x1F) + ord('A') - 1),
        chr(((manufacturer >> 5) & 0x1F) + ord('A') - 1),
        chr((manufacturer & 0x1F) + ord('A') - 1)
    ])

    print(f"Manufacturer ID: {manufacturer_id}")

    text = f"Manufacturer ID: {manufacturer_id}\n"
    output = output[:offset[0]] + text + output[offset[0]:]
    offset[0] += len(text)

    return output

def parse_product_code(edid: bytes, output: str, offset: list) -> str:
    product_code = edid[10] | (edid[11] << 8)

    print(f"Product Code: {product_code} (0x{product_code:04X})")

    text = f"Product Code: {product_code} (0x{product_code:04X})\n"
    output = output[:offset[0]] + text + output[offset[0]:]
    offset[0] += len(text)

    return output

def parse_serial_number(edid: bytes, output: str, offset: list) -> str:
    serial = (edid[12]
              | (edid[13] << 8)
              | (edid[14] << 16)
              | (edid[15] << 24))

    text = f"Serial Number: {serial} (0x{serial:08X})\n"
    print(text, end="")

    output = output[:offset[0]] + text + output[offset[0]:]
    offset[0] += len(text)

    return output

def parse_manufacture_date(edid: bytes, output: str, offset: list) -> str:
    week = edid[16]
    year_offset = edid[17]
    year = 1990 + year_offset

    text = f"Manufacture Date: Year {year}, Week {week}\n"
    print(text, end="")

    output = output[:offset[0]] + text + output[offset[0]:]
    offset[0] += len(text)

    return output

def parse_video_input(edid: bytes, output: str, offset: list) -> str:
    input_byte = edid[20]

    if input_byte & 0x80:
        print("Video Input Type: Digital")
        text = "Video Input Type: Digital\n"
        output = output[:offset[0]] + text + output[offset[0]:]
        offset[0] += len(text)

        bit = (input_byte >> 4) & 0x07
        interface = input_byte & 0x0F

        bits = ["Undefined", "6", "8", "10", "12", "14", "16", "Reserved"]
        interfaces = ["Undefined", "DVI", "HDMIa", "HDMIb", "MDDI", "DisplayPort"]

        text = f"   Bits per colour: {bits[bit]}\n"
        print(text, end="")
        output = output[:offset[0]] + text + output[offset[0]:]
        offset[0] += len(text)

        if interface < len(interfaces):
            iface_str = interfaces[interface]
        else:
            iface_str = "Reserved or Unknown"

        text = f"   Interface: {iface_str}\n"
        print(text, end="")
        output = output[:offset[0]] + text + output[offset[0]:]
        offset[0] += len(text)

    else:
        print("Video Input Type: Analog")
        text = "Video Input Type: Analog\n"
        output = output[:offset[0]] + text + output[offset[0]:]
        offset[0] += len(text)

        level = (input_byte >> 5) & 0x03
        setup = (input_byte >> 4) & 0x01
        sync = input_byte & 0x0F

        video_levels = [
            "0.700, 0.300 (1.0 V p-p)",
            "0.714, 0.286 (1.0 V p-p)",
            "1.000, 0.286 (1.0 V p-p)",
            "0.700, 0.000 (0.7 V p-p)",
        ]

        text = f"   Signal Level: {video_levels[level]}\n"
        print(text, end="")
        output = output[:offset[0]] + text + output[offset[0]:]
        offset[0] += len(text)

        if setup:
            setup_text = "Video setup: Blank-to-Black setup or pedestal\n"
        else:
            setup_text = "Video setup: Blank level = Black level\n"

        print(setup_text, end="")
        output = output[:offset[0]] + setup_text + output[offset[0]:]
        offset[0] += len(setup_text)

        sync_header = "   Sync Types Supported:\n"
        print(sync_header, end="")
        output = output[:offset[0]] + sync_header + output[offset[0]:]
        offset[0] += len(sync_header)

        if sync & 0x08:
            sync_text = "   -Separate Sync H & V Signals\n"
            print(sync_text, end="")
            output = output[:offset[0]] + sync_text + output[offset[0]:]
            offset[0] += len(sync_text)
        if sync & 0x04:
            sync_text = "   -Composite Sync H & V Signals\n"
            print(sync_text, end="")
            output = output[:offset[0]] + sync_text + output[offset[0]:]
            offset[0] += len(sync_text)
        if sync & 0x02:
            sync_text = "   -Composite Sync Signal on Green Video\n"
            print(sync_text, end="")
            output = output[:offset[0]] + sync_text + output[offset[0]:]
            offset[0] += len(sync_text)
        if sync & 0x01:
            sync_text = "   -Serration on Vertical Sync\n"
            print(sync_text, end="")
            output = output[:offset[0]] + sync_text + output[offset[0]:]
            offset[0] += len(sync_text)

    return output

def parse_screen_size(edid: bytes, output: str, offset: list) -> str:
    horizontal_size = edid[21]
    vertical_size = edid[22]

    text = f"Screen Size: {horizontal_size} cm x {vertical_size} cm\n"
    print(text, end="")
    output = output[:offset[0]] + text + output[offset[0]:]
    offset[0] += len(text)

    return output

def parse_display_gamma(edid: bytes, output: str, offset: list) -> str:
    gamma_encoded = edid[23]
    gamma = (gamma_encoded + 100) / 100.0

    gamma_str = f"{gamma:.2f}"
    print(f"Display Gamma: {gamma_str}")

    text = f"Display Gamma: {gamma_str} \n"
    output = output[:offset[0]] + text + output[offset[0]:]
    offset[0] += len(text)

    return output

def parse_supported_features(edid: bytes, output: str, offset: list) -> str:
    features = edid[24]
    input_type = edid[20]

    power = (features >> 5) & 0x03

    print("Supported Features:")
    text = "Supported Features:\n"
    output = output[:offset[0]] + text + output[offset[0]:]
    offset[0] += len(text)

    if power & 0x04:
        print(" - Standby Supported")
        text = " - Standby Supported\n"
        output = output[:offset[0]] + text + output[offset[0]:]
        offset[0] += len(text)

    if features & 0x02:
        print(" - Suspend Supported")
        text = " - Suspend Supported\n"
        output = output[:offset[0]] + text + output[offset[0]:]
        offset[0] += len(text)

    if features & 0x01:
        print(" - Active-Off Supported")
        text = " - Active-Off Supported\n"
        output = output[:offset[0]] + text + output[offset[0]:]
        offset[0] += len(text)

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

    print(f" - Display Type: {display}")
    text = f" - Display Type: {display}\n"
    output = output[:offset[0]] + text + output[offset[0]:]
    offset[0] += len(text)

    if features & 0x04:
        print(" - sRGB Color Space Default")
        text = " - sRGB Color Space Default\n"
        output = output[:offset[0]] + text + output[offset[0]:]
        offset[0] += len(text)

    if features & 0x02:
        print(" - Preferred Timing Mode")
        text = " - Preferred Timing Mode\n"
        output = output[:offset[0]] + text + output[offset[0]:]
        offset[0] += len(text)

    if features & 0x01:
        print(" - Continuous Timing Support")
        text = " - Continuous Timing Support\n"
        output = output[:offset[0]] + text + output[offset[0]:]
        offset[0] += len(text)

    return output

def parse_colour_characteristics(edid: bytes, output: str, offset: list) -> str:
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

    def float_to_str(val):
        return f"{val:.4f}"

    red_x_f = red_x / 1024.0
    red_y_f = red_y / 1024.0
    green_x_f = green_x / 1024.0
    green_y_f = green_y / 1024.0
    blue_x_f = blue_x / 1024.0
    blue_y_f = blue_y / 1024.0
    white_x_f = white_x / 1024.0
    white_y_f = white_y / 1024.0

    lines = [
        "Color Characteristics (Chromaticity Coordinates):\n",
        f"  Red   : (X = {float_to_str(red_x_f)}, Y = {float_to_str(red_y_f)})\n",
        f"  Green : (X = {float_to_str(green_x_f)}, Y = {float_to_str(green_y_f)})\n",
        f"  Blue  : (X = {float_to_str(blue_x_f)}, Y = {float_to_str(blue_y_f)})\n",
        f"  White : (X = {float_to_str(white_x_f)}, Y = {float_to_str(white_y_f)})\n"
    ]

    for line in lines:
        print(line, end='')
        output = output[:offset[0]] + line + output[offset[0]:]
        offset[0] += len(line)

    return output

def float_to_string(value: float) -> str:
    return f"{int(value)}.{int((value - int(value)) * 10000):04d}"

def verify_edid_checksum(edid: bytes) -> bool:
    return sum(edid) % 256 == 0

def parse_established_timings(edid: bytes) -> str:
    timing1 = edid[35]
    timing2 = edid[36]
    timing3 = edid[37]

    established_timings = [
        "720x400 @ 70Hz", "720x400 @ 88Hz", "640x480 @ 60Hz", "640x480 @ 67Hz",
        "640x480 @ 72Hz", "640x480 @ 75Hz", "800x600 @ 56Hz", "800x600 @ 60Hz",
        "800x600 @ 72Hz", "800x600 @ 75Hz", "832x624 @ 75Hz", "1024x768 @ 87Hz (interlaced)",
        "1024x768 @ 60Hz", "1024x768 @ 70Hz", "1024x768 @ 75Hz", "1280x1024 @ 75Hz"
    ]

    output_lines = ["Established Timings:"]

    mask = 0x80
    for i in range(8):
        if timing1 & mask:
            output_lines.append(f" - {established_timings[i]}")
        mask >>= 1

    mask = 0x80
    for i in range(8):
        if timing2 & mask:
            output_lines.append(f" - {established_timings[8 + i]}")
        mask >>= 1

    if timing3 != 0x00:
        output_lines.append(f" - Manufacturer reserved timings: 0x{timing3:02X}")

    return "\n".join(output_lines) + "\n"

def parse_standard_timings(edid: bytes) -> str:
    output_lines = ["Standard Timings:"]

    aspect_ratios = ["16:10", "4:3", "5:4", "16:9"]

    for i in range(8):
        byte1 = edid[38 + i * 2]
        byte2 = edid[39 + i * 2]

        if byte1 == 0x01 and byte2 == 0x01:
            continue

        horizontal_resolution = (byte1 + 31) * 8
        aspect = (byte2 >> 6) & 0x03
        vertical_frequency = (byte2 & 0x3F) + 60

        if aspect == 0:  # 16:10
            vertical_resolution = horizontal_resolution * 10 // 16
        elif aspect == 1:
            vertical_resolution = horizontal_resolution * 3 // 4
        elif aspect == 2: 
            vertical_resolution = horizontal_resolution * 4 // 5
        elif aspect == 3: 
            vertical_resolution = horizontal_resolution * 9 // 16
        else:
            vertical_resolution = 0

        output_lines.append(f" - {horizontal_resolution} x {vertical_resolution} ({aspect_ratios[aspect]}) @ {vertical_frequency}Hz")

    return "\n".join(output_lines) + "\n"

def parse_edid_array(edid: bytes) -> str:
    output_lines = []

    if not check_header(edid):
        output_lines.append("Invalid EDID header\n")
        return "".join(output_lines)

    output_lines.append("Valid EDID header\n")

    # Each parse_* function is assumed to return a string
    output_lines.append(parse_manufacturer_id(edid))
    output_lines.append(parse_product_code(edid))
    output_lines.append(parse_serial_number(edid))
    output_lines.append(parse_manufacture_date(edid))
    output_lines.append(parse_edid_version(edid))
    output_lines.append(parse_video_input(edid))
    output_lines.append(parse_screen_size(edid))
    output_lines.append(parse_display_gamma(edid))
    output_lines.append(parse_supported_features(edid))
    output_lines.append(parse_colour_characteristics(edid))
    output_lines.append(parse_established_timings(edid))
    output_lines.append(parse_standard_timings(edid))

    if verify_edid_checksum(edid):
        output_lines.append("Checksum is valid\n")
    else:
        output_lines.append("Checksum is invalid\n")

    # Join everything into a single string
    edid_output = "".join(output_lines)

    # Debug print equivalent
    print(edid_output)

    return edid_output

def string_to_hex(hex_string: str) -> bytes:
    edid = bytearray()
    hex_string = hex_string.strip()

    i = 0
    length = len(hex_string)
    while i < length and len(edid) < 128:
        while i < length and hex_string[i].isspace():
            i += 1
        if i >= length:
            break

        if i + 1 < length:
            hex_byte = hex_string[i:i+2]
            try:
                byte = int(hex_byte, 16)
                edid.append(byte)
                i += 2
            except ValueError:
                break
        else:
            break

    return bytes(edid)

def parse_edid_string(hex_string: str) -> str:
    output = []
    
    edid = string_to_hex(hex_string)
    
    if not check_header(edid):
        output.append("Invalid EDID header\n")
        return "".join(output)
    
    output.append("Valid EDID header\n")
    
    parse_manufacturer_id(edid, output)
    parse_product_code(edid, output)
    parse_serial_number(edid, output)
    parse_manufacture_date(edid, output)
    parse_edid_version(edid, output)
    parse_video_input(edid, output)
    parse_screen_size(edid, output)
    parse_display_gamma(edid, output)
    parse_supported_features(edid, output)
    parse_colour_characteristics(edid, output)
    parse_established_timings(edid, output)
    parse_standard_timings(edid, output)

    if verify_edid_checksum(edid):
        output.append("Checksum is valid\n")
    else:
        output.append("Checksum is invalid\n")

    return "".join(output)







