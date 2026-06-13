import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import pandas as pd
import os


def track_dominance_map(year, gp, d1, d2, output_dir="."):
    session = fastf1.get_session(year, gp, "Q")
    session.load()

    fastf1.plotting.setup_mpl(misc_mpl_mods=False, color_scheme=None)

    lap1 = session.laps.pick_driver(d1).pick_fastest()
    lap2 = session.laps.pick_driver(d2).pick_fastest()

    tel1 = lap1.get_telemetry()
    tel2 = lap2.get_telemetry()

    max_distance = max(tel1['Distance'].max(), tel2['Distance'].max())
    distance_space = np.linspace(0, max_distance, 1500)

    speed1 = np.interp(distance_space, tel1['Distance'], tel1['Speed'])
    speed2 = np.interp(distance_space, tel2['Distance'], tel2['Speed'])

    x_coords = np.interp(distance_space, tel1['Distance'], tel1['X'])
    y_coords = np.interp(distance_space, tel1['Distance'], tel1['Y'])

    num_minisectors = 25
    minisector_length = max_distance / num_minisectors
    minisectors = (distance_space // minisector_length).astype(int)

    df = pd.DataFrame({
        'Distance': distance_space,
        'Speed1': speed1,
        'Speed2': speed2,
        'Minisector': minisectors,
        'X': x_coords,
        'Y': y_coords
    })

    avg_speeds = df.groupby('Minisector')[['Speed1', 'Speed2']].mean()
    avg_speeds['Fastest'] = np.where(avg_speeds['Speed1'] > avg_speeds['Speed2'], 1, 2)

    df = df.merge(avg_speeds['Fastest'], on='Minisector')

    points = np.array([df['X'], df['Y']]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    try:
        color1 = fastf1.plotting.get_driver_color(d1, session)
        color2 = fastf1.plotting.get_driver_color(d2, session)
    except:
        color1, color2 = 'cyan', 'magenta'

    color_map = {1: color1, 2: color2}
    colors = df['Fastest'][:-1].map(color_map).to_list()

    actual_event = session.event['EventName']

    fig, ax = plt.subplots(figsize=(12, 10))
    fig.suptitle(f"{year} {actual_event} - Qualifying\nTrack Dominance: {d1} vs {d2}", fontsize=16, fontweight='bold')

    lc = LineCollection(segments, colors=colors, linewidths=5.5)
    ax.add_collection(lc)

    ax.set_xlim(df['X'].min() - 600, df['X'].max() + 600)
    ax.set_ylim(df['Y'].min() - 600, df['Y'].max() + 600)
    ax.set_aspect('equal')
    ax.axis('off')

    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color=color1, lw=5, label=f"{d1} Faster"),
        Line2D([0], [0], color=color2, lw=5, label=f"{d2} Faster")
    ]
    ax.legend(handles=legend_elements, loc='upper right', frameon=True, fontsize=12)

    plt.tight_layout()
    output_path = os.path.join(output_dir, "track_dominance_map.png")
    plt.savefig(output_path, dpi=300)
    plt.close()

    return output_path


if __name__ == "__main__":
    track_dominance_map(2024, "British", "VER", "NOR")
