import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def analyze_acceleration():
    # Path to the CSV file
    csv_path = os.path.join('..', 'app', 'src', 'main', 'assets', 'ACCELERATION.csv')
    
    # Read the CSV
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: Could not find file at {csv_path}")
        return

    # Calculate dt (assuming constant time step based on first two rows)
    dt = df['timestamp'][1] - df['timestamp'][0]
    print(f"Time step (dt): {dt}s")

    # --- Ground Truth (acceleration) ---
    # Velocity = integral of acceleration
    # We use cumulative sum * dt
    df['velocity_gt'] = df['acceleration'].cumsum() * dt
    
    # Distance = integral of velocity
    df['distance_gt'] = df['velocity_gt'].cumsum() * dt

    # --- Noisy Data (noisyacceleration) ---
    df['velocity_noisy'] = df['noisyacceleration'].cumsum() * dt
    df['distance_noisy'] = df['velocity_noisy'].cumsum() * dt

    # --- Results ---
    final_distance_gt = df['distance_gt'].iloc[-1]
    final_distance_noisy = df['distance_noisy'].iloc[-1]

    print(f"Final Distance (Ground Truth): {final_distance_gt:.4f} m")
    print(f"Final Distance (Noisy): {final_distance_noisy:.4f} m")
    print(f"Difference: {abs(final_distance_gt - final_distance_noisy):.4f} m")

    # --- Plotting ---
    plt.figure(figsize=(12, 10))

    # 1. Acceleration
    plt.subplot(3, 1, 1)
    plt.plot(df['timestamp'], df['acceleration'], label='Ground Truth', color='green')
    plt.plot(df['timestamp'], df['noisyacceleration'], label='Noisy', color='red', alpha=0.7)
    plt.title('Acceleration vs Time')
    plt.ylabel('Acceleration (m/s^2)')
    plt.legend()
    plt.grid(True)

    # 2. Velocity
    plt.subplot(3, 1, 2)
    plt.plot(df['timestamp'], df['velocity_gt'], label='Ground Truth', color='green')
    plt.plot(df['timestamp'], df['velocity_noisy'], label='Noisy', color='red', alpha=0.7)
    plt.title('Velocity vs Time')
    plt.ylabel('Velocity (m/s)')
    plt.legend()
    plt.grid(True)

    # 3. Distance
    plt.subplot(3, 1, 3)
    plt.plot(df['timestamp'], df['distance_gt'], label='Ground Truth', color='green')
    plt.plot(df['timestamp'], df['distance_noisy'], label='Noisy', color='red', alpha=0.7)
    plt.title('Distance vs Time')
    plt.ylabel('Distance (m)')
    plt.xlabel('Time (s)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('part1_plots.png')
    print("Plots saved to 'part1_plots.png'")
    # plt.show() # Commented out for non-interactive environments

if __name__ == "__main__":
    analyze_acceleration()
