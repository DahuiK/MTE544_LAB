# You can use this file to plot the loged sensor data
# Note that you need to modify/adapt it to your own files
# Feel free to make any modifications/additions here

import matplotlib.pyplot as plt
from utilities_inital import FileReader
import math
import argparse

def plot_imu(filename):
    headers, values = FileReader(filename).read_file()
    # make time start at 0 and change nanoseconds to seconds
    time_list = [(row[-1] - values[0][-1]) / 1e9 for row in values]

    # putting into arrays
    ax, ay, wz = [], [], []
    for row in values:
        ax.append(row[0])
        ay.append(row[1])
        wz.append(row[2])

    # plotting
    plt.figure(figsize=(10, 6))
    plt.plot(time_list, ax, 'r-', label='a_x (m/s^2)')
    plt.plot(time_list, ay, 'g--', label='a_y (m/s^2)')
    plt.plot(time_list, wz, 'b-.', label='w_z (rad/s)')
    plt.title(f'IMU Data vs Time ({filename})')
    plt.xlabel('Time (s)')
    plt.ylabel('Sensor Values')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_odom(filename):
    headers, values = FileReader(filename).read_file()
    time_list = [(row[-1] - values[0][-1]) / 1e9 for row in values]
    
    x, y, th = [], [], []
    for row in values:
        x.append(row[0])
        y.append(row[1])
        th.append(row[2])
        
    # Plot 1: x, y, th vs t
    plt.figure(figsize=(10, 6))
    plt.plot(time_list, x, 'r-', label='x position (m)')
    plt.plot(time_list, y, 'g--', label='y position (m)')
    plt.plot(time_list, th, 'b-.', label='theta (rad)')
    plt.title(f'Linear Inductive Encoder Data vs Time ({filename})')
    plt.xlabel('Time (s)')
    plt.ylabel('Values')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # Plot 2: x vs y
    plt.figure(figsize=(8, 8))
    plt.plot(x, y, 'm-x', label='Robot Path')
    plt.title(f'Linear Inductive Encoder Path (X vs Y) ({filename})')
    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    plt.legend()
    plt.grid(True)
    plt.axis('equal') # for better comparison
    plt.show()

def plot_laser(filename):
    headers, values = FileReader(filename).read_file()
    
    # first row
    row = values[0]
    
    # matching formatting from msg
    angle_increment = row[-2]
    ranges = row[:-2]
    
    x_coords, y_coords = [], []
    
    # change ranges to cartesian with x = r*cos(theta), y = r*sin(theta)
    for i, r in enumerate(ranges):
        # take out NaN and Inf
        if not math.isnan(r) and not math.isinf(r):
            theta = i * angle_increment
            x_coords.append(r * math.cos(theta))
            y_coords.append(r * math.sin(theta))
            
    plt.figure(figsize=(8, 8))
    plt.scatter(x_coords, y_coords, c='b', marker='.', label='Laser Scan Points')
    plt.title(f'Laser Scan Cartesian Map ({filename})')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def process_file(filename):
    # use function based on name
    if 'imu' in filename.lower():
        plot_imu(filename)
    elif 'odom' in filename.lower():
        plot_odom(filename)
    elif 'laser' in filename.lower() or 'scan' in filename.lower():
        plot_laser(filename)
    else:
        print(f"Unrecognized file type for {filename}")

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Process sensor data files.')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to process')
    args = parser.parse_args()
    
    for filename in args.files:
        print(f"Plotting {filename}...")
        process_file(filename)

    # if not (filename):
    #     print ("nope")