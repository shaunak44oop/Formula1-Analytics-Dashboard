import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt


def compare_drivers(year, gp, session_type, d1, d2):
    # 1. Load Session
    session = fastf1.get_session(year, gp, session_type)
    session.load()

    # Enable F1 team color schemes
    fastf1.plotting.setup_mpl(misc_mpl_mods=False, color_scheme=None)

    # 2. Extract Fastest Laps and Telemetry
    lap1 = session.laps.pick_driver(d1).pick_fastest()
    lap2 = session.laps.pick_driver(d2).pick_fastest()

    # get_telemetry() is much smoother and more robust than get_car_data()
    car1 = lap1.get_telemetry()
    car2 = lap2.get_telemetry()

    # Automatically grab official driver colors
    try:
        color1 = fastf1.plotting.get_driver_color(d1, session)
        color2 = fastf1.plotting.get_driver_color(d2, session)
    except:
        color1, color2 = "blue", "red"  # Fallback if colors fail

    # 3. Create Multi-Panel Plot Grid
    # sharex=True ensures zooming into a corner on one graph zooms all of them
    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True, gridspec_kw={'height_ratios': [2, 1, 1]})
    fig.suptitle(f"{year} {gp} {session_type} - Telemetry Comparison\n{d1} vs {d2}", fontsize=18, fontweight='bold')

    # --- TOP PANEL: Speed ---
    axes[0].plot(car1['Distance'], car1['Speed'], color=color1, label=d1, linewidth=2)
    axes[0].plot(car2['Distance'], car2['Speed'], color=color2, label=d2, linewidth=2)
    axes[0].set_ylabel("Speed (km/h)", fontsize=12)
    axes[0].legend(loc="lower right", frameon=True)
    axes[0].grid(True, linestyle='--', alpha=0.6)

    # --- MIDDLE PANEL: Throttle ---
    axes[1].plot(car1['Distance'], car1['Throttle'], color=color1, linewidth=1.5)
    axes[1].plot(car2['Distance'], car2['Throttle'], color=color2, linewidth=1.5)
    axes[1].set_ylabel("Throttle (%)", fontsize=12)
    axes[1].grid(True, linestyle='--', alpha=0.6)

    # --- BOTTOM PANEL: Brake ---
    axes[2].plot(car1['Distance'], car1['Brake'], color=color1, linewidth=1.5)
    axes[2].plot(car2['Distance'], car2['Brake'], color=color2, linewidth=1.5)
    axes[2].set_ylabel("Brake", fontsize=12)
    axes[2].set_xlabel("Distance (m)", fontsize=12)

    # Format the brake graph to just show On/Off states
    axes[2].set_yticks([0, 1])
    axes[2].set_yticklabels(['Off', 'On'])
    axes[2].grid(True, linestyle='--', alpha=0.6)

    # 4. Save and Cleanup
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.1)  # Removes vertical gaps between subplots
    #plt.savefig("telemetry_comparison.png", dpi=300)
    output_path = os.path.join(output_dir, "telemetry_comparison.png")
    plt.savefig(output_path, dpi=300)
    return output_path
    plt.close()


# For testing locally
if __name__ == "__main__":
    compare_drivers(2025, "Canada", "Q", "VER", "NOR")