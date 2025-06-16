import argparse
import sys

from parser import(
    check_header,
    parse_manufacturer_id,
    parse_week,
    parse_year,
    parse_edid_all
    )

from cli_utils import (
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
    #add arguments
    parser = argparse.ArgumentParser(description="EDID Tool: Generate, Edit, or Parse EDID files.")
    parser.add_argument("mode", choices=["parse", "edit", "gen"], nargs='?', help="Operation mode: parse/edit/gen")
    parser.add_argument("-read", help="Input EDID binary file (required for parse/edit)")
    parser.add_argument("-write", help="Output EDID binary file (required for gen/edit)")
    parser.add_argument("-v", action="store_true", help="Verbose output: print final EDID data")

    parser.add_argument("--manufacturer", type=manufacturer_id_type)
    parser.add_argument("--product", type=int)
    parser.add_argument("--serial", type=int)
    parser.add_argument("--week", type=int)
    parser.add_argument("--year", type=int)
    parser.add_argument("--version", type=int)
    parser.add_argument("--revision", type=int)
    parser.add_argument("--input_type", choices=["Digital", "Analog"])
    parser.add_argument("--bits_per_color", default="Undefined")
    parser.add_argument("--interface", default="Undefined")
    parser.add_argument("--signal_level", default="0.700, 0.300 (1.0 V p-p)")
    parser.add_argument("--setup", action="store_true")
    parser.add_argument("--sync_hv", action="store_true")
    parser.add_argument("--sync_comp", action="store_true")
    parser.add_argument("--sync_green", action="store_true")
    parser.add_argument("--sync_serration", action="store_true")
    parser.add_argument("--horizontal", type=int)
    parser.add_argument("--vertical", type=int)
    parser.add_argument("--gamma", type=float)
    parser.add_argument("--standby", action="store_true")
    parser.add_argument("--suspend", action="store_true")
    parser.add_argument("--active_off", action="store_true")
    parser.add_argument("--display_type", type=int, choices=range(4))
    parser.add_argument("--srgb", action="store_true")
    parser.add_argument("--preferred_timing", action="store_true")
    parser.add_argument("--continuous_timing", action="store_true")
    parser.add_argument("--digital", action="store_true")
    parser.add_argument("--red_x", type=float)
    parser.add_argument("--red_y", type=float)
    parser.add_argument("--green_x", type=float)
    parser.add_argument("--green_y", type=float)
    parser.add_argument("--blue_x", type=float)
    parser.add_argument("--blue_y", type=float)
    parser.add_argument("--white_x", type=float)
    parser.add_argument("--white_y", type=float)
    parser.add_argument("--selected_timings", nargs="*", default=[])
    parser.add_argument("--manufacturer_byte", type=lambda x: int(x, 0))
    parser.add_argument("--standard_timings", nargs="+", metavar="TIMING", help="Standard timings in format HRES:ASPECT:VREF (e.g. 1280:16:10:60)")

    return parser

def convert_standard_timing_args(arg_list):
    timings = []
    for s in arg_list:
        try:
            parts = s.strip().split(":")
            if len(parts) != 4:
                raise ValueError
            hres = int(parts[0])
            aspect = f"{parts[1]}:{parts[2]}"
            refresh = int(parts[3])
            timings.append((hres, aspect, refresh))
        except ValueError:
            print(f"Error: Invalid standard timing format: {s}")
            print("Expected format: HRES:ASPECT_W:ASPECT_H:VREF (e.g., 1280:16:10:60)")
            sys.exit(1)
    return timings

def manufacturer_id_type(value):
    value = value.upper()
    if len(value) != 3 or not value.isalpha():
        raise argparse.ArgumentTypeError("Manufacturer ID must be 3 alphabetic characters.")
    return value

VALID_ASPECTS = { "16, 10", "4, 3", "5, 4", "16, 9",}

def is_valid_standard_timing(hres: int, aspect: str, refresh: int) -> bool:
    valid_timings = {
    (640, "4:3", 60), (640, "4:3", 72), (640, "4:3", 75), (640, "4:3", 85),
    (720, "16:10", 70),
    (800, "4:3", 56), (800, "4:3", 60), (800, "4:3", 72), (800, "4:3", 75), (800, "4:3", 85),
    (832, "4:3", 75),
    (1024, "4:3", 60), (1024, "4:3", 70), (1024, "4:3", 75), (1024, "4:3", 85),
    (1152, "4:3", 75),
    (1280, "16:9", 60), (1280, "16:9", 75),
    (1280, "15:9", 60), (1280, "15:9", 75),
    (1280, "16:10", 60), (1280, "16:10", 75),
    (1280, "4:3", 60), (1280, "4:3", 85),
    (1280, "5:4", 60), (1280, "5:4", 75), (1280, "5:4", 85),
    (1360, "16:9", 60), (1366, "16:9", 60),
    (1440, "16:10", 60), (1440, "16:10", 75),
    (1600, "16:9", 60), (1600, "16:9", 75),
    (1600, "4:3", 60), (1600, "4:3", 75),
    (1680, "16:10", 60), (1680, "16:10", 75),
    (1920, "16:9", 60), (1920, "16:9", 75),
    (1920, "16:10", 60),
    (2048, "16:9", 60), (2048, "4:3", 60)
    }
    return (hres, aspect, refresh) in valid_timings


def main():
    # displays the gui when there aren't any arguments
    if len(sys.argv) == 1:
        import gui
        gui.run_gui()
        return

    try:
        parser = build_cli_parser()
        args = parser.parse_args()
    except SystemExit as e:
        print("Error: Invalid Arguments")
        sys.exit(e.code)

# parse mode
    if args.mode == "parse":
        if not args.read:
            print("Error: -read is required for parse mode.")
            return
        try:
            with open(args.read, "rb") as f:
                edid = bytearray(f.read())
        except FileNotFoundError:
            print(f"Error: File not found: {args.read}")
            sys.exit(1)
           
#checks for invalid files 
        is_valid = check_header(edid)
        if not is_valid:
            print(f"Invalid EDID. Your EDID is invalid and cannot be loaded.")
            sys.exit(1)
            
        if len(edid) < 128 or len(edid) % 128 != 0:
            print(f"Error: EDID size must be 128 bytes. Got {len(edid)} bytes.")
            sys.exit(1)
            
        manu = parse_manufacturer_id(edid)
        if len(manu) != 3 or not manu.isalpha():
            print(f"Invalid Manufacturer ID. Your EDID cannot be loaded")
            sys.exit(1)
        
        mweek = parse_week(edid)
        if mweek < 0 or mweek > 53:
            print(f"Invalid manufacture week")
            sys.exit(1)
        
        myear = parse_year(edid)
        if myear < 1990 or myear > 2100:
            print(f"Invalid manufacture year")
            sys.exit(1)
            
        parsed_output = parse_edid_all(edid)
        print(parsed_output)

#generating mode
    elif args.mode == "gen":
        required_fields = ["manufacturer", "product", "serial", "week", "year", "version", "revision",
                       "input_type", "horizontal", "vertical", "gamma", "display_type",
                       "red_x", "red_y", "green_x", "green_y", "blue_x", "blue_y", "white_x", "white_y"]

        missing = [field for field in required_fields if getattr(args, field) is None]
        if missing:
            print(f"Error: Missing required fields for generation: {', '.join(missing)}")
            sys.exit(1)
        if not args.write:
            print("Error: -write is required for gen mode.")
            sys.exit(1)
            
        VALID_ESTABLISHED_TIMINGS = {
            "720x400@70Hz", "720x400@88Hz", "640x480@60Hz", "640x480@67Hz",
            "640x480@72Hz", "640x480@75Hz", "800x600@56Hz", "800x600@60Hz",
            "800x600@72Hz", "800x600@75Hz", "832x624@75Hz", "1024x768@87Hz (interlaced)",
            "1024x768@60Hz", "1024x768@70Hz", "1024x768@75Hz", "1280x1024@75Hz"
        }
        normalized_timings = [t.replace(" ", "") for t in args.selected_timings]
        invalid = [t for t in normalized_timings if t not in VALID_ESTABLISHED_TIMINGS]
        if invalid:
            print("Error: Invalid established timing(s):")
            for t in invalid:
                print(f"  - {t}")
            print("\nValid options are:")
            for t in sorted(VALID_ESTABLISHED_TIMINGS):
                print(f"  - {t}")
            sys.exit(1)
        
        standard_timings = convert_standard_timing_args(args.standard_timings) if args.standard_timings else []
        for hres, aspect, refresh in standard_timings:
            if not is_valid_standard_timing(hres, aspect, refresh):
                print(f"Invalid standard timing: {hres}:{aspect} @ {refresh}Hz")
                sys.exit(1)

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
            standard_timings
        )

        with open(args.write, "wb") as f:
            f.write(bytes.fromhex(edid.replace(" ", "")))
        if args.v:
            print("Generated EDID:\n", edid)

    elif args.mode == "edit":
        if not args.read or not args.write:
            print("Error: -read and -write are required for edit mode.")
            sys.exit(1)
            
        if not any(vars(args)[k] is not None for k in vars(args) if k not in ["command", "read", "write", "v"]):
            print("Error: No fields provided to edit.")
            sys.exit(1)

        with open(args.read, "rb") as f:
            edid = bytearray(f.read())

        if args.manufacturer: encode_manufacturer_id(edid, args.manufacturer)
        if args.product is not None: encode_product_id(edid, args.product)
        if args.serial is not None: encode_serial_number(edid, args.serial)
        if args.week is not None and args.year is not None:
            encode_manufacture_date(edid, args.week, args.year)
        if args.version is not None and args.revision is not None:
            encode_edid_version(edid, args.version, args.revision)
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
        
        VALID_ESTABLISHED_TIMINGS = {
            "720x400@70Hz", "720x400@88Hz", "640x480@60Hz", "640x480@67Hz",
            "640x480@72Hz", "640x480@75Hz", "800x600@56Hz", "800x600@60Hz",
            "800x600@72Hz", "800x600@75Hz", "832x624@75Hz", "1024x768@87Hz (interlaced)",
            "1024x768@60Hz", "1024x768@70Hz", "1024x768@75Hz", "1280x1024@75Hz"
        }

        if args.selected_timings:
            # make sure the established timings are of the options
            normalized_timings = [t.replace(" ", "") for t in args.selected_timings]
            invalid = [t for t in normalized_timings if t not in VALID_ESTABLISHED_TIMINGS]
            if invalid:
                print("Error: Invalid established timing(s):")
                for t in invalid:
                    print(f"  - {t}")
                print("\nValid options are:")
                for t in sorted(VALID_ESTABLISHED_TIMINGS):
                    print(f"  - {t}")
                sys.exit(1)
            
            encode_established_timings(edid, normalized_timings, args.manufacturer_byte)
            
        if args.standard_timings:
            # make sure the standard timings are in the correct format and one of the options
            timings = convert_standard_timing_args(args.standard_timings)
            for hres, aspect, refresh in timings:
                if not is_valid_standard_timing(hres, aspect, refresh):
                    print(f"Invalid standard timing: {hres}:{aspect}@{refresh}Hz")
                    sys.exit(1)
            
            encode_standard_timings(edid, timings)

        with open(args.write, "wb") as f:
            f.write(edid)
        if args.v:
            print("Modified EDID:\n", edid.hex(" ", 1))

if __name__ == "__main__":
    main()
