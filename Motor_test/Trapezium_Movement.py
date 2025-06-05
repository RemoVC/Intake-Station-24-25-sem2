from gpiozero import OutputDevice
import time

#######################################
# Trapezoidal Movement with Real Acceleration
#######################################

# Define GPIO pins for controlling the stepper motor
PUL = OutputDevice(17)  # Pulse pin - triggers steps
DIR = OutputDevice(27)  # Direction pin - sets direction of rotation
ENA = OutputDevice(22)  # Enable pin - turns the motor on/off

ENA.off()  # Enable the motor (LOW = ON for most drivers)

def move_steps_with_acceleration(step_count, max_speed, acceleration, direction=1):
    """
    Move the stepper motor using trapezoidal motion:
    - Accelerates with constant acceleration
    - Maintains a maximum speed for a period
    - Decelerates with the same acceleration

    Parameters:
    - step_count: Total number of steps for the move
    - max_speed: Maximum step speed (in steps per second)
    - acceleration: Acceleration value (in steps/sec^2)
    - direction: 1 for forward, 0 for reverse
    """

    # Set the direction pin
    DIR.value = 1 if direction == 1 else 0

    step_size = 1  # Each pulse represents one step
    min_speed = 100  # Minimum speed to avoid extremely slow delays (steps/sec)

    # Time required to reach max speed from 0 using v = a * t → t = v / a
    time_to_max_speed = max_speed / acceleration

    # Calculate how many steps are taken during acceleration using:
    # s = 0.5 * a * t^2
    accel_steps = int(0.5 * acceleration * time_to_max_speed ** 2 / step_size)

    # Prevent overshooting total steps
    accel_steps = min(accel_steps, step_count // 2)

    decel_steps = accel_steps
    const_speed_steps = step_count - accel_steps - decel_steps

    print(f"Acceleration Steps: {accel_steps}, Constant Speed Steps: {const_speed_steps}, Deceleration Steps: {decel_steps}")

    # ACCELERATION PHASE
    for i in range(accel_steps):
        # Linearly increase time from 0 to time_to_max_speed
        t = (i / accel_steps) * time_to_max_speed
        speed = acceleration * t  # v = a * t
        speed = max(speed, min_speed)  # Cap minimum speed
        delay = 1 / (2 * speed)  # Delay for each half pulse (on/off)
        PUL.on()
        time.sleep(delay)
        PUL.off()
        time.sleep(delay)

    # CONSTANT SPEED PHASE
    delay = 1 / (2 * max_speed)
    for _ in range(const_speed_steps):
        PUL.on()
        time.sleep(delay)
        PUL.off()
        time.sleep(delay)

    # DECELERATION PHASE
    for i in range(decel_steps):
        # Time from 0 to time_to_max_speed in reverse
        t = (i / decel_steps) * time_to_max_speed
        speed = max_speed - acceleration * t  # v = vmax - a * t
        speed = max(speed, min_speed)
        delay = 1 / (2 * speed)
        PUL.on()
        time.sleep(delay)
        PUL.off()
        time.sleep(delay)

try:
    # Define total steps for one full rotation (adjust gear ratio if needed)
    steps_per_rotation = 6400 * 9  # 9 = gear ratio

    # Motion profile parameters
    max_speed = 200000       # Max speed in steps per second
    acceleration = 200       # Acceleration in steps per second squared

    # Start timer
    start = time.time()

    # Execute movement
    move_steps_with_acceleration(
        step_count=steps_per_rotation,
        max_speed=max_speed,
        acceleration=acceleration,
        direction=1  # 1 = forward
    )

    # End timer
    end = time.time()
    print(f"1 full rotation completed in {round(end - start, 2)} seconds")

except KeyboardInterrupt:
    print("Program interrupted by user.")

finally:
    ENA.on()  # Disable the motor (HIGH = OFF for most drivers)
    print("ENA HIGH → Motor disabled")
