import tkinter as tk
from tkinter import messagebox, filedialog, ttk

class EDIDEditorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("EDID Editor")
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Fields
        self.header_var = tk.StringVar()
        self.manufacturer_id_var = tk.StringVar()
        self.product_id_var = tk.StringVar()
        self.serial_number_var = tk.StringVar()
        self.week_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.version_var = tk.StringVar()
        self.revision_var = tk.StringVar()
        self.display_var = tk.StringVar()
        self.horizontal_var = tk.StringVar()
        self.vertical_var = tk.StringVar()
        self.gamma_var = tk.StringVar()
        self.redx_var = tk.StringVar()
        self.redy_var = tk.StringVar()
        self.greenx_var = tk.StringVar()
        self.greeny_var = tk.StringVar()
        self.bluex_var = tk.StringVar()
        self.bluey_var = tk.StringVar()
        self.whitex_var = tk.StringVar()
        self.whitey_var = tk.StringVar()
        
        #subtitle_label = tk.Label(self.root, text="Field Inputs", font=("Helvetica", 12, "bold"))
        #subtitle_label.pack(pady=5)
        
        self.outer_boxes = []
        box_titles = ["Manufacture Details", "Video Input", "Display Details","Colour Characteristics", 
                      "Timing Info", "Checksum", "Output"]
        for i in range(5):
            box = ttk.LabelFrame(main_frame, padding=10)
            box.grid(row=0, column=i, padx=5, pady=5, sticky='n')
            self.outer_boxes.append(box)

        self.inner_boxes = []
        
        #manufacture details
        header_box = ttk.LabelFrame(self.outer_boxes[0], padding=1)
        header_box.pack(fill="both", expand=True, pady=2)
        self.inner_boxes.append(header_box)
        
        header_frame = ttk.Frame(header_box)
        header_frame.pack(anchor='w', pady=5)
        ttk.Label(header_frame, text="Header: ").grid(row=0, column=0, padx=(0, 5))

        self.bits_var = tk.StringVar()
        header_combo = ttk.Combobox(header_frame, textvariable=self.header_var, width=15, state="readonly")
        header_combo['values'] = ("Standard", "Invalid")
        header_combo.current(0)
        header_combo.grid(row=0, column=1)

        manufacture_box = ttk.LabelFrame(self.outer_boxes[0], text="Manufacture Details", padding=5)
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

        digital_rb = tk.Radiobutton(video_box, text="Digital", variable=self.signal_type_var, value="Digital")
        digital_rb.pack(anchor='w')  # align left
        
        bits_frame = ttk.Frame(video_box)
        bits_frame.pack(anchor='w', pady=5)
        ttk.Label(bits_frame, text="Bits per colour: ").grid(row=0, column=0, padx=(0, 5))

        self.bits_var = tk.StringVar()
        bits_combo = ttk.Combobox(bits_frame, textvariable=self.bits_var, width=15, state="readonly")
        bits_combo['values'] = ("Undefined", "6", "8", "10", "12", "14", "16", "Reserved")
        bits_combo.current(0)
        bits_combo.grid(row=0, column=1)
        
        interface_frame = ttk.Frame(video_box)
        interface_frame.pack(anchor='w', pady=5)
        ttk.Label(interface_frame, text="Interface: ").grid(row=0, column=0, padx=(0, 5))

        self.interface_var = tk.StringVar()
        interface_combo = ttk.Combobox(interface_frame, textvariable=self.interface_var, state="readonly")
        interface_combo['values'] = ("Undefined", "DVI", "HDMIa", "HDMIb", "MDDI", "DisplayPort")
        interface_combo.current(0)
        interface_combo.grid(row=0, column=1)

        analog_rb = tk.Radiobutton(video_box, text="Analog", variable=self.signal_type_var, value="Analog")
        analog_rb.pack(anchor='w')
        chosen = self.signal_type_var.get()
        
        level_frame = ttk.Frame(video_box)
        level_frame.pack(anchor='w', pady=5)
        ttk.Label(level_frame, text="Signal Level: ").grid(row=0, column=0, padx=(0, 5))

        self.level_var = tk.StringVar()
        level_combo = ttk.Combobox(level_frame, textvariable=self.level_var, width=15, state="readonly")
        level_combo['values'] = ("0.700, 0.300 (1.0 V p-p)", "0.714, 0.286 (1.0 V p-p)", "1.000, 0.286 (1.0 V p-p)",
            "0.700, 0.000 (0.7 V p-p)")
        level_combo.current(0)
        level_combo.grid(row=0, column=1)
        
        setup_frame = ttk.Frame(video_box)
        setup_frame.pack(anchor='w', pady=5)
        ttk.Label(setup_frame, text="Video Setup: ").grid(row=0, column=0, padx=(0, 5))

        self.setup_var = tk.StringVar()
        setup_combo = ttk.Combobox(setup_frame, textvariable=self.setup_var, width=15, state="readonly")
        setup_combo['values'] = ("Blank-to-Black setup or pedestal", "Blank level = Black level")
        setup_combo.current(0)
        setup_combo.grid(row=0, column=1)
        
        checklist_sync_frame = ttk.LabelFrame(video_box, text="Sync Types Supported", padding=10)
        checklist_sync_frame.pack(padx=10, pady=10, anchor='w')

        sync_options = ["Separate", "Composite", "Composite on Green"]
        self_check_vars = []

        for i, option in enumerate(sync_options):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(checklist_sync_frame, text=option, variable=var)
            chk.grid(row=i, column=0, sticky="w", pady=2)
            self_check_vars.append(var)
        
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
        
        supported_box = ttk.LabelFrame(self.outer_boxes[1], text="Supported Features", padding=5)
        supported_box.pack(fill="both", expand=True, pady=5)
        self.inner_boxes.append(supported_box)
        
        checklist_support_frame = ttk.LabelFrame(supported_box, text="Sync Types Supported", padding=10)
        checklist_support_frame.pack(padx=10, pady=10, anchor='w')

        options_support = ["Standby", "Suspend", "Active-off", "sRBG", "Preferred Timing", "Continuous Timing"]
        self_support_vars = []

        for i, option in enumerate(options_support):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(checklist_support_frame, text=option, variable=var)
            chk.grid(row=i, column=0, sticky="w", pady=2)
            self_support_vars.append(var)
            
        digital_rb = tk.Radiobutton(supported_box, text="Digital", variable=self.signal_type_var, value="Digital")
        digital_rb.pack(anchor='w')
        
        display_frame = ttk.Frame(supported_box)
        display_frame.pack(anchor='w', pady=5)
        ttk.Label(display_frame, text="Display Types: ").grid(row=0, column=0, padx=(0, 5))

        self.display_var = tk.StringVar()
        display_combo = ttk.Combobox(display_frame, textvariable=self.display_var, width=15, state="readonly")
        display_combo['values'] = ("RGB 4:4:4", "RGB 4:4:4 & YCrCb 4:4:4", "RGB 4:4:4 & YCrCb 4:2:2", "RGB 4:4:4 & YCrCb 4:4:4 & YCrCb 4:2:2")
        display_combo.current(0)
        display_combo.grid(row=0, column=1)
        
        analog_rb = tk.Radiobutton(supported_box, text="Analog", variable=self.signal_type_var, value="Analog")
        analog_rb.pack(anchor='w')
        chosen = self.signal_type_var.get()
        
        display_frame = ttk.Frame(supported_box)
        display_frame.pack(anchor='w', pady=5)
        ttk.Label(display_frame, text="Display Types: ").grid(row=0, column=0, padx=(0, 5))

        self.display_var = tk.StringVar()
        display_combo = ttk.Combobox(display_frame, textvariable=self.display_var, width=15, state="readonly")
        display_combo['values'] = ("Monochrome or Grayscale", "RGB Color", "Non-RGB Color", "Undefined")
        display_combo.current(0)
        display_combo.grid(row=0, column=1)
        
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

        options_established = ["720x400 @ 70Hz", "720x400 @ 88Hz", "640x480 @ 60Hz", "640x480 @ 67Hz", "640x480 @ 72Hz", "640x480 @ 75Hz", "800x600 @ 56Hz", "800x600 @ 60Hz",
        "800x600 @ 72Hz", "800x600 @ 75Hz", "832x624 @ 75Hz", "1024x768 @ 87Hz (interlaced)", "1024x768 @ 60Hz", "1024x768 @ 70Hz", "1024x768 @ 75Hz", "1280x1024 @ 75Hz"]
        self_established_vars = []

        for i, option in enumerate(options_established):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(checklist_established_frame, text=option, variable=var)
            chk.grid(row=i, column=0, sticky="w", pady=2)
            self_established_vars.append(var)
        
        standard_box = ttk.LabelFrame(self.outer_boxes[3], text="Standard Timings", padding=5)
        standard_box.pack(fill="both", expand=True, pady=5)
        self.inner_boxes.append(standard_box)
        
        checklist_standard_frame = ttk.LabelFrame(standard_box, padding=10)
        checklist_standard_frame.pack(padx=10, pady=10, anchor='w')

        options_standard = ["640 x 480 (4:3) @ 60Hz", "640 x 480 (4:3) @ 72Hz","640 x 480 (4:3) @ 75Hz", "800 x 600 (4:3) @ 56Hz",
            "800 x 600 (4:3) @ 60Hz", "800 x 600 (4:3) @ 72Hz", "800 x 600 (4:3) @ 75Hz", "832 x 624 (4:3) @ 75Hz", "1024 x 768 (4:3) @ 60Hz",
            "1024 x 768 (4:3) @ 70Hz", "1024 x 768 (4:3) @ 75Hz", "1280 x 720 (16:9) @ 60Hz", "1280 x 768 (15:9) @ 60Hz", "1280 x 800 (16:10) @ 60Hz", "1280 x 960 (4:3) @ 60Hz",
            "1280 x 960 (4:3) @ 85Hz", "1280 x 1024 (5:4) @ 60Hz", "1280 x 1024 (5:4) @ 75Hz", "1280 x 1024 (5:4) @ 85Hz", "1360 x 768 (16:9) @ 60Hz",
            "1366 x 768 (16:9) @ 60Hz", "1440 x 900 (16:10) @ 60Hz", "1440 x 900 (16:10) @ 75Hz", "1600 x 900 (16:9) @ 60Hz",
            "1600 x 1200 (4:3) @ 60Hz", "1680 x 1050 (16:10) @ 60Hz", "1920 x 1080 (16:9) @ 60Hz", "1920 x 1200 (16:10) @ 60Hz",
            "2048 x 1152 (16:9) @ 60Hz", "2048 x 1536 (4:3) @ 60Hz"]
        self_standard_vars = []
        
        mid_index = len(options_standard) // 2
        options_col1 = options_standard[:mid_index]
        options_col2 = options_standard[mid_index:]

        for i, option in enumerate(options_col1):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(checklist_standard_frame, text=option, variable=var)
            chk.grid(row=i, column=0, sticky="w", pady=2)
            self_standard_vars.append(var)
            
        for i, option in enumerate(options_col2):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(checklist_standard_frame, text=option, variable=var)
            chk.grid(row=i, column=1, sticky="w", padx=(20, 0), pady=2)  # optional left padding for spacing
            self_standard_vars.append(var)
        
        checksum_box = ttk.LabelFrame(self.outer_boxes[3], padding=5)
        checksum_box.pack(fill="both", expand=True, pady=2)
        self.inner_boxes.append(checksum_box)
        
        checksum_frame = ttk.Frame(checksum_box)
        checksum_frame.pack(anchor='w', pady=5)
        ttk.Label(checksum_frame, text="Checksum: ").grid(row=0, column=0, padx=(0, 5))

        self.bits_var = tk.StringVar()
        checksum_combo = ttk.Combobox(checksum_frame, textvariable=self.header_var, width=15, state="readonly")
        checksum_combo['values'] = ("Standard", "Invalid")
        checksum_combo.current(0)
        checksum_combo.grid(row=0, column=1)

        text_frame = ttk.Frame(self.outer_boxes[4], padding=5)
        text_frame.pack(fill='both', expand=True)

        self.output_text = tk.Text(text_frame, height=30, width=35, wrap='word')
        self.output_text.pack(fill='both', expand=True)
        
        button_frame = ttk.Frame(self.outer_boxes[4], padding=10)
        button_frame.pack()

        ttk.Button(button_frame, text="Generate EDID", command=self.not_implemented).pack()
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")

        status_bar = ttk.Label(self.outer_boxes[4], textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(side="bottom", fill="x")

        self.create_menu()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open File", command=self.not_implemented)
        file_menu.add_command(label="Save EDID", command=self.not_implemented)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    def save_edid(self):
        # Placeholder for save functionality
        filename = filedialog.asksaveasfilename(defaultextension=".bin")
        if filename:
            # In full version, generate binary and save
            with open(filename, "wb") as f:
                f.write(b"\x00" * 128)  # placeholder
            messagebox.showinfo("Saved", f"Saved dummy EDID to {filename}")
            
    def not_implemented(self):
        messagebox.showinfo("Coming Soon", "This feature is not implemented yet.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EDIDEditorGUI(root)
    root.mainloop()
