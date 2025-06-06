import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import re

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
    )

from utils import(
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

class EDIDEditorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("EDID Editor")
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Fields
        self.header_var = tk.StringVar()
        self.manufacturer_id_var = tk.StringVar()
        self.product_id_var = tk.IntVar()
        self.serial_number_var = tk.IntVar()
        self.week_var = tk.IntVar()
        self.year_var = tk.IntVar()
        self.version_var = tk.IntVar()
        self.revision_var = tk.IntVar()
        self.horizontal_var = tk.IntVar()
        self.vertical_var = tk.IntVar()
        self.gamma_var = tk.DoubleVar()
        self.redx_var = tk.DoubleVar()
        self.redy_var = tk.DoubleVar()
        self.greenx_var = tk.DoubleVar()
        self.greeny_var = tk.DoubleVar()
        self.bluex_var = tk.DoubleVar()
        self.bluey_var = tk.DoubleVar()
        self.whitex_var = tk.DoubleVar()
        self.whitey_var = tk.DoubleVar()
        self.manfacturer_timings_byte = tk.IntVar()

        
        #subtitle_label = tk.Label(self.root, text="Field Inputs", font=("Helvetica", 12, "bold"))
        #subtitle_label.pack(pady=5)        
        self.current_file_path = None
                
        self.outer_boxes = []
        box_titles = ["Manufacture Details", "Video Input", "Display Details","Colour Characteristics", 
                      "Timing Info", "Checksum", "Output"]
        for i in range(5):
            box = ttk.Frame(main_frame, padding=8, borderwidth=0, relief="flat")
            box.grid(row=0, column=i, padx=5, pady=5, sticky='n')
            self.outer_boxes.append(box)

        self.inner_boxes = []
        
        #manufacture details

        self.header_var = tk.StringVar()

        manufacture_box = ttk.LabelFrame(self.outer_boxes[0], text="Manufacture Details", padding=5, borderwidth=5)
        manufacture_box.pack(fill="both", expand=True, pady=5)
        self.inner_boxes.append(manufacture_box)

        ttk.Label(manufacture_box, text="Manufacturer ID:").grid(row=0, column=0, sticky='e')
        ttk.Entry(manufacture_box, textvariable=self.manufacturer_id_var, width=15).grid(row=0, column=1, pady=5)

        ttk.Label(manufacture_box, text="Product ID:").grid(row=1, column=0, sticky='e')
        ttk.Entry(manufacture_box, textvariable=self.product_id_var, width=15).grid(row=1, column=1, pady=5)

        ttk.Label(manufacture_box, text="Serial Number:").grid(row=2, column=0, sticky='e')
        ttk.Entry(manufacture_box, textvariable=self.serial_number_var, width=15).grid(row=2, column=1, pady=5)

        ttk.Label(manufacture_box, text="Manufacture Week:").grid(row=3, column=0, sticky='e')
        ttk.Entry(manufacture_box, textvariable=self.week_var, width=15).grid(row=3, column=1, pady=5)

        ttk.Label(manufacture_box, text="Manufacture Year:").grid(row=4, column=0, sticky='e')
        ttk.Entry(manufacture_box, textvariable=self.year_var, width=15).grid(row=4, column=1, pady=5)

        ttk.Label(manufacture_box, text="Version:").grid(row=5, column=0, sticky='e')
        ttk.Entry(manufacture_box, textvariable=self.version_var, width=15).grid(row=5, column=1, pady=5)

        ttk.Label(manufacture_box, text="Revision:").grid(row=6, column=0, sticky='e')
        ttk.Entry(manufacture_box, textvariable=self.revision_var, width=15).grid(row=6, column=1, pady=5)

        #video input

        video_box = ttk.LabelFrame(self.outer_boxes[0], text="Video Input", padding=5)
        video_box.pack(fill="both", expand=True, pady=5)
        self.inner_boxes.append(video_box)

        self.signal_type_var = tk.StringVar(value="Digital")
        self.signal_type_var.trace_add("write", self.update_video_input_state)

        digital_rb = tk.Radiobutton(video_box, text="Digital", variable=self.signal_type_var, value="Digital")
        digital_rb.pack(anchor='w') 
        
        bits_frame = ttk.Frame(video_box)
        bits_frame.pack(anchor='w', pady=5)
        ttk.Label(bits_frame, text="Bits per colour: ").grid(row=0, column=0, padx=(0, 5))

        self.bits_var = tk.StringVar()
        self.bits_combo = ttk.Combobox(bits_frame, textvariable=self.bits_var, width=15, state="readonly")
        self.bits_combo['values'] = ("Undefined", "6", "8", "10", "12", "14", "16", "Reserved")
        self.bits_combo.current(0)
        self.bits_combo.grid(row=0, column=1)
        
        interface_frame = ttk.Frame(video_box)
        interface_frame.pack(anchor='w', pady=5)
        ttk.Label(interface_frame, text="Interface: ").grid(row=0, column=0, padx=(0, 5))

        self.interface_var = tk.StringVar()
        self.interface_combo = ttk.Combobox(interface_frame, textvariable=self.interface_var, state="readonly")
        self.interface_combo['values'] = ("Undefined", "DVI", "HDMIa", "HDMIb", "MDDI", "DisplayPort")
        self.interface_combo.current(0)
        self.interface_combo.grid(row=0, column=1)

        analog_rb = tk.Radiobutton(video_box, text="Analog", variable=self.signal_type_var, value="Analog")
        analog_rb.pack(anchor='w')
        chosen = self.signal_type_var.get()
        
        level_frame = ttk.Frame(video_box)
        level_frame.pack(anchor='w', pady=5)
        ttk.Label(level_frame, text="Signal Level: ").grid(row=0, column=0, padx=(0, 5))

        self.level_var = tk.StringVar()
        self.level_combo = ttk.Combobox(level_frame, textvariable=self.level_var, width=15, state="readonly")
        self.level_combo['values'] = ("0.700, 0.300 (1.0 V p-p)", "0.714, 0.286 (1.0 V p-p)", "1.000, 0.286 (1.0 V p-p)",
            "0.700, 0.000 (0.7 V p-p)")
        self.level_combo.current(0)
        self.level_combo.grid(row=0, column=1)
        
        setup_frame = ttk.Frame(video_box)
        setup_frame.pack(anchor='w', pady=5)
        ttk.Label(setup_frame, text="Video Setup: ").grid(row=0, column=0, padx=(0, 5))

        self.setup_var = tk.StringVar()
        self.setup_combo = ttk.Combobox(setup_frame, textvariable=self.setup_var, width=15, state="readonly")
        self.setup_combo['values'] = ("Blank-to-Black setup or pedestal", "Blank level = Black level")
        self.setup_combo.current(0)
        self.setup_combo.grid(row=0, column=1)
        
        checklist_sync_frame = ttk.LabelFrame(video_box, text="Sync Types Supported", padding=10)
        checklist_sync_frame.pack(padx=10, pady=10, anchor='w')

        sync_options = ["Separate", "Composite", "Composite on Green", "Serration"]
        self.self_check_vars = []
        self.sync_checks =[]
        

        for i, option in enumerate(sync_options):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(checklist_sync_frame, text=option, variable=var)
            chk.grid(row=i, column=0, sticky="w", pady=2)
            self.self_check_vars.append(var)
            self.sync_checks.append(chk)
        
        #display
        
        display_box = ttk.LabelFrame(self.outer_boxes[1], text="Display Details", padding=5)
        display_box.pack(fill="both", expand=True, pady=5)
        self.inner_boxes.append(display_box)
        
        ttk.Label(display_box, text="Screen size (horizontal):").grid(row=0, column=0, sticky='e')
        ttk.Entry(display_box, textvariable=self.horizontal_var, width=10).grid(row=0, column=1, pady=5)
        
        ttk.Label(display_box, text="Screen size (vertical):").grid(row=1, column=0, sticky='e')
        ttk.Entry(display_box, textvariable=self.vertical_var, width=10).grid(row=1, column=1, pady=5)
        
        ttk.Label(display_box, text="Display Gamma: ").grid(row=2, column=0, sticky='e')
        ttk.Entry(display_box, textvariable=self.gamma_var, width=10).grid(row=2, column=1, pady=5)
        
        #supported features
        
        supported_box = ttk.LabelFrame(self.outer_boxes[1], text="Supported Features", padding=5)
        supported_box.pack(fill="both", expand=True, pady=5)
        self.inner_boxes.append(supported_box)
        
        checklist_support_frame = ttk.LabelFrame(supported_box, text="Sync Types Supported", padding=10)
        checklist_support_frame.pack(padx=10, pady=10, anchor='w')

        options_support = ["Standby", "Suspend", "Active-off", "sRGB", "Preferred Timing", "Continuous Timing"]
        self.self_support_vars = []

        for i, option in enumerate(options_support):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(checklist_support_frame, text=option, variable=var)
            chk.grid(row=i, column=0, sticky="w", pady=2)
            self.self_support_vars.append(var)
            
        digital_rb = tk.Radiobutton(supported_box, text="Digital", variable=self.signal_type_var, value="Digital", command=self.update_video_input_state)
        digital_rb.pack(anchor='w')
        
        display_d_frame = ttk.Frame(supported_box)
        display_d_frame.pack(anchor='w', pady=5)
        ttk.Label(display_d_frame, text="Display Types: ").grid(row=0, column=0, padx=(0, 5))

        self.display_d_var = tk.StringVar()
        self.display_d_combo = ttk.Combobox(display_d_frame, textvariable=self.display_d_var, width=15, state="readonly")
        self.display_d_combo['values'] = ("RGB 4:4:4", "RGB 4:4:4 & YCrCb 4:4:4", "RGB 4:4:4 & YCrCb 4:2:2", "RGB 4:4:4 & YCrCb 4:4:4 & YCrCb 4:2:2")
        self.display_d_combo.current(0)
        self.display_d_combo.grid(row=0, column=1)
        
        analog_rb = tk.Radiobutton(supported_box, text="Analog", variable=self.signal_type_var, value="Analog", command=self.update_video_input_state)
        analog_rb.pack(anchor='w')
        chosen = self.signal_type_var.get()
        
        display_frame = ttk.Frame(supported_box)
        display_frame.pack(anchor='w', pady=5)
        ttk.Label(display_frame, text="Display Types: ").grid(row=0, column=0, padx=(0, 5))

        self.display_var = tk.StringVar()
        self.display_a_combo = ttk.Combobox(display_frame, textvariable=self.display_var, width=15, state="readonly")
        self.display_a_combo['values'] = ("Monochrome or Grayscale", "RGB Color", "Non-RGB Color", "Undefined")
        self.display_a_combo.current(0)
        self.display_a_combo.grid(row=0, column=1)
        
        if self.signal_type_var.get() == "Digital":
            display_options = ("RGB 4:4:4", "RGB 4:4:4 & YCrCb 4:4:4", "RGB 4:4:4 & YCrCb 4:2:2", "RGB 4:4:4 & YCrCb 4:4:4 & YCrCb 4:2:2")
            selected_display = self.display_d_var.get()
        else:
            display_options = ("Monochrome or Grayscale", "RGB Color", "Non-RGB Color", "Undefined")
            selected_display = self.display_var.get()

        try:
            self.display_type_index = display_options.index(selected_display)
        except ValueError:
            self.display_type_index = 0
        
        #colour
        
        colour_box = ttk.LabelFrame(self.outer_boxes[1], text="Colour Characteristics", padding=5)
        colour_box.pack(fill="both", expand=True, pady=5)
        self.inner_boxes.append(colour_box)

        ttk.Label(colour_box, text="Red: ").grid(row=0, column=0, sticky='e')
        ttk.Label(colour_box, text="x ").grid(row=0, column=1, sticky='e')
        ttk.Entry(colour_box, textvariable=self.redx_var, width=10).grid(row=0, column=2, pady=5)
        ttk.Label(colour_box, text="y ").grid(row=0, column=3, sticky='e')
        ttk.Entry(colour_box, textvariable=self.redy_var, width=10).grid(row=0, column=4)
        
        ttk.Label(colour_box, text="Green: ").grid(row=1, column=0, sticky='e')
        ttk.Label(colour_box, text="x ").grid(row=1, column=1, sticky='e')
        ttk.Entry(colour_box, textvariable=self.greenx_var, width=10).grid(row=1, column=2, pady=5)
        ttk.Label(colour_box, text="y ").grid(row=1, column=3, sticky='e')
        ttk.Entry(colour_box, textvariable=self.greeny_var, width=10).grid(row=1, column=4)
        
        ttk.Label(colour_box, text="Blue: ").grid(row=2, column=0, sticky='e')
        ttk.Label(colour_box, text="x ").grid(row=2, column=1, sticky='e')
        ttk.Entry(colour_box, textvariable=self.bluex_var, width=10).grid(row=2, column=2, pady=5)
        ttk.Label(colour_box, text="y ").grid(row=2, column=3, sticky='e')
        ttk.Entry(colour_box, textvariable=self.bluey_var, width=10).grid(row=2, column=4)
        
        ttk.Label(colour_box, text="White: ").grid(row=3, column=0, sticky='e')
        ttk.Label(colour_box, text="x ").grid(row=3, column=1, sticky='e')
        ttk.Entry(colour_box, textvariable=self.whitex_var, width=10).grid(row=3, column=2, pady=5)
        ttk.Label(colour_box, text="y ").grid(row=3, column=3, sticky='e')
        ttk.Entry(colour_box, textvariable=self.whitey_var, width=10).grid(row=3, column=4)
        
        #timings
        
        established_box = ttk.LabelFrame(self.outer_boxes[2], text="Established Timings", padding=5)
        established_box.pack(fill="both", expand=True, pady=5)
        self.inner_boxes.append(established_box)
        
        checklist_established_frame = ttk.LabelFrame(established_box, padding=10)
        checklist_established_frame.pack(padx=10, pady=10, anchor='w')

        self.options_established = ["720x400 @ 70Hz", "720x400 @ 88Hz", "640x480 @ 60Hz", "640x480 @ 67Hz", "640x480 @ 72Hz", "640x480 @ 75Hz", "800x600 @ 56Hz", "800x600 @ 60Hz",
        "800x600 @ 72Hz", "800x600 @ 75Hz", "832x624 @ 75Hz", "1024x768 @ 87Hz (interlaced)", "1024x768 @ 60Hz", "1024x768 @ 70Hz", "1024x768 @ 75Hz", "1280x1024 @ 75Hz"]
        self.established_vars = []

        for i, option in enumerate(self.options_established):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(checklist_established_frame, text=option, variable=var)
            chk.grid(row=i, column=0, sticky="w", pady=2)
            self.established_vars.append(var)
                    
        manu_timings_box = ttk.LabelFrame(self.outer_boxes[2], text="Manufacturer Timings", padding=5)
        manu_timings_box.pack(fill="both", expand=True, pady=5)
        self.inner_boxes.append(manu_timings_box)

        checklist_manu_frame = ttk.LabelFrame(manu_timings_box, padding=10)
        checklist_manu_frame.pack(padx=10, pady=10, anchor='w')

        self.options_manu = ["1152x870 @ 75Hz"]
        self.manu_vars = []

        for i, option in enumerate(self.options_manu):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(checklist_manu_frame, text=option, variable=var)
            chk.grid(row=i, column=0, sticky="w", pady=2)
            self.manu_vars.append(var)
        
        standard_box = ttk.LabelFrame(self.outer_boxes[3], text="Standard Timings", padding=5)
        standard_box.pack(fill="both", expand=True, pady=5)
        self.inner_boxes.append(standard_box)
        
        checklist_standard_frame = ttk.LabelFrame(standard_box, padding=10)
        checklist_standard_frame.pack(padx=10, pady=10, anchor='w')

        self.options_standard = [
        "640 x 480 (4:3) @ 60Hz", "640 x 480 (4:3) @ 72Hz", "640 x 480 (4:3) @ 75Hz", "640 x 480 (4:3) @ 85Hz",
        "720 x 400 (16:10) @ 70Hz", "800 x 600 (4:3) @ 56Hz", "800 x 600 (4:3) @ 60Hz", "800 x 600 (4:3) @ 72Hz", "800 x 600 (4:3) @ 75Hz", "800 x 600 (4:3) @ 85Hz",
        "832 x 624 (4:3) @ 75Hz", "1024 x 768 (4:3) @ 60Hz", "1024 x 768 (4:3) @ 70Hz", "1024 x 768 (4:3) @ 75Hz", "1024 x 768 (4:3) @ 85Hz",
        "1152 x 864 (4:3) @ 75Hz", "1280 x 720 (16:9) @ 60Hz", "1280 x 720 (16:9) @ 75Hz", "1280 x 768 (15:9) @ 60Hz", "1280 x 768 (15:9) @ 75Hz",
        "1280 x 800 (16:10) @ 60Hz", "1280 x 800 (16:10) @ 75Hz", "1280 x 960 (4:3) @ 60Hz", "1280 x 960 (4:3) @ 85Hz", "1280 x 1024 (5:4) @ 60Hz", "1280 x 1024 (5:4) @ 75Hz", "1280 x 1024 (5:4) @ 85Hz",
        "1360 x 768 (16:9) @ 60Hz", "1366 x 768 (16:9) @ 60Hz", "1440 x 900 (16:10) @ 60Hz", "1440 x 900 (16:10) @ 75Hz", "1600 x 900 (16:9) @ 60Hz", "1600 x 900 (16:9) @ 75Hz",
        "1600 x 1200 (4:3) @ 60Hz", "1600 x 1200 (4:3) @ 75Hz", "1680 x 1050 (16:10) @ 60Hz", "1680 x 1050 (16:10) @ 75Hz", "1920 x 1080 (16:9) @ 60Hz", "1920 x 1080 (16:9) @ 75Hz",
        "1920 x 1200 (16:10) @ 60Hz", "2048 x 1152 (16:9) @ 60Hz", "2048 x 1536 (4:3) @ 60Hz"]
        self.standard_vars = []
        
        mid_index = len(self.options_standard) // 2
        options_col1 = self.options_standard[:mid_index]
        options_col2 = self.options_standard[mid_index:]

        for i, option in enumerate(options_col1):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(checklist_standard_frame, text=option, variable=var)
            chk.grid(row=i, column=0, sticky="w", pady=2)
            self.standard_vars.append(var)
            
        for i, option in enumerate(options_col2):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(checklist_standard_frame, text=option, variable=var)
            chk.grid(row=i, column=1, sticky="w", padx=(20, 0), pady=2)  # optional left padding for spacing
            self.standard_vars.append(var)

        self.checksum_var = tk.StringVar()

        text_frame = ttk.Frame(self.outer_boxes[4], padding=5)
        text_frame.pack(fill='both', expand=True)

        self.output_text = tk.Text(text_frame, height=30, width=35, wrap='word')
        self.output_text.pack(fill='both', expand=True)
        
        button_frame = ttk.Frame(self.outer_boxes[4], padding=10)
        button_frame.pack()

        ttk.Button(button_frame, text="Generate EDID", command=self.on_generate_button_click).pack()
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")

        status_bar = ttk.Label(self.outer_boxes[4], textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(side="bottom", fill="x")

        self.create_menu()
        self.update_video_input_state()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open File", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_edid)
        file_menu.add_command(label="Save as", command=self.save_edid_as)
        file_menu.add_command(label="Help", command=self.not_implemented)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)
        
    def display_edid(self, edid: bytes):
        """
        Display the EDID hex dump in the GUI's output area.
        """
        lines = []
        for i in range(0, len(edid), 16):
            chunk = edid[i:i+16]
            hex_chunk = ' '.join(f"{byte:02X}" for byte in chunk)
            lines.append(hex_chunk)
        hex_dump = '\n'.join(lines)

        self.output_text.configure(state='normal')
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, hex_dump)
        self.output_text.configure(state='disabled')

        
    def load_edid_fields(self, edid_data: bytes):
        is_valid = check_header(edid_data)
        self.header_var.set("Valid" if is_valid else "Invalid")

        if not is_valid:
            messagebox.showerror("Invalid EDID", "Your EDID is invalid and cannot be loaded.")
            return
        
        """is_checksum_valid = verify_edid_checksum(edid_data)
        self.checksum_var.set("Valid" if is_checksum_valid else "Invalid")

        if not is_checksum_valid:
            messagebox.showerror("Invalid Checksum", "Your EDID checksum is invalid and cannot be loaded.")
            return"""
        self.detailed_bytes = edid_data[54:]
        
        self.manufacturer_id_var.set(parse_manufacturer_id(edid_data))
        self.product_id_var.set(str(parse_product_code(edid_data)))
        self.serial_number_var.set(str(parse_serial_number(edid_data)))
        self.week_var.set(parse_week(edid_data))
        self.year_var.set(parse_year(edid_data))
        self.version_var.set(parse_edid_version(edid_data))
        self.revision_var.set(parse_edid_revision(edid_data))
        data = parse_video_input(edid_data)

        self.signal_type_var.set(data["signal_type"])

        if data["signal_type"] == "Digital":
            self.bits_var.set(data["bits"])
            self.interface_var.set(data["interface"])
        else:
            self.level_var.set(data["level"])
            self.setup_var.set(data["setup"])
            self.sync_checks[0].state(['!disabled', 'selected' if data.get("sync_separate") else '!selected'])
            self.sync_checks[1].state(['!disabled', 'selected' if data.get("sync_composite") else '!selected'])
            self.sync_checks[2].state(['!disabled', 'selected' if data.get("sync_on_green") else '!selected'])  
        
        screen_info = parse_screen_size(edid_data)
        if screen_info:
            text, _ = screen_info[0]
            parts = text.split(":")[1].strip().split(" x ")
            self.horizontal_var.set(parts[0].replace(" cm", ""))
            self.vertical_var.set(parts[1].replace(" cm", ""))

        gamma_info = parse_display_gamma(edid_data)
        if gamma_info:
            gamma_text, _ = gamma_info[0]
            gamma_value = gamma_text.split(":")[1].strip()
            self.gamma_var.set(gamma_value)
        
        features = parse_supported_features(edid_data)

        support_flags = {
            "Standby": False, "Suspend": False, "Active-off": False, "sRGB": False, "Preferred Timing": False, "Continuous Timing": False}

        for line, _ in features:
            if "Standby Supported" in line:
                support_flags["Standby"] = True
            elif "Suspend Supported" in line:
                support_flags["Suspend"] = True
            elif "Active-Off Supported" in line:
                support_flags["Active-off"] = True
            elif "sRGB" in line:
                support_flags["sRGB"] = True
            elif "Preferred Timing" in line:
                support_flags["Preferred Timing"] = True
            elif "Continuous Timing" in line:
                support_flags["Continuous Timing"] = True
            elif "Display Type:" in line:
                clean_line = line.lstrip("- ").strip()
                display_type = clean_line.split(":", 1)[1].strip()
                digital_types = self.display_d_combo['values']
                analog_types = self.display_a_combo['values']
                
                if display_type in digital_types:
                    self.signal_type_var.set("Digital")
                    self.update_video_input_state()
                    self.display_d_combo.set(display_type)
                elif display_type in analog_types:
                    self.signal_type_var.set("Analog")
                    self.update_video_input_state()
                    self.display_a_combo.set(display_type)
                else:
                    self.signal_type_var.set("Digital")
                    self.update_video_input_state()
                    if display_type in digital_types:
                        self.display_d_combo.set(display_type)
                    else:
                        self.signal_type_var.set("Digital")
                        self.update_video_input_state()
                        self.display_d_combo.set(digital_types[0])

        for i, option in enumerate(support_flags):
            self.self_support_vars[i].set(support_flags[option])
            
        colour_values = parse_colour_characteristics(edid_data)

        self.redx_var.set(f"{colour_values['red_x']:.4f}")
        self.redy_var.set(f"{colour_values['red_y']:.4f}")
        self.greenx_var.set(f"{colour_values['green_x']:.4f}")
        self.greeny_var.set(f"{colour_values['green_y']:.4f}")
        self.bluex_var.set(f"{colour_values['blue_x']:.4f}")
        self.bluey_var.set(f"{colour_values['blue_y']:.4f}")
        self.whitex_var.set(f"{colour_values['white_x']:.4f}")
        self.whitey_var.set(f"{colour_values['white_y']:.4f}")
        
        timing_flags, manufacturer_timings = parse_established_timings(edid_data)
        self.manu_vars[0].set(bool(manufacturer_timings & 0x80))

        for i in range(min(len(self.established_vars), len(timing_flags))):
            self.established_vars[i].set(timing_flags[i])
            
        parsed_timings = parse_standard_timings(edid_data)

        for var in self.standard_vars:
            var.set(False)

        for i, option in enumerate(self.options_standard):
            if option in parsed_timings:
                self.standard_vars[i].set(True)

        self.update_video_input_state()

        
    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("EDID binary", "*.bin")])
        if not path:
            return

        with open(path, "rb") as f:
            self.edid_data = f.read()

        self.display_edid(self.edid_data)
        self.load_edid_fields(self.edid_data)
        self.status_var.set(f"Opened file")
        self.current_file_path = path
        self.original_edid_bytes = self.edid_data


    def save_edid(self):
        if self.current_file_path:
            try:
                if hasattr(self, 'last_edid') and self.last_edid is not None:
                    data_to_save = self.last_edid
                elif hasattr(self, 'original_edid_bytes') and self.original_edid_bytes is not None:
                    data_to_save = self.original_edid_bytes
                else:
                    raise ValueError("No EDID data to save.")

                with open(self.current_file_path, 'wb') as f:
                    f.write(data_to_save)

                self.status_var.set(f"Saved to {self.current_file_path}")
            except Exception as e:
                self.status_var.set(f"Error saving: {e}")
        else:
            self.save_edid_as()

            
    def save_edid_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".bin",
            filetypes=[("Binary files", "*.bin"), ("All files", "*.*")]
        )
        if file_path:
            try:
                if hasattr(self, 'last_edid') and self.last_edid is not None:
                    data_to_save = self.last_edid
                elif hasattr(self, 'original_edid_bytes') and self.original_edid_bytes is not None:
                    data_to_save = self.original_edid_bytes
                else:
                    raise ValueError("No EDID data to save.")                
                with open(file_path, 'wb') as f:
                    f.write(data_to_save)
                self.current_file_path = file_path
                self.status_var.set(f"Saved as {file_path}")
            except Exception as e:
                self.status_var.set(f"Error saving: {e}")
                
    def get_edid_binary_data(self):
        hex_str = self.output_text.get("1.0", tk.END).strip()
    
        hex_str = hex_str.replace("\n", " ").replace("\r", " ")
    
        hex_bytes = hex_str.split()
    
        try:
            binary_data = bytes(int(b, 16) for b in hex_bytes)
            return binary_data
        except ValueError:
            messagebox.showerror("Error", "Invalid hex format in output.")
            return None

            
    def not_implemented(self):
        messagebox.showinfo("Coming Soon", "This feature is not implemented yet.")
        
    def update_video_input_state(self, *args):
        signal_type = self.signal_type_var.get()

        if signal_type == "Digital":
            self.bits_combo.config(state="readonly")
            self.interface_combo.config(state="readonly")
            self.display_d_combo.config(state="readonly")
            self.level_combo.config(state="disabled")
            self.setup_combo.config(state="disabled")
            self.display_a_combo.config(state="disabled")
            for chk in self.sync_checks:
                chk.config(state="disabled")
        else:
            self.bits_combo.config(state="disabled")
            self.interface_combo.config(state="disabled")
            self.display_d_combo.config(state="disabled")
            self.level_combo.config(state="readonly")
            self.setup_combo.config(state="readonly")
            self.display_a_combo.config(state="readonly")
            for chk in self.sync_checks:
                chk.config(state="normal")
                
    def on_generate_button_click(self):
        try:
            self.selected_timings = [label for var, label in zip(self.established_vars, self.options_established) if var.get()]
            self.manufacturer_timings_byte = 0x80 if self.manu_vars[0].get() else 0x00
            timings_standard = self.get_standard_timings_list()
            edid_hex = generate_all(
                self.manufacturer_id_var.get(),
                int(self.product_id_var.get()),
                int(self.serial_number_var.get()),
                int(self.week_var.get()),
                int(self.year_var.get()),
                int(self.version_var.get()),
                int(self.revision_var.get()),
                self.signal_type_var.get(),
                self.bits_var.get(),
                self.interface_var.get(),
                self.level_var.get(),
                self.setup_var.get(),
                self.self_check_vars[0].get(),
                self.self_check_vars[1].get(),
                self.self_check_vars[2].get(),
                self.self_check_vars[3].get(),
                int(self.horizontal_var.get()),
                int(self.vertical_var.get()),
                float(self.gamma_var.get()),
                self.self_support_vars[0].get(),
                self.self_support_vars[1].get(),
                self.self_support_vars[2].get(),
                self.display_type_index,
                self.self_support_vars[3].get(),
                self.self_support_vars[4].get(),
                self.self_support_vars[5].get(),
                self.signal_type_var.get(),
                self.redx_var.get(), self.redy_var.get(),
                self.greenx_var.get(), self.greeny_var.get(),
                self.bluex_var.get(), self.bluey_var.get(),
                self.whitex_var.get(), self.whitey_var.get(),
                self.selected_timings,
                self.manufacturer_timings_byte,
                timings_standard
            )
            
            edid_bytes = bytearray.fromhex(edid_hex.replace(" ", ""))

            if hasattr(self, "detailed_bytes"):
                edid_bytes += self.detailed_bytes
            else:
                edid_bytes += bytes([0] * 74)  # 18*4 + 2

            lines = [" ".join(f"{b:02X}" for b in edid_bytes[i:i+16]) for i in range(0, len(edid_bytes), 16)]
            final_output = "\n".join(lines)
            
            self.last_edid = edid_bytes

            self.output_text.configure(state='normal')
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, final_output)
            self.output_text.configure(state='disabled')
            print("Generated: ", edid_hex)
            self.status_var.set(f"EDID Generated! ")

        except Exception as e:
            messagebox.showerror("Encoding Error", str(e))
            
    def get_standard_timings_list(self):
        standard_timings_list = []
        for i, var in enumerate(self.standard_vars):
            if var.get():
                label = self.options_standard[i]
                match = re.match(r"(\d+)\s*x\s*(\d+)\s*\(([\d:]+)\)\s*@\s*(\d+)Hz", label)
                if match:
                    width = int(match.group(1))
                    aspect_ratio = match.group(3)
                    refresh_rate = int(match.group(4))
                    standard_timings_list.append((width, aspect_ratio, refresh_rate))
        return standard_timings_list



if __name__ == "__main__":
    root = tk.Tk()
    app = EDIDEditorGUI(root)
    root.mainloop()

