import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.signal import find_peaks

def analyze_trajectory():
    csv_path = os.path.join('..', 'app', 'src', 'main', 'assets', 'WALKING_AND_TURNING.csv')
    
    try:
        df = pd.read_csv(csv_path, usecols=range(10))
    except FileNotFoundError:
        print(f"Error: Could not find file at {csv_path}")
        return

    # 1. Process Timestamp
    df['time_sec'] = (df['timestamp'] - df['timestamp'].iloc[0]) / 1e9
    df['dt'] = df['time_sec'].diff().fillna(0)

    # 2. Step Detection
    df['accel_mag'] = np.sqrt(df['accel_x']**2 + df['accel_y']**2 + df['accel_z']**2)
    
    dt_avg = df['time_sec'].diff().mean()
    window_size = int(0.2 / dt_avg)
    df['accel_smooth'] = df['accel_mag'].rolling(window=window_size, center=True).mean()
    
    min_dist = int(0.3 / dt_avg)
    peaks, _ = find_peaks(df['accel_smooth'].fillna(0), height=10.5, distance=min_dist)
    
    print(f"Steps detected: {len(peaks)}")

    # 3. Heading Calculation
    # Integrate gyro_z
    df['angle_rad'] = (df['gyro_z'] * df['dt']).cumsum()
    
    # Initial position
    x = [0]
    y = [0]
    stride_length = 0.8 # meters

    # 4. Calculate Trajectory
    # We iterate through the steps
    # For each step, we take the heading at that timestamp
    
    step_times = df['time_sec'].iloc[peaks].values
    step_indices = peaks
    
    for i in step_indices:
        # Get heading at the time of the step
        # We might want to offset the heading by 90 degrees if the phone orientation is different
        # But assuming standard orientation:
        current_heading = df['angle_rad'].iloc[i]
        
        # Update position
        new_x = x[-1] + stride_length * np.cos(current_heading)
        new_y = y[-1] + stride_length * np.sin(current_heading)
        
        x.append(new_x)
        y.append(new_y)

    # 5. Plotting
    plt.figure(figsize=(8, 8))
    plt.plot(x, y, marker='o', markersize=4, linestyle='-', color='blue')
    plt.plot(x[0], y[0], 'go', label='Start')
    plt.plot(x[-1], y[-1], 'ro', label='End')
    
    plt.title(f'Trajectory (Steps: {len(peaks)})')
    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    plt.axis('equal')
    plt.grid(True)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('part4_trajectory.png')
    print("Plot saved to 'part4_trajectory.png'")

if __name__ == "__main__":
    analyze_trajectory()
