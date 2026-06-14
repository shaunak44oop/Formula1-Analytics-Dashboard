import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib

matplotlib.use('Agg')

import fastf1

# Ensure cache and clean output folder exist upfront
OUTPUT_DIR = "F1_Analytics_Plots"
for folder in ["cache", OUTPUT_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)

fastf1.Cache.enable_cache("cache")

from racepace import race_pace_report
from qualifying import qualifying_report
from telemetry import compare_drivers
from trackmap import track_dominance_map
from topspeed import top_speed_analysis


class F1AnalyticsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("F1 Blog Analytics Dashboard")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        title_label = ttk.Label(root, text="🏁 F1 Analytics Asset Generator", font=("Arial", 16, "bold"))
        title_label.pack(pady=15)

        # --- INPUT FRAME ---
        input_frame = ttk.LabelFrame(root, text=" Session Details ", padding=15)
        input_frame.pack(pady=10, padx=20, fill="x")
        input_frame.columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="Year:").grid(row=0, column=0, sticky="w", pady=5)
        self.year_entry = ttk.Entry(input_frame)
        self.year_entry.insert(0, "2024")
        self.year_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        ttk.Label(input_frame, text="Grand Prix:").grid(row=1, column=0, sticky="w", pady=5)
        self.gp_entry = ttk.Entry(input_frame)
        self.gp_entry.insert(0, "British")
        self.gp_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        # --- DRIVER COMPARISON FRAME ---
        driver_frame = ttk.LabelFrame(root, text=" Driver Setup ", padding=15)
        driver_frame.pack(pady=10, padx=20, fill="x")
        driver_frame.columnconfigure(1, weight=1)

        ttk.Label(driver_frame, text="Driver 1 (e.g. VER):").grid(row=0, column=0, sticky="w", pady=5)
        self.d1_entry = ttk.Entry(driver_frame)
        self.d1_entry.insert(0, "VER")
        self.d1_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        ttk.Label(driver_frame, text="Driver 2 (e.g. NOR):").grid(row=1, column=0, sticky="w", pady=5)
        self.d2_entry = ttk.Entry(driver_frame)
        self.d2_entry.insert(0, "NOR")
        self.d2_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        ttk.Label(driver_frame, text="Telemetry Session:").grid(row=2, column=0, sticky="w", pady=5)
        self.session_type = ttk.Combobox(driver_frame, values=["Q", "R"], state="readonly")
        self.session_type.set("Q")
        self.session_type.grid(row=2, column=1, sticky="ew", pady=5, padx=5)

        # --- ACTIONS FRAME ---
        actions_frame = ttk.LabelFrame(root, text=" Select Analysis Mode ", padding=15)
        actions_frame.pack(pady=10, padx=20, fill="x")

        ttk.Button(actions_frame, text="Global Race Pace", command=lambda: self.run_task("race_pace")).grid(row=0,
                                                                                                            column=0,
                                                                                                            padx=5,
                                                                                                            pady=5,
                                                                                                            sticky="ew")
        ttk.Button(actions_frame, text="Qualifying Gap", command=lambda: self.run_task("qualifying")).grid(row=0,
                                                                                                           column=1,
                                                                                                           padx=5,
                                                                                                           pady=5,
                                                                                                           sticky="ew")
        ttk.Button(actions_frame, text="Telemetry Compare", command=lambda: self.run_task("telemetry")).grid(row=1,
                                                                                                             column=0,
                                                                                                             padx=5,
                                                                                                             pady=5,
                                                                                                             sticky="ew")
        ttk.Button(actions_frame, text="Track Dominance Map", command=lambda: self.run_task("track_map")).grid(row=1,
                                                                                                               column=1,
                                                                                                               padx=5,
                                                                                                               pady=5,
                                                                                                               sticky="ew")

        # <--- NEW TOP SPEED BUTTON (Spans 2 columns) --->
        ttk.Button(actions_frame, text="Top Speed Analysis", command=lambda: self.run_task("top_speed")).grid(row=2,
                                                                                                              column=0,
                                                                                                              columnspan=2,
                                                                                                              padx=5,
                                                                                                              pady=5,
                                                                                                              sticky="ew")

        actions_frame.columnconfigure(0, weight=1)
        actions_frame.columnconfigure(1, weight=1)

        self.status_label = ttk.Label(root, text="Status: Ready", font=("Arial", 10, "italic"), foreground="blue")
        self.status_label.pack(pady=10)

    def safe_update_status(self, text, color):
        self.root.after(0, lambda: self.status_label.config(text=text, foreground=color))

    def safe_show_error(self, title, message):
        self.root.after(0, lambda: messagebox.showerror(title, message))

    def run_task(self, mode):
        threading.Thread(target=self.execute_analysis, args=(mode,), daemon=True).start()

    def open_image(self, filepath):
        if sys.platform == "win32":
            os.startfile(filepath)

    def execute_analysis(self, mode):
        try:
            year = int(self.year_entry.get())
            gp = self.gp_entry.get().strip()

            # Pre-verification test call
            fastf1.get_session(year, gp, 'R')

            d1 = self.d1_entry.get().strip().upper()
            d2 = self.d2_entry.get().strip().upper()
            sess_type = self.session_type.get()

            self.safe_update_status("Status: Fetching verified data...", "orange")

            if mode == "race_pace":
                filepath = race_pace_report(year, gp, output_dir=OUTPUT_DIR)
            elif mode == "qualifying":
                filepath = qualifying_report(year, gp, output_dir=OUTPUT_DIR)
            elif mode == "telemetry":
                filepath = compare_drivers(year, gp, sess_type, d1, d2, output_dir=OUTPUT_DIR)
            elif mode == "track_map":
                filepath = track_dominance_map(year, gp, d1, d2, output_dir=OUTPUT_DIR)
            elif mode == "top_speed":  # <--- NEW EXECUTION ROUTE
                filepath = top_speed_analysis(year, gp, sess_type, output_dir=OUTPUT_DIR)

            self.safe_update_status("Status: Chart Generated!", "green")
            self.open_image(filepath)

        except Exception as e:
            self.safe_update_status("Status: Error encountered", "red")
            self.safe_show_error("Engine Error", f"An error occurred while compiling data:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = F1AnalyticsApp(root)
    root.mainloop()
