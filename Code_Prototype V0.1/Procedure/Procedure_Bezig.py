import subprocess
import sys
import os
import time
import tkinter

if len(sys.argv) < 4:
    print("Gebruik: Procedure_Bezig.py <aantal_fotos> <object_naam> <snelheid>")
    sys.exit(1)

photo_count = int(sys.argv[1])
object_name = sys.argv[2]
speed = str(sys.argv[3])

if speed == "Med": 
    speed_value = 0.0008
elif speed == "Slow":
    speed_value = 0.0007
elif speed == "Fast":
    speed_value = 0.000005  # Bijv. een snelle snelheid



print(f"Start procedure voor object: {object_name} met {photo_count} foto's op snelheid {speed_value}.")

total_steps = 6400 * 9
steps_per_photo = total_steps // photo_count

motor_script = os.path.join("Motor", "Motor_Auto.py")
camera_script = os.path.join("Camera", "Picture_Auto.py")

for i in range(photo_count):
    print(f"Stap {i + 1}/{photo_count}: draaien en foto nemen...")


    # Foto nemen
    subprocess.run(["python3", camera_script, object_name, str(i + 1)])

    if i+1 !=  photo_count:
    # Motor draaien met stappen en snelheid
        subprocess.run(["python3", motor_script, str(steps_per_photo), str(speed)])

   

    #################### Time saving########## time.sleep(0.2)  # kleine pauze tussen foto's 
