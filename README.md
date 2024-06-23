# Obstacle-Avoiding Robot with GoPiGo3 and Ultrasonic Sensors

## Introduction
This project involves building a robot using the GoPiGo3 robot platform that can use 3 ultrasonic sensors to detect obstacles in its path and try to avoid them.


## Features
- Obstacle detection using ultrasonic sensors.
- Automatic turning and backtracking when obstacles are detected.
- Adjustable speed and distance thresholds.


## Setup and Installation
1. **Install Libraries**:
    ```bash
    sudo pip3 install easygopigo3
    sudo apt-get install python3-rpi.gpio
    ```

2. **Wire the Ultrasonic Sensors**:
    - Connect the TRIG and ECHO pins of the ultrasonic sensors to the GPIO pins on the Raspberry Pi as described in the code.

3. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/obstacle-avoiding-robot.git
    cd obstacle-avoiding-robot
    ```

4. **Run the Code**:
    ```bash
    python3 obstacle_avoiding_robot.py
    ```

## Usage
- **Start the Robot**:
    - Ensure the robot is on a flat surface and free of obstacles.
    - Run the code using `python3 obstacle_avoiding_robot.py`.
    - The robot will start moving forward and will avoid obstacles autonomously.

- **Stop the Robot**:
    - Press `Ctrl+C` to stop the robot and clean up GPIO settings.


## Code Overview
- **Distance Measurement**:
    -The `distance()` function emits an ultrasonic pulse and measures the time it takes for the echo to bounce back, thereby determining the distance to an object.

- **Movement Functions**:
    - `move_forward()`: Moves the robot forward for a short duration.
    - `backtrack_and_find_clear_path()`: Moves the robot backward and turns to find a clear path.
    - `turn_until_clear(direction, threshold)`: Turns the robot in a specified direction until a clear path is detected.

- **Main Loop**:
    - Continuously measures distances from the sensors.
    - Stops and makes decisions based on the distances detected, such as turning or backtracking.
