import sys
from gpiozero import OutputDevice  # Used to control GPIO pins on Raspberry Pi
import time
import signal  # Not used in this script, but useful for handling clean exits

# GPIO Pin setup for motor control
PUL = OutputDevice(17)  # Pulse pin: sends step signal to stepper driver
DIR = OutputDevice(27)  # Direction pin: sets rotation direction
ENA = OutputDevice(22)  # Enable pin: enables or disables the stepper driver

# Enable the motor driver (active LOW)
ENA.off()  # Set LOW to activate driver

def draai_stappen(aantal_stappen, snelheid, richting=1):
    """
    Function to rotate the motor a specific number of steps.
    
    :param aantal_stappen: Number of steps to move
    :param snelheid: Delay between pulses (lower = faster)
    :param richting: Direction (1 = right, 0 = left)
    """
    DIR.value = 1 if richting == 1 else 0  # Set direction pin
    for _ in range(aantal_stappen):
        PUL.on()              # Send HIGH signal
        time.sleep(snelheid)  # Wait
        PUL.off()             # Send LOW signal
        time.sleep(snelheid)  # Wait again

def motor_beweging(richting, snelheid):
    """
    Function to continuously rotate the motor in the given direction.

    :param richting: Direction of rotation (0 = left, 1 = right)
    :param snelheid: Speed of rotation (delay between steps)
    """
    try:
        stappen_per_tafelrotatie = 6400 * 9  # Total steps for a full rotation (adjust to your setup)

        while True:
            if richting == 0:
                draai_stappen(stappen_per_tafelrotatie, snelheid, richting=0)
            elif richting == 1:
                draai_stappen(stappen_per_tafelrotatie, snelheid, richting=1)

            time.sleep(0.1)  # Small pause to prevent CPU overload

    except KeyboardInterrupt:
        print("\nMotor interrupted with Ctrl+C!")
        ENA.on()  # Disable the motor
        cleanup()

def cleanup():
    """
    Cleanly shut down GPIO pins and disable the motor.
    """
    ENA.on()   # Disable motor
    PUL.close()
    DIR.close()

# Read command-line arguments
if len(sys.argv) < 3:
    print("Error: Not enough arguments. Usage: python Motor_Manual.py <direction> <speed>")
    sys.exit(1)

richting = int(sys.argv[1])    # 0 for left, 1 for right
snelheid = float(sys.argv[2])  # Delay in seconds (e.g., 0.001 for fast)

# Start motor movement with provided parameters
motor_beweging(richting, snelheid)
