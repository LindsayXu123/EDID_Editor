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
    encode_standard_timings,
    generate_all
)

print("Manufacturer ID Encoding:")
print("DEL ", encode_manufacturer_id("DEL"))
print("BNQ ", encode_manufacturer_id("BNQ"))

print("\nProduct ID Encoding:")
print("17017 ", encode_product_id(17017))
print("32805 ", encode_product_id(32805))

print("\nSerial Number Encoding:")
print("1113212748 ->", encode_serial_number(1113212748))
print("21573 ->", encode_serial_number(21573))

print("\nManufacture Date Encoding:")
print("Week 15, Year 2024 ->", encode_manufacture_date(15, 2024))
print("Week 22, Year 2020 ->", encode_manufacture_date(22, 2020))

print("\nVersion: ")
print(encode_edid_version(1, 4))
print(encode_edid_version(1, 4))

print("\nVideo input")
print(build_video_input("Digital", bits_per_color="10", interface="DisplayPort"))  

print(build_video_input(
    "Analog",
    signal_level="0.714, 0.286 (1.0 V p-p)",
    setup=True,
    sync_hv=True,
    sync_comp=True
))

print("\nScreen size")
print(encode_screen_size(60, 34))
print(encode_screen_size(70, 40))

print("\nGamma")
print(encode_display_gamma(2.2))
print(encode_display_gamma(2.2))

print("\nSupported features")
print(encode_supported_features(
    standby=False,
    suspend=True,
    active_off=False,
    display_type=3,
    srgb=False,
    preferred_timing=True,
    continuous_timing=False,
    digital=True
))
print(encode_supported_features(
    standby=False,
    suspend=True,
    active_off=False,
    display_type=3,
    srgb=True,
    preferred_timing=True,
    continuous_timing=False,
    digital=True
)) 

print("\nColour")
hex_string = encode_colour_characteristics(
    red_x=0.6787, red_y=0.3134,
    green_x=0.2685, green_y=0.6787,
    blue_x=0.1445, blue_y=0.0595,
    white_x=0.3134, white_y=0.3291
)
print(hex_string)
hex_string2 = encode_colour_characteristics(
    red_x=0.6582, red_y=0.3320,
    green_x=0.3017, green_y=0.6240,
    blue_x=0.1474, blue_y=0.0556,
    white_x=0.3125, white_y=0.3291
)
print(hex_string2)

print("\nEstablished")
hex_string = encode_established_timings([
    "720x400 @ 70Hz", "640x480 @ 60Hz", "640x480 @ 75Hz", "800x600 @ 60Hz",
    "800x600 @ 75Hz", "1024x768 @ 60Hz", "1024x768 @ 75Hz", "1280x1024 @ 75Hz"
], 0x00)
print(hex_string)
hex_string2 = encode_established_timings([
    "720x400 @ 70Hz", "640x480 @ 60Hz", "640x480 @ 75Hz", "640x480 @ 75Hz", "800x600 @ 60Hz",
    "800x600 @ 75Hz", "832x624 @ 75Hz", "1024x768 @ 60Hz", "1024x768 @ 75Hz", "1280x1024 @ 75Hz"
], 0x80)
print(hex_string2)

print("\nStandard")
example_timings = [
    (1920, "16:10", 60),
    (1920, "16:9", 60),
    (1680, "16:10", 60),
    (1600, "4:3", 60),
    (1280, "5:4", 60),
    (1280, "16:10", 60),
    (1152, "4:3", 75),
    (2048, "16:9", 60)
]
encoded = encode_standard_timings(example_timings)
print(encoded)
example_timings2 = [
    (1280, "5:4", 60),
    (1280, "16:9", 60),
    (1280, "16:10", 60),
    (1600, "16:9", 60),
    (1680, "16:10", 60),
    (1920, "16:9", 60)
]
encoded2 = encode_standard_timings(example_timings2)
print(encoded2)

gen_all = generate_all()