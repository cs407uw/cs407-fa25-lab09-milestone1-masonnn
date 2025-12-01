import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.signal import find_peaks

def detect_steps():
    csv_path = os.path.join('..', 'app', 'src', 'main', 'assets', 'WALKING.csv')
    
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: Could not find file at {csv_path}")
        return

    # 1. Process Timestamp
    # Convert nanoseconds to seconds, starting from 0
    df['time_sec'] = (df['timestamp'] - df['timestamp'].iloc[0]) / 1e9

    # 2. Calculate Magnitude
    df['accel_mag'] = np.sqrt(df['accel_x']**2 + df['accel_y']**2 + df['accel_z']**2)

    # 3. Smooth the signal (Moving Average)
    # Window size needs to be tuned. Assuming ~100Hz sampling (dt=0.01s), 
    # a step takes ~0.5s. A window of 0.1s-0.2s might be good.
    # Let's check the sampling rate.
    dt_avg = df['time_sec'].diff().mean()
    print(f"Average sampling rate: {1/dt_avg:.2f} Hz")
    
    # Use a window of roughly 0.2 seconds
    window_size = int(0.2 / dt_avg)
    df['accel_smooth'] = df['accel_mag'].rolling(window=window_size, center=True).mean()

    # 4. Peak Detection
    # We need to find peaks in the smoothed signal.
    # Threshold: Gravity is ~9.8. Steps usually cause spikes above 10-11.
    # Let's try a threshold of 10.5 or 11.
    # Min distance: A step takes at least 0.3s.
    min_dist = int(0.3 / dt_avg)
    
    peaks, _ = find_peaks(df['accel_smooth'].fillna(0), height=10.5, distance=min_dist)
    
    num_steps = len(peaks)
    print(f"Number of steps detected: {num_steps}")

    # 5. Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(df['time_sec'], df['accel_mag'], label='Raw Magnitude', alpha=0.3, color='gray')
    plt.plot(df['time_sec'], df['accel_smooth'], label='Smoothed Magnitude', color='blue')
    plt.plot(df['time_sec'].iloc[peaks], df['accel_smooth'].iloc[peaks], "x", label='Detected Steps', color='red')
    
    plt.title(f'Step Detection (Count: {num_steps})')
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration Magnitude (m/s^2)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('part2_steps.png')
    print("Plot saved to 'part2_steps.png'")

if __name__ == "__main__":
    detect_steps()
