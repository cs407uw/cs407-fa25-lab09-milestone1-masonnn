import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def analyze_direction():
    csv_path = os.path.join('..', 'app', 'src', 'main', 'assets', 'TURNING.csv')
    
    try:
        # usecols=range(10) ensures we only read the valid columns and ignore trailing commas
        df = pd.read_csv(csv_path, usecols=range(10))
    except FileNotFoundError:
        print(f"Error: Could not find file at {csv_path}")
        return

    # 1. Process Timestamp
    df['time_sec'] = (df['timestamp'] - df['timestamp'].iloc[0]) / 1e9
    
    # Calculate dt
    # We can use the mean dt or individual dt
    # Individual dt is better if sampling is irregular
    df['dt'] = df['time_sec'].diff().fillna(0)

    # 2. Integrate Gyro Z
    # gyro_z is in rad/s (usually). Let's assume rad/s.
    # Angle = cumulative sum of (gyro_z * dt)
    df['angle_rad'] = (df['gyro_z'] * df['dt']).cumsum()
    
    # Convert to degrees
    df['angle_deg'] = np.degrees(df['angle_rad'])

    # 3. Results
    total_turn = df['angle_deg'].iloc[-1]
    print(f"Total angle turned: {total_turn:.2f} degrees")

    # 4. Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(df['time_sec'], df['angle_deg'], label='Heading Angle', color='purple')
    
    plt.title(f'Direction Detection (Total Turn: {total_turn:.2f}°)')
    plt.xlabel('Time (s)')
    plt.ylabel('Angle (degrees)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('part3_direction.png')
    print("Plot saved to 'part3_direction.png'")

if __name__ == "__main__":
    analyze_direction()
