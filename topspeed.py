import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import pandas as pd
import os


def top_speed_analysis(year, gp, session_type, output_dir="."):
    # 1. Load Session
    session = fastf1.get_session(year, gp, session_type)
    session.load()

    # Enable F1 team color schemes
    fastf1.plotting.setup_mpl(misc_mpl_mods=False, color_scheme=None)

    # 2. Extract Max Speeds
    drivers = pd.unique(session.laps['Driver'])
    speed_data = []

    for drv in drivers:
        drv_laps = session.laps.pick_driver(drv)
        if drv_laps.empty:
            continue

        fastest_lap = drv_laps.pick_fastest()
        if pd.isna(fastest_lap['LapTime']):
            continue

        try:
            # Extract telemetry for the fastest lap and find the absolute highest speed recorded
            tel = fastest_lap.get_telemetry()
            max_speed = tel['Speed'].max()

            try:
                color = fastf1.plotting.get_driver_color(drv, session)
            except:
                color = "gray"

            speed_data.append({'Driver': drv, 'TopSpeed': max_speed, 'Color': color})
        except Exception as e:
            print(f"Skipping {drv} due to missing telemetry: {e}")
            continue

    # 3. Sort Data for the Plot
    df = pd.DataFrame(speed_data)
    df = df.sort_values(by='TopSpeed',
                        ascending=True)  # Ascending keeps the fastest driver at the top of a horizontal bar chart

    # 4. Create the Plot
    fig, ax = plt.subplots(figsize=(12, 8))
    actual_event = session.event['EventName']

    bars = ax.barh(df['Driver'], df['TopSpeed'], color=df['Color'], edgecolor='black', height=0.7)

    # Add text labels directly inside the bars for a professional look
    for bar in bars:
        width = bar.get_width()
        ax.text(width - 2, bar.get_y() + bar.get_height() / 2, f"{int(width)} km/h",
                ha='right', va='center', color='white', fontweight='bold', fontsize=10)

    # 5. Formatting and Cleanup
    ax.set_title(f"{year} {actual_event} ({session_type})\nTop Speed Analysis (Fastest Lap)", fontsize=16,
                 fontweight='bold')
    ax.set_xlabel("Top Speed (km/h)", fontsize=12)

    # Zoom in the X-axis so the differences between cars are highly visible
    min_speed = df['TopSpeed'].min()
    ax.set_xlim(min_speed - 10, df['TopSpeed'].max() + 5)

    ax.grid(axis='x', linestyle='--', alpha=0.6)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.tight_layout()
    output_path = os.path.join(output_dir, "top_speed_analysis.png")
    plt.savefig(output_path, dpi=300)
    plt.close()

    return output_path


if __name__ == "__main__":
    top_speed_analysis(2024, "British", "Q")