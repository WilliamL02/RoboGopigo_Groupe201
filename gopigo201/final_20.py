import easygopigo3 as easy
import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define sensor pins
left_trig = 5
left_echo = 6
front_trig = 16
front_echo = 12
right_trig = 20
right_echo = 21

# Set up sensor pins
GPIO.setup(left_trig, GPIO.OUT)
GPIO.setup(left_echo, GPIO.IN)
GPIO.setup(front_trig, GPIO.OUT)
GPIO.setup(front_echo, GPIO.IN)
GPIO.setup(right_trig, GPIO.OUT)
GPIO.setup(right_echo, GPIO.IN)

# Initialize GoPiGo
my_easy_robot = easy.EasyGoPiGo3()

def distance(trig_pin, echo_pin):
    # Send pulse to trigger
    GPIO.output(trig_pin, True)
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)

    # Measure time for echo
    pulse_start = time.time()
    pulse_end = time.time()
    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()
    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()

    # Calculate distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound = 34300 cm/s, divide by 2 as we're measuring round-trip
    distance = round(distance, 2)
    return distance

def move_forward():
    my_easy_robot.set_speed(200)  # Adjust speed as needed
    my_easy_robot.forward()
    time.sleep(0.5)  # Adjust as per your robot's movement needs

def backtrack_and_find_clear_path():
    my_easy_robot.stop()
    print("Backing up to find clear path...")

    speed_cm_per_s = 20  # Adjust according to your robot's speed
    distance_to_backtrack = 30  # Distance to backtrack in cm

    # Back up for the calculated time
    my_easy_robot.set_speed(200)  # Set the speed; adjust as necessary
    my_easy_robot.backward()
    time.sleep(time_to_backtrack)  # Move backward for the calculated time
    my_easy_robot.stop()

    # Stop and turn left to find clear path
    print("Turning right to find clear path...")
    my_easy_robot.turn_degrees(-55)

    # Continue moving forward to find clear path
    move_forward()

def turn_until_clear(direction, threshold):
    # Turn until the front sensor detects no obstacle within the threshold
    print(f"Turning {direction} until clear...")
    while distance(front_trig, front_echo) < threshold:
        if direction == "left":
            my_easy_robot.turn_degrees(-56)  # Turn left by small increments
        elif direction == "right":
            my_easy_robot.turn_degrees(56)  # Turn right by small increments
        time.sleep(0.1)  # Small delay for stabilization
    print("Path clear in front. Stopping turn.")

try:
    while True:
        # Measure distance from each sensor
        left_distance = distance(left_trig, left_echo)
        front_distance = distance(front_trig, front_echo)
        right_distance = distance(right_trig, right_echo)

        # Print distances for debugging
        print("Left Distance:", left_distance, "cm")
        print("Front Distance:", front_distance, "cm")
        print("Right Distance:", right_distance, "cm")

        # Define distance thresholds
        obstacle_threshold = 10  # Threshold for immediate obstacle avoidance
        backtrack_threshold = 30  # Threshold for backtracking decision

        # Check distances and make a decision
        if front_distance < obstacle_threshold:
            my_easy_robot.stop()
            print("Obstacle detected in front. Stopping.")

            # Determine the direction with the greatest distance
            if left_distance > right_distance:
                if left_distance > obstacle_threshold:
                    print("Turning left where distance is longer.")
                    turn_until_clear("left", obstacle_threshold)
                else:
                    print("No clear path. Backtracking.")
                    backtrack_and_find_clear_path()
            elif right_distance > left_distance:
                if right_distance > obstacle_threshold:
                    print("Turning right where distance is longer.")
                    turn_until_clear("right", obstacle_threshold)
                else:
                    print("No clear path. Backtracking.")
                    backtrack_and_find_clear_path()
            else:
                print("No clear path. Backtracking.")
                backtrack_and_find_clear_path()

            # Delay to stabilize before re-checking distances
            time.sleep(1.0)
        elif (left_distance < backtrack_threshold and 
              front_distance < backtrack_threshold and 
              right_distance < backtrack_threshold):
            # If all distances are below the backtrack threshold, backtrack
            print("All sensors detect obstacles within 30 cm. Backtracking.")
            backtrack_and_find_clear_path()
        else:
            # No obstacles detected, continue moving forward
            move_forward()

except KeyboardInterrupt:
    GPIO.cleanup()
    my_easy_robot.stop()

