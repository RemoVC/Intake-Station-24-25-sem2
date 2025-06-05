from picamera2 import Picamera2
import time
import os
from datetime import datetime
from gpiozero import OutputDevice

# === GPIO Setup ===
PUL = OutputDevice(17)  # Pulse pin for the stepper motor
DIR = OutputDevice(27)  # Direction pin for the stepper motor
ENA = OutputDevice(22)  # Enable pin for the stepper motor

# === Motor Settings ===
steps_per_revolution = 6400 * 9  # Steps per revolution, depends on your gear ratio
photo_count = 4  # Number of photos to be taken over a 360-degree rotation
steps_per_photo = steps_per_revolution // photo_count  # Calculate how many steps per photo

# === Photo Storage Setup ===
save_dir = "/home/IntakeStation/Documents/Code_Prototype V0.1/Results/RotationPhotos"  # Path to store photos
os.makedirs(save_dir, exist_ok=True)  # Create the directory if it doesn't exist

# === Camera Setup ===
picam2 = Picamera2()  # Initialize the camera

# Configure the camera for 4K resolution in 4:3 aspect ratio
video_config = picam2.create_still_configuration(main={"size": (4032, 3024)})  # Set to 4:3 aspect ratio
picam2.configure(video_config)  # Apply the configuration

picam2.start()  # Start the camera
time.sleep(1)  # Wait briefly to allow the camera to start

# === Activate Motor ===
DIR.value = 1  # Set motor direction (1 for clockwise, 0 for counter-clockwise)
ENA.on()  # Enable the motor

# Loop to take photos at equal intervals
for i in range(photo_count):
    degrees = int(i * (360 / photo_count))  # Calculate the angle for each photo
    ENA.on()  # Enable the motor to take a photo
    # Capture photo with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Get the current timestamp
    filename = f"photo_{degrees}deg_{timestamp}.jpg"  # Create a filename based on the angle and timestamp
    path = os.path.join(save_dir, filename)  # Full path to save the photo
    picam2.capture_file(path)  # Capture the photo
    time.sleep(1)  # Wait briefly before taking the next photo
    print(f"Photo taken at {degrees}°: {path}")  # Print the photo location
    ENA.off()  # Disable the motor after taking the photo
    if i+1 != photo_count:  # Check if this is not the last photo
        # Rotate motor to the next position
        for _ in range(steps_per_photo):  # Move the motor by the required steps
            PUL.on()  # Send a pulse to the motor
            time.sleep(0.0001)  # Wait briefly
            PUL.off()  # End the pulse
            time.sleep(0.0001)  # Wait briefly

# === Camera and Motor Shutdown ===
picam2.close()  # Close the camera
ENA.on()  # Disable the motor to stop movement

print("All photos taken and saved.")  # Print completion message
