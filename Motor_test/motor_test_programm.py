from gpiozero import OutputDevice
import time

# Define GPIO pins for controlling the stepper motor
PUL = OutputDevice(17)  # Pulse pin
DIR = OutputDevice(27)  # Direction pin
ENA = OutputDevice(22)  # Enable pin

# Disable the motor driver (ENA is active low)
ENA.off()

def rotate_steps(step_count, speed, direction=1):
    """
    Rotates the stepper motor a given number of steps at a specified speed and direction.
    
    :param step_count: Total number of steps to move the motor.
    :param speed: Delay between pulse signals (controls speed).
    :param direction: Direction of rotation (1 for forward, 0 for backward).
    """
    DIR.value = 1 if direction == 1 else 0  # Set rotation direction

    for _ in range(step_count):
        PUL.on()               # Send pulse high
        time.sleep(speed)      # Wait for pulse duration
        PUL.off()              # Send pulse low
        time.sleep(speed)      # Wait before the next pulse

try:
    # Define motor rotation parameters
    steps_per_rotation = 6400 * 1   # Full rotation = 6400 steps (adjust for microstepping)
    rps = 0.8                       # Rotations per second
    delay_per_half_step = 1 / (2 * 6400 * 9 * rps)  # Time between each half step
    
    start = time.time()  # Start time for measuring duration
    rotate_steps(steps_per_rotation, delay_per_half_step, direction=1)  # Rotate once
    end = time.time()    # End time after rotation
    
    print("1 full rotation completed in", end - start, "seconds")

except KeyboardInterrupt:
    print("\nInterrupted with Ctrl+C! Motor is being disabled...")

finally:
    ENA.on()  # Re-enable (or disable, depending on hardware logic) the motor driver

# Speed testing:
# 0.001 is a good speed for testing
