from picamera2 import Picamera2
import time
import os

def capture_photo():
    # Directory for saving photos
    photo_directory = "/home/IntakeStation/Documents/Code_Prototype V0.1/Results/FreeMode"
    
    # Timestamp for the filename
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    photo_filename = f"photo_Freemode_{timestamp}.jpg"

    # Check if the directory exists, if not, create it
    if not os.path.exists(photo_directory):
        os.makedirs(photo_directory)

    # Complete path for saving the photo
    photo_path = os.path.join(photo_directory, photo_filename)

    # Initialize Picamera2
    picam2 = Picamera2()

    # Configure the camera for high resolution (4056x3040 for 12MP)
    config = picam2.create_still_configuration(main={"size": (4056, 3040)})
    picam2.configure(config)

    # Start the camera
    picam2.start()

    # Capture the photo with the configured resolution
    picam2.capture_file(photo_path)

    # Close the camera after capturing the image
    picam2.close()

    print(f"Picture Saved: {photo_path}")
    return photo_path

if __name__ == "__main__":
    capture_photo()
