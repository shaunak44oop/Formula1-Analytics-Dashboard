import os
import fastf1

# 1. Handle the cache directory automatically
if not os.path.exists("cache"):
    os.makedirs("cache")

fastf1.Cache.enable_cache("cache")

# 2. Import all your upgraded modules
from racepace import race_pace_report
from qualifying import qualifying_report
from telemetry import compare_drivers
from trackmap import track_dominance_map

# 3. Global parameters for your blog post
YEAR = 2026
GP = "Monaco"
DRIVER_1 = "HAM"
DRIVER_2 = "ANT"

if __name__ == "__main__":
    print("🏎️ Starting F1 Analytics Engine...")

    # Generate the 2-panel Boxplot & Rolling Pace charts
    print("Generating Race Pace Analysis...")
    race_pace_report(YEAR, GP)

    # Generate the horizontal Gap to Pole chart
    print("Generating Qualifying Gap Report...")
    qualifying_report(YEAR, GP)

    # Generate the 3-panel Speed/Throttle/Brake dashboard
    print(f"Generating Telemetry Comparison for {DRIVER_1} vs {DRIVER_2}...")
    compare_drivers(YEAR, GP, "Q", DRIVER_1, DRIVER_2)

    # Generate the spatial mini-sector track dominance map
    print(f"Generating Track Dominance Map for {DRIVER_1} vs {DRIVER_2}...")
    track_dominance_map(YEAR, GP, DRIVER_1, DRIVER_2)

    print("\n🎉 Success! All professional blog assets have been generated:")
    print("📁 advanced_race_pace.png")
    print("📁 qualifying_gap.png")
    print("📁 telemetry_comparison.png")
    print("📁 track_dominance_map.png")