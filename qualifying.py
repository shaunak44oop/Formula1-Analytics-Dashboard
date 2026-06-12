import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import pandas as pd


def qualifying_report(year, gp):
    # 1. Load Session
    session = fastf1.get_session(year, gp, "Q")
    session.load()

    # Enable F1 team color schemes
    fastf1.plotting.setup_mpl(misc_mpl_mods=False, color_scheme=None)

    # 2. Extract Fastest Laps
    drivers = pd.unique(session.laps['Driver'])
    list_fastest_laps = list()

    for drv in drivers:
        drvs_fastest_lap = session.laps.pick_driver(drv).pick_fastest()
        list_fastest_laps.append(drvs_fastest_lap)

    # Group and sort the laps
    fastest_laps = fastf1.core.Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)

    # Drop drivers who didn't set a valid time (e.g., DNS or crashed)
    fastest_laps = fastest_laps.dropna(subset=['LapTime'])

    # The pole lap is now guaranteed to be the first one
    pole_lap = fastest_laps.pick_fastest()

    # 3. Calculate Gap to Pole
    fastest_laps['Gap'] = (fastest_laps['LapTime'] - pole_lap['LapTime']).dt.total_seconds()

    # 4. Create the Plot
    fig, ax = plt.subplots(figsize=(12, 8))

    # Iterate through to plot each driver with their team color
    for index, lap in fastest_laps.iterlaps():
        driver = lap['Driver']
        gap = lap['Gap']

        try:
            color = fastf1.plotting.get_driver_color(driver, session)
        except:
            color = "gray"  # Fallback

        # Plot horizontal bar
        ax.barh(driver, gap, color=color, edgecolor='black', height=0.7)

        # Add the text label for the gap directly onto the plot
        if gap == 0:
            ax.text(0.05, index, "POLE", va='center', ha='left', color='white', fontweight='bold', fontsize=10)
        else:
            ax.text(gap + 0.05, index, f"+{gap:.3f}s", va='center', ha='left', fontsize=10)

    # 5. Formatting and Cleanup
    ax.set_title(f"{year} {gp} Grand Prix\nQualifying Gap to Pole", fontsize=16, fontweight='bold')
    ax.set_xlabel("Gap to Pole (Seconds)", fontsize=12)
    ax.invert_yaxis()  # Puts the fastest driver at the top
    ax.grid(axis='x', linestyle='--', alpha=0.6)

    # Remove outer borders for a modern web look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.tight_layout()
    #plt.savefig("qualifying_gap.png", dpi=300)
    output_path = os.path.join(output_dir, "qualifying_gap.png")
    plt.savefig(output_path, dpi=300)
    return output_path
    plt.close()


# For testing locally
if __name__ == "__main__":
    qualifying_report(2025, "Canada")