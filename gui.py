# # import os
# # import threading
# # import tkinter as tk
# # from tkinter import messagebox, ttk
# # import fastf1
# #
# # # Ensure cache directory exists upfront
# # if not os.path.exists("cache"):
# #     os.makedirs("cache")
# # fastf1.Cache.enable_cache("cache")
# #
# # # Import your upgraded visualization modules
# # from racepace import race_pace_report
# # from qualifying import qualifying_report
# # from telemetry import compare_drivers
# # from trackmap import track_dominance_map
# #
# #
# # class F1AnalyticsApp:
# #
# #     def __init__(self, root):
# #         self.root = root
# #         self.root.title("F1 Blog Analytics Dashboard")
# #         self.root.geometry("450x550")
# #         self.root.resizable(False, False)
# #
# #         # Style configurations
# #         self.style = ttk.Style()
# #         self.style.theme_use("clam")
# #
# #         # Title Label
# #         title_label = ttk.Label(
# #             root, text="🏁 F1 Analytics Asset Generator", font=("Arial", 16, "bold")
# #         )
# #         title_label.pack(pady=15)
# #
# #         # --- INPUT FRAME ---
# #         input_frame = ttk.LabelFrame(root, text=" Session Details ", padding=15)
# #         input_frame.pack(pady=10, padx=20, fill="x")
# #         input_frame.columnconfigure(1, weight=1) # Makes the input column expandable
# #
# #         # Year Input
# #         ttk.Label(input_frame, text="Year:").grid(
# #             row=0, column=0, sticky="w", pady=5
# #         )
# #         self.year_entry = ttk.Entry(input_frame)
# #         self.year_entry.insert(0, "2025")
# #         self.year_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5) # Fixed: sticky="ew"
# #
# #         # Grand Prix Input
# #         ttk.Label(input_frame, text="Grand Prix:").grid(
# #             row=1, column=0, sticky="w", pady=5
# #         )
# #         self.gp_entry = ttk.Entry(input_frame)
# #         self.gp_entry.insert(0, "Canada")
# #         self.gp_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5) # Fixed: sticky="ew"
# #
# #         # --- DRIVER COMPARISON FRAME ---
# #         driver_frame = ttk.LabelFrame(
# #             root, text=" Driver Setup (For Maps & Telemetry) ", padding=15
# #         )
# #         driver_frame.pack(pady=10, padx=20, fill="x")
# #         driver_frame.columnconfigure(1, weight=1) # Makes the input column expandable
# #
# #         # Driver 1
# #         ttk.Label(driver_frame, text="Driver 1 (e.g. VER):").grid(
# #             row=0, column=0, sticky="w", pady=5
# #         )
# #         self.d1_entry = ttk.Entry(driver_frame)
# #         self.d1_entry.insert(0, "VER")
# #         self.d1_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5) # Fixed: sticky="ew"
# #
# #         # Driver 2
# #         ttk.Label(driver_frame, text="Driver 2 (e.g. NOR):").grid(
# #             row=1, column=0, sticky="w", pady=5
# #         )
# #         self.d2_entry = ttk.Entry(driver_frame)
# #         self.d2_entry.insert(0, "NOR")
# #         self.d2_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5) # Fixed: sticky="ew"
# #
# #         # Telemetry Session Type Dropdown
# #         ttk.Label(driver_frame, text="Telemetry Session:").grid(
# #             row=2, column=0, sticky="w", pady=5
# #         )
# #         self.session_type = ttk.Combobox(
# #             driver_frame, values=["Q", "R", "FP1", "FP2", "FP3"], state="readonly"
# #         )
# #         self.session_type.set("Q")
# #         self.session_type.grid(row=2, column=1, sticky="ew", pady=5, padx=5) # Fixed: sticky="ew"
# #
# #         # --- ACTIONS FRAME ---
# #         actions_frame = ttk.LabelFrame(root, text=" Select Analysis Mode ", padding=15)
# #         actions_frame.pack(pady=10, padx=20, fill="x")
# #
# #         # Grid buttons for a clean UI matrix
# #         ttk.Button(
# #             actions_frame,
# #             text="Global Race Pace",
# #             command=lambda: self.run_task("race_pace"),
# #         ).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
# #         ttk.Button(
# #             actions_frame,
# #             text="Qualifying Gap",
# #             command=lambda: self.run_task("qualifying"),
# #         ).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
# #         ttk.Button(
# #             actions_frame,
# #             text="Telemetry Compare",
# #             command=lambda: self.run_task("telemetry"),
# #         ).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
# #         ttk.Button(
# #             actions_frame,
# #             text="Track Dominance Map",
# #             command=lambda: self.run_task("track_map"),
# #         ).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
# #
# #         actions_frame.columnconfigure(0, weight=1)
# #         actions_frame.columnconfigure(1, weight=1)
# #
# #         # Progress / Status indicator
# #         self.status_label = ttk.Label(
# #             root, text="Status: Ready", font=("Arial", 10, "italic"), foreground="blue"
# #         )
# #         self.status_label.pack(pady=10)
# #
# #     def run_task(self, mode):
# #         # We process downloading/rendering in a separate thread so the GUI window doesn't freeze up
# #         threading.Thread(target=self.execute_analysis, args=(mode,), daemon=True).start()
# #
# #     def execute_analysis(self, mode):
# #         try:
# #             year = int(self.year_entry.get())
# #         except ValueError:
# #             messagebox.showerror("Input Error", "Year must be a valid number.")
# #             return
# #
# #         gp = self.gp_entry.get().strip()
# #         d1 = self.d1_entry.get().strip().upper()
# #         d2 = self.d2_entry.get().strip().upper()
# #         sess_type = self.session_type.get()
# #
# #         if not gp:
# #             messagebox.showerror("Input Error", "Grand Prix field cannot be blank.")
# #             return
# #
# #         self.status_label.config(text="Status: Fetching data & generating chart...", foreground="orange")
# #         self.root.update_idletasks()
# #
# #         try:
# #             if mode == "race_pace":
# #                 race_pace_report(year, gp)
# #                 filename = "advanced_race_pace.png"
# #             elif mode == "qualifying":
# #                 qualifying_report(year, gp)
# #                 filename = "qualifying_gap.png"
# #             elif mode == "telemetry":
# #                 compare_drivers(year, gp, sess_type, d1, d2)
# #                 filename = "telemetry_comparison.png"
# #             elif mode == "track_map":
# #                 track_dominance_map(year, gp, d1, d2)
# #                 filename = "track_dominance_map.png"
# #
# #             self.status_label.config(text="Status: Chart Generated Successfully!", foreground="green")
# #             messagebox.showinfo("Success", f"Chart successfully saved as:\n{filename}")
# #
# #         except Exception as e:
# #             self.status_label.config(text="Status: Error encountered", foreground="red")
# #             messagebox.showerror("Engine Error", f"An error occurred:\n{str(e)}")
# #
# #
# # if __name__ == "__main__":
# #     root = tk.Tk()
# #     app = F1AnalyticsApp(root)
# #     root.mainloop()
# import os
# import sys
# import threading
# import tkinter as tk
# from tkinter import messagebox, ttk
# import fastf1
#
# # Ensure cache and clean output folder exist upfront
# OUTPUT_DIR = "F1_Analytics_Plots"
# for folder in ["cache", OUTPUT_DIR]:
#     if not os.path.exists(folder):
#         os.makedirs(folder)
#
# fastf1.Cache.enable_cache("cache")
#
# from racepace import race_pace_report
# from qualifying import qualifying_report
# from telemetry import compare_drivers
# from trackmap import track_dominance_map
#
#
# class F1AnalyticsApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("F1 Blog Analytics Dashboard")
#         self.root.geometry("450x550")
#         self.root.resizable(False, False)
#
#         self.style = ttk.Style()
#         self.style.theme_use("clam")
#
#         title_label = ttk.Label(root, text="🏁 F1 Analytics Asset Generator", font=("Arial", 16, "bold"))
#         title_label.pack(pady=15)
#
#         # --- INPUT FRAME ---
#         input_frame = ttk.LabelFrame(root, text=" Session Details ", padding=15)
#         input_frame.pack(pady=10, padx=20, fill="x")
#         input_frame.columnconfigure(1, weight=1)
#
#         ttk.Label(input_frame, text="Year:").grid(row=0, column=0, sticky="w", pady=5)
#         self.year_entry = ttk.Entry(input_frame)
#         self.year_entry.insert(0, "2025")
#         self.year_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
#
#         ttk.Label(input_frame, text="Grand Prix:").grid(row=1, column=0, sticky="w", pady=5)
#         self.gp_entry = ttk.Entry(input_frame)
#         self.gp_entry.insert(0, "Canada")
#         self.gp_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
#
#         # --- DRIVER COMPARISON FRAME ---
#         driver_frame = ttk.LabelFrame(root, text=" Driver Setup (For Maps & Telemetry) ", padding=15)
#         driver_frame.pack(pady=10, padx=20, fill="x")
#         driver_frame.columnconfigure(1, weight=1)
#
#         ttk.Label(driver_frame, text="Driver 1 (e.g. VER):").grid(row=0, column=0, sticky="w", pady=5)
#         self.d1_entry = ttk.Entry(driver_frame)
#         self.d1_entry.insert(0, "VER")
#         self.d1_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
#
#         ttk.Label(driver_frame, text="Driver 2 (e.g. NOR):").grid(row=1, column=0, sticky="w", pady=5)
#         self.d2_entry = ttk.Entry(driver_frame)
#         self.d2_entry.insert(0, "NOR")
#         self.d2_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
#
#         ttk.Label(driver_frame, text="Telemetry Session:").grid(row=2, column=0, sticky="w", pady=5)
#         self.session_type = ttk.Combobox(driver_frame, values=["Q", "R", "FP1", "FP2", "FP3"], state="readonly")
#         self.session_type.set("Q")
#         self.session_type.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
#
#         # --- ACTIONS FRAME ---
#         actions_frame = ttk.LabelFrame(root, text=" Select Analysis Mode ", padding=15)
#         actions_frame.pack(pady=10, padx=20, fill="x")
#
#         ttk.Button(actions_frame, text="Global Race Pace", command=lambda: self.run_task("race_pace")).grid(row=0,
#                                                                                                             column=0,
#                                                                                                             padx=5,
#                                                                                                             pady=5,
#                                                                                                             sticky="ew")
#         ttk.Button(actions_frame, text="Qualifying Gap", command=lambda: self.run_task("qualifying")).grid(row=0,
#                                                                                                            column=1,
#                                                                                                            padx=5,
#                                                                                                            pady=5,
#                                                                                                            sticky="ew")
#         ttk.Button(actions_frame, text="Telemetry Compare", command=lambda: self.run_task("telemetry")).grid(row=1,
#                                                                                                              column=0,
#                                                                                                              padx=5,
#                                                                                                              pady=5,
#                                                                                                              sticky="ew")
#         ttk.Button(actions_frame, text="Track Dominance Map", command=lambda: self.run_task("track_map")).grid(row=1,
#                                                                                                                column=1,
#                                                                                                                padx=5,
#                                                                                                                pady=5,
#                                                                                                                sticky="ew")
#
#         actions_frame.columnconfigure(0, weight=1)
#         actions_frame.columnconfigure(1, weight=1)
#
#         self.status_label = ttk.Label(root, text="Status: Ready", font=("Arial", 10, "italic"), foreground="blue")
#         self.status_label.pack(pady=10)
#
#     def run_task(self, mode):
#         threading.Thread(target=self.execute_analysis, args=(mode,), daemon=True).start()
#
#     def open_image(self, filepath):
#         """Cross-platform automated system image opening."""
#         try:
#             if sys.platform == "win32":
#                 os.startfile(filepath)
#             elif sys.platform == "darwin":  # macOS
#                 import subprocess
#                 subprocess.call(["open", filepath])
#             else:  # Linux
#                 import subprocess
#                 subprocess.call(["xdg-open", filepath])
#         except Exception as e:
#             print(f"Could not open image file automatically: {e}")
#
#     def execute_analysis(self, mode):
#         try:
#             year = int(self.year_entry.get())
#         except ValueError:
#             messagebox.showerror("Input Error", "Year must be a valid number.")
#             return
#
#         gp = self.gp_entry.get().strip()
#         d1 = self.d1_entry.get().strip().upper()
#         d2 = self.d2_entry.get().strip().upper()
#         sess_type = self.session_type.get()
#
#         if not gp:
#             messagebox.showerror("Input Error", "Grand Prix field cannot be blank.")
#             return
#
#         self.status_label.config(text="Status: Fetching data & generating chart...", foreground="orange")
#         self.root.update_idletasks()
#
#         try:
#             if mode == "race_pace":
#                 filepath = race_pace_report(year, gp, output_dir=OUTPUT_DIR)
#             elif mode == "qualifying":
#                 filepath = qualifying_report(year, gp, output_dir=OUTPUT_DIR)
#             elif mode == "telemetry":
#                 filepath = compare_drivers(year, gp, sess_type, d1, d2, output_dir=OUTPUT_DIR)
#             elif mode == "track_map":
#                 filepath = track_dominance_map(year, gp, d1, d2, output_dir=OUTPUT_DIR)
#
#             self.status_label.config(text="Status: Chart Generated!", foreground="green")
#
#             # Automatically display the file using your default system app
#             self.open_image(filepath)
#
#         except Exception as e:
#             self.status_label.config(text="Status: Error encountered", foreground="red")
#             messagebox.showerror("Engine Error", f"An error occurred:\n{str(e)}")
#
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = F1AnalyticsApp(root)
#     root.mainloop()
import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox, ttk

# --- FIX 1: Force Matplotlib to use a headless background engine ---
# This eliminates the "Starting a Matplotlib GUI outside main thread" warning.
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


class F1AnalyticsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("F1 Blog Analytics Dashboard")
        self.root.geometry("450x550")
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

        actions_frame.columnconfigure(0, weight=1)
        actions_frame.columnconfigure(1, weight=1)

        self.status_label = ttk.Label(root, text="Status: Ready", font=("Arial", 10, "italic"), foreground="blue")
        self.status_label.pack(pady=10)

    # --- FIX 2: Thread-Safe UI Update Helpers ---
    def safe_update_status(self, text, color):
        """Schedules status text modifications cleanly back onto the main GUI thread loop."""
        self.root.after(0, lambda: self.status_label.config(text=text, foreground=color))

    def safe_show_error(self, title, message):
        """Schedules popups safely onto the main thread loop so it never crashes execution."""
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

            self.safe_update_status("Status: Chart Generated!", "green")
            self.open_image(filepath)

        except Exception as e:
            self.safe_update_status("Status: Error encountered", "red")
            self.safe_show_error("Engine Error", f"An error occurred while compiling data:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = F1AnalyticsApp(root)
    root.mainloop()
