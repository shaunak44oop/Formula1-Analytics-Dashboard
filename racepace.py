import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


def race_pace_report(year, gp, output_dir="."):
    session = fastf1.get_session(year, gp, "R")
    session.load()

    fastf1.plotting.setup_mpl(misc_mpl_mods=False, color_scheme=None)

    laps = session.laps.pick_quicklaps()
    drivers = session.results["Abbreviation"]

    driver_stats = []
    best_mean = float('inf')

    for drv in drivers:
        drv_laps = laps.pick_driver(drv)
        if not drv_laps.empty:
            mean_time = drv_laps["LapTime"].dt.total_seconds().mean()
            driver_stats.append({
                "driver": drv,
                "mean": mean_time,
                "laps": drv_laps
            })
            if mean_time < best_mean:
                best_mean = mean_time

    driver_stats.sort(key=lambda x: x["mean"])

    sorted_drivers = [stat["driver"] for stat in driver_stats]
    data = [stat["laps"]["LapTime"].dt.total_seconds().dropna() for stat in driver_stats]

    labels = []
    for stat in driver_stats:
        mean_str = f"{stat['mean']:.2f}"
        gap = stat["mean"] - best_mean
        gap_str = f"+{gap:.2f}" if gap > 0 else "+0.00"
        labels.append(f"{stat['driver']}\n{mean_str}\n{gap_str}")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12), gridspec_kw={'height_ratios': [1.2, 1]})
    fig.suptitle(f"{year} {gp} Grand Prix\nRace Pace Analysis", fontsize=18, fontweight='bold')

    bplot = ax1.boxplot(
        data,
        tick_labels=labels,
        patch_artist=True,
        showmeans=True,
        meanline=True,
        meanprops={"color": "black", "ls": "--", "lw": 1.5},
        medianprops={"color": "black", "ls": "-", "lw": 1.5},
        flierprops={"marker": "o", "markersize": 4, "alpha": 0.5}
    )

    for patch, driver in zip(bplot['boxes'], sorted_drivers):
        try:
            color = fastf1.plotting.get_driver_color(driver, session)
        except:
            color = "gray"
        patch.set_facecolor(color)
        patch.set_alpha(0.8)

    ax1.set_title("Global Racepace (Sorted by Mean Quick Lap)", fontsize=14)
    ax1.set_ylabel("Lap Time (s)")
    ax1.grid(axis='y', linestyle='--', alpha=0.6)

    # Tracking used colors to differentiate teammates
    used_colors = {}

    for stat in driver_stats:
        drv = stat["driver"]
        drv_laps = stat["laps"].copy().sort_values(by="LapNumber")
        smoothed_times = drv_laps["LapTime"].dt.total_seconds().rolling(window=3, min_periods=1).mean()

        try:
            color = fastf1.plotting.get_driver_color(drv, session)
        except:
            color = "gray"

        # Determine line style based on teammate status
        if color in used_colors:
            linestyle = '--'  # Second teammate gets dashed
        else:
            linestyle = '-'  # First teammate gets solid
            used_colors[color] = drv

        ax2.plot(drv_laps["LapNumber"], smoothed_times, label=drv, color=color, linewidth=2, linestyle=linestyle)

    ax2.set_title("Smoothed Lap-by-Lap Racepace (Teammates Differentiated by Dashed Lines)", fontsize=14)
    ax2.set_xlabel("Lap Number")
    ax2.set_ylabel("Lap Time (s) [3-Lap Rolling Avg]")
    ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=10, frameon=False)
    ax2.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    output_path = os.path.join(output_dir, "advanced_race_pace.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path