import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import os


def compare_drivers(year, gp, session_type, d1, d2, output_dir="."):
    session = fastf1.get_session(year, gp, session_type)
    session.load()

    fastf1.plotting.setup_mpl(misc_mpl_mods=False, color_scheme=None)

    lap1 = session.laps.pick_driver(d1).pick_fastest()
    lap2 = session.laps.pick_driver(d2).pick_fastest()

    car1 = lap1.get_telemetry()
    car2 = lap2.get_telemetry()

    try:
        color1 = fastf1.plotting.get_driver_color(d1, session)
        color2 = fastf1.plotting.get_driver_color(d2, session)
    except:
        color1, color2 = "blue", "red"

    actual_event = session.event['EventName']

    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True, gridspec_kw={'height_ratios': [2, 1, 1]})
    fig.suptitle(f"{year} {actual_event} ({session_type})\nTelemetry Comparison: {d1} vs {d2}", fontsize=18,
                 fontweight='bold')

    axes[0].plot(car1['Distance'], car1['Speed'], color=color1, label=d1, linewidth=2)
    axes[0].plot(car2['Distance'], car2['Speed'], color=color2, label=d2, linewidth=2)
    axes[0].set_ylabel("Speed (km/h)", fontsize=12)
    axes[0].legend(loc="lower right", frameon=True)
    axes[0].grid(True, linestyle='--', alpha=0.6)

    axes[1].plot(car1['Distance'], car1['Throttle'], color=color1, linewidth=1.5)
    axes[1].plot(car2['Distance'], car2['Throttle'], color=color2, linewidth=1.5)
    axes[1].set_ylabel("Throttle (%)", fontsize=12)
    axes[1].grid(True, linestyle='--', alpha=0.6)

    axes[2].plot(car1['Distance'], car1['Brake'], color=color1, linewidth=1.5)
    axes[2].plot(car2['Distance'], car2['Brake'], color=color2, linewidth=1.5)
    axes[2].set_ylabel("Brake", fontsize=12)
    axes[2].set_xlabel("Distance (m)", fontsize=12)
    axes[2].set_yticks([0, 1])
    axes[2].set_yticklabels(['Off', 'On'])
    axes[2].grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.1)

    output_path = os.path.join(output_dir, "telemetry_comparison.png")
    plt.savefig(output_path, dpi=300)
    plt.close()

    return output_path


if __name__ == "__main__":
    compare_drivers(2024, "British", "Q", "VER", "NOR")
