import time
import os
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
from gpiozero import OutputDevice
from datetime import datetime

# === GPIO Setup for the Motor ===
PUL = OutputDevice(17)  # Pulse pin for stepper motor control
DIR = OutputDevice(27)  # Direction pin for stepper motor
ENA = OutputDevice(22)  # Enable pin for stepper motor

# Set the motor direction
DIR.value = 1  # Set motor direction (1 for clockwise, 0 for counter-clockwise)

# Activate the motor
ENA.off()  # Enable the motor (motor is on when ENA is low)

# === Video Storage Setup ===
video_dir = "/home/IntakeStation/Videos"  # Directory to save the video
os.makedirs(video_dir, exist_ok=True)  # Create the directory if it doesn't exist
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Get current timestamp
video_path = os.path.join(video_dir, f"rotation_video_{timestamp}.h264")  # Full path for the video

# === Camera Setup ===
picam2 = Picamera2()  # Initialize the PiCamera2
video_config = picam2.create_video_configuration(main={"size": (1920, 1080)})  # Configure video resolution
picam2.configure(video_config)  # Apply configuration

# === Encoder and Output Setup ===
encoder = H264Encoder(bitrate=10000000)  # Set the encoder to H264 with a bitrate of 10 Mbps
output = FileOutput(video_path)  # Set the output file path for the video

# === Start Video Recording ===
picam2.start_recording(encoder, output)  # Start recording video
print(f" Recording started: {video_path}")  # Print message with the video path
time.sleep(1)  # Wait a moment before starting the motor

# === Rotate the Motor by 360 Degrees ===
# The number of steps depends on your motor configuration, adjust accordingly
for _ in range(6400 * 9):  # Rotate the motor (6400 steps per revolution * 9 for your setup)
    PUL.on()  # Send a pulse to the motor
    time.sleep(0.00005)  # Wait briefly between pulses
    PUL.off()  # End the pulse
    time.sleep(0.00005)  # Wait briefly before sending the next pulse

# === Stop Video Recording ===
picam2.stop_recording()  # Stop recording video
picam2.close()  # Close the camera

# === Deactivate the Motor ===
ENA.on()  # Disable the motor (motor is off when ENA is high)

# === Completion Message ===
print(f" Recording completed and saved: {video_path}")  # Print completion message with the video path
