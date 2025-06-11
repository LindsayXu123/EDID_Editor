import argparse
import os
import sys
from parser import(
    check_header,
    parse_manufacturer_id,
    parse_product_code,
    parse_serial_number,
    parse_week,
    parse_year,
    parse_edid_version,
    parse_edid_revision,
    parse_video_input,
    parse_screen_size,
    parse_display_gamma,
    parse_supported_features,
    parse_colour_characteristics,
    parse_established_timings,
    parse_standard_timings,
    verify_edid_checksum,
    parse_edid_all
    )

from cli_utils import(
    encode_manufacturer_id,
    encode_product_id,
    encode_serial_number,
    encode_manufacture_date,
    encode_edid_version,
    encode_input_type,
    encode_screen_size,
    encode_display_gamma,
    encode_supported_features,
    encode_colour_characteristics,
    encode_established_timings,
    encode_standard_timings,
    generate_all
)

def build_cli_parser():
    parser = argparse.ArgumentParser(description="EDID Tool: Generate, Parse, or Edit EDID files.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Generate command
    gen = subparsers.add_parser("generate", help="Generate EDID from parameters")
    
    # Shared fields (also used in edit mode)
    for p in (gen,):
        p.add_argument("--manufacturer", help="3-letter manufacturer ID (e.g., DEL)")
        p.add_argument("--product", type=int, help="Product ID (0–65535)")
        p.add_argument("--serial", type=int, help="Serial number (0–4294967295)")
        p.add_argument("--week", type=int, help="Manufacture week (1–53)")
        p.add_argument("--year", type=int, help="Manufacture year (>= 1990)")
        p.add_argument("--version", type=int, help="EDID version")
        p.add_argument("--revision", type=int, help="EDID revision")

        p.add_argument("--input_type", choices=["Digital", "Analog"], help="Input type")
        p.add_argument("--bits_per_color", default="Undefined", help="Bits per color (Digital only)")
        p.add_argument("--interface", default="Undefined", help="Digital interface type")
        p.add_argument("--signal_level", default="0.700, 0.300 (1.0 V p-p)", help="Signal level (Analog only)")
        p.add_argument("--setup", action="store_true", help="Setup expected (Analog only)")
        p.add_argument("--sync_hv", action="store_true")
        p.add_argument("--sync_comp", action="store_true")
        p.add_argument("--sync_green", action="store_true")
        p.add_argument("--sync_serration", action="store_true")

        p.add_argument("--horizontal", type=int, help="Screen width in cm")
        p.add_argument("--vertical", type=int, help="Screen height in cm")
        p.add_argument("--gamma", type=float, help="Display gamma")

        p.add_argument("--standby", action="store_true")
        p.add_argument("--suspend", action="store_true")
        p.add_argument("--active_off", action="store_true")
        p.add_argument("--display_type", type=int, choices=range(4))
        p.add_argument("--srgb", action="store_true")
        p.add_argument("--preferred_timing", action="store_true")
        p.add_argument("--continuous_timing", action="store_true")
        p.add_argument("--digital", action="store_true")

        p.add_argument("--red_x", type=float)
        p.add_argument("--red_y", type=float)
        p.add_argument("--green_x", type=float)
        p.add_argument("--green_y", type=float)
        p.add_argument("--blue_x", type=float)
        p.add_argument("--blue_y", type=float)
        p.add_argument("--white_x", type=float)
        p.add_argument("--white_y", type=float)

        p.add_argument("--selected_timings", nargs="*", default=[], help="List of established timings")
        p.add_argument("--manufacturer_byte", type=lambda x: int(x, 0), help="Manufacturer reserved byte")
        p.add_argument("--standard_timings", nargs=3, action="append")

        p.add_argument("--output", help="Output .bin filename")

    parse = subparsers.add_parser("parse", help="Parse and optionally edit an EDID file")
    parse.add_argument("file", help="Path to EDID .bin file")
    for a in gen._actions:
        if a.dest not in ["help", "output"]:
            parse._add_action(a)
    parse.add_argument("--save", help="Output file to save edited EDID")

    return parser

def main():
    parser = build_cli_parser()
    args = parser.parse_args()

    if args.command == "generate":
        edid = generate_all(
            args.manufacturer, args.product, args.serial,
            args.week, args.year, args.version, args.revision,
            args.input_type, args.bits_per_color, args.interface,
            args.signal_level, args.setup, args.sync_hv,
            args.sync_comp, args.sync_green, args.sync_serration,
            args.horizontal, args.vertical, args.gamma,
            args.standby, args.suspend, args.active_off,
            args.display_type, args.srgb, args.preferred_timing,
            args.continuous_timing, args.digital,
            args.red_x, args.red_y, args.green_x, args.green_y,
            args.blue_x, args.blue_y, args.white_x, args.white_y,
            args.selected_timings, args.manufacturer_byte,
            args.standard_timings
        )
        if args.output:
            with open(args.output, "wb") as f:
                f.write(bytes.fromhex(edid.replace(" ", "")))
        else:
            print(edid)

    elif args.command == "parse":
        with open(args.file, "rb") as f:
            edid = bytearray(f.read())

        print(parse_edid_all(edid))

        if any(vars(args)[k] is not None for k in vars(args) if k not in ["command", "file", "save"]):
            if args.manufacturer: encode_manufacturer_id(edid, args.manufacturer)
            if args.product is not None: encode_product_id(edid, args.product)
            if args.serial is not None: encode_serial_number(edid, args.serial)
            if args.week is not None and args.year is not None: encode_manufacture_date(edid, args.week, args.year)
            if args.version is not None and args.revision is not None: encode_edid_version(edid, args.version, args.revision)
            if args.input_type:
                encode_input_type(edid, args.input_type, args.bits_per_color, args.interface,
                                  args.signal_level, args.setup, args.sync_hv,
                                  args.sync_comp, args.sync_green, args.sync_serration)
            if args.horizontal is not None and args.vertical is not None:
                encode_screen_size(edid, args.horizontal, args.vertical)
            if args.gamma is not None:
                encode_display_gamma(edid, args.gamma)
            if args.display_type is not None:
                encode_supported_features(edid, args)
            if all(v is not None for v in [args.red_x, args.red_y, args.green_x, args.green_y,
                                           args.blue_x, args.blue_y, args.white_x, args.white_y]):
                encode_colour_characteristics(edid, args)
            if args.selected_timings:
                encode_established_timings(edid, args.selected_timings, args.manufacturer_byte)
            if args.standard_timings:
                encode_standard_timings(edid, args.standard_timings)

            if args.save:
                with open(args.save, "wb") as f:
                    f.write(edid)
                print(f"Saved modified EDID to {args.save}")

if __name__ == "__main__":
    main()
