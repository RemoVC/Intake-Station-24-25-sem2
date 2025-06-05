from picamera2 import Picamera2
import time
import os
import sys
from datetime import datetime  # Added to handle date and time

# Get arguments from command line
object_name = sys.argv[1]  # Object name (e.g., product ID or item name)
foto_nummer = sys.argv[2]  # Photo number (can be used to track multiple photos for the same object)

# Generate a timestamp string (e.g., 2024-04-15_14-30-59)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Define base directory path for saving the photos
base_dir = "/home/IntakeStation/Documents/Code_Prototype V0.1/Results/Procedure"
object_dir = os.path.join(base_dir, object_name)

# Create the object directory if it doesn't exist yet
os.makedirs(object_dir, exist_ok=True)

# Define the filename for saving the photo (based on object name, photo number, and timestamp)
filename = f"{object_name}_{foto_nummer}_{timestamp}.jpg"
save_path = os.path.join(object_dir, filename)

# Initialize Picamera2
picam2 = Picamera2()

# Configure the camera for high resolution (4056x3040 for Camera Module 3)
config = picam2.create_still_configuration(main={"size": (4056, 3040)})
picam2.configure(config)

# Start the camera
picam2.start()

# Small delay to ensure the camera is fully initialized
#####################################Time Save ###################################################3time.sleep(0.2)

# Capture the photo and save it to the specified path
picam2.capture_file(save_path)

# Close the camera after capturing the photo
picam2.close()

# Confirmation message with the path where the photo is saved
print(f"Picture Taken: {save_path}")
