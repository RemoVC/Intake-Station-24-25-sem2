from gpiozero import OutputDevice
import time
import sys

#  Command-line arguments: number of steps and speed mode
if len(sys.argv) < 3:
    print("Usage: python3 Motor_Auto.py <number_of_steps> <speed>")
    sys.exit(1)

aantal_stappen = int(sys.argv[1])       # Number of motor steps
max_snelheid_str = sys.argv[2]          # Speed type as string: 'Slow', 'Med', or 'Fast'

# Convert the speed string to a numeric delay (in seconds)
if max_snelheid_str == "Slow":
    max_snelheid = 0.0008  # Slower speed (larger delay between steps)
elif max_snelheid_str == "Med":
    max_snelheid = 0.0001  # Medium speed
elif max_snelheid_str == "Fast":
    max_snelheid = 0.00005  # Fastest speed (smallest delay)
else:
    print("Invalid speed. Choose 'Slow', 'Med', or 'Fast'.")
    sys.exit(1)

# GPIO pin setup
PUL = OutputDevice(17)  # Pulse pin: controls step signals
DIR = OutputDevice(27)  # Direction pin: controls motor rotation direction
ENA = OutputDevice(22)  # Enable pin: activates the motor driver

ENA.off()  # Enable the motor (active LOW)

# Function to rotate the motor a specified number of steps
def draai_stappen(aantal_stappen, snelheid):
    DIR.value = 1  # Set rotation direction (1 = clockwise)
    
    delay = max_snelheid  # Set delay between steps based on speed

    for _ in range(aantal_stappen):
        PUL.on()             # Set pulse pin HIGH
        time.sleep(delay)    # Wait for delay
        PUL.off()            # Set pulse pin LOW
        time.sleep(delay)    # Wait again

try:
    # Start motor rotation with the specified number of steps and speed
    print(f"Starting rotation for {aantal_stappen} steps at speed: {max_snelheid}...")

    draai_stappen(aantal_stappen=aantal_stappen, snelheid=max_snelheid)
    print("Rotation complete.")

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    ENA.on()  # Disable the motor (set pin HIGH)
    print("Motor disabled.")
