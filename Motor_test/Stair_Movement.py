from gpiozero import OutputDevice
import time

# Define GPIO pins
PUL = OutputDevice(17)
DIR = OutputDevice(27)
ENA = OutputDevice(22)

# Enable motor
ENA.off()

def move_steps_three_phase(total_steps, min_speed, max_speed, direction=1, accel_steps=200):
    """
    Moves the stepper motor in three phases:
    1. Constant low speed
    2. Constant high speed
    3. Constant low speed
    """

    # Set direction
    DIR.value = 1 if direction == 1 else 0

    # Make sure we don't ask more acceleration steps than we have
    if 2 * accel_steps > total_steps:
        accel_steps = total_steps // 2

    # Calculate steps for constant high speed phase
    const_steps = total_steps - 2 * accel_steps

    # Phase 1: Low speed (starting)
    for _ in range(accel_steps):
        PUL.on()
        time.sleep(min_speed)
        PUL.off()
        time.sleep(min_speed)

    # Phase 2: High speed
    for _ in range(const_steps):
        PUL.on()
        time.sleep(max_speed)
        PUL.off()
        time.sleep(max_speed)

    # Phase 3: Low speed (ending)
    for _ in range(accel_steps):
        PUL.on()
        time.sleep(min_speed)
        PUL.off()
        time.sleep(min_speed)

try:
    steps_per_table_rotation = 6400 * 9
    min_speed = 0.0001         # Slower speed
    max_speed = 0.000005      # Faster speed
    accel_steps = 6400        # Number of steps for start and end phases

    start = time.time()

    move_steps_three_phase(
        total_steps=steps_per_table_rotation,
        min_speed=min_speed,
        max_speed=max_speed,
        direction=0,
        accel_steps=accel_steps
    )

    end = time.time()
    print("1 full rotation completed in", round(end - start, 2), "seconds")

except KeyboardInterrupt:
    print("\nStopped manually (Ctrl + C)")

finally:
    ENA.on()
    print("ENA High = Motor disabled")
