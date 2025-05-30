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

print("Manufacturer ID Encoding:")
print("DEL ", encode_manufacturer_id("DEL"))

print("\nProduct ID Encoding:")
print("17017 ", encode_product_id(17017))

print("\nSerial Number Encoding:")
print("1113212748 ->", encode_serial_number(1113212748))

print("\nManufacture Date Encoding:")
print("Week 1, Year 1990 ->", encode_manufacture_date(15, 2024))

print("\nVersion: ")
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

print("\nGamma")
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

print("\nColour")
hex_string = encode_colour_characteristics(
    red_x=0.6787, red_y=0.3134,
    green_x=0.2685, green_y=0.6787,
    blue_x=0.1445, blue_y=0.0595,
    white_x=0.3134, white_y=0.3291
)
print(hex_string)

print("\nEstablished")
hex_string = encode_established_timings([
    "720x400 @ 70Hz", "640x480 @ 60Hz", "640x480 @ 75Hz", "800x600 @ 60Hz",
    "800x600 @ 75Hz", "1024x768 @ 60Hz", "1024x768 @ 75Hz", "1280x1024 @ 75Hz"
])
print(hex_string)

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