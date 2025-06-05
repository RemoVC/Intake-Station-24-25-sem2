import tkinter as tk
from tkinter import messagebox
import subprocess
import os

class FreeMode(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.motor_process = None

        # Title of the FreeMode screen
        label = tk.Label(self, text="FreeMode", font=("Arial", 24))
        label.pack(pady=20)

        # Create a frame for the direction buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        # Left button to move clockwise
        self.btn_left = tk.Button(button_frame, text="Move ClockWise", command=self.toggle_left)
        self.btn_left.grid(row=0, column=0, padx=10)

        # Right button to move counterclockwise
        self.btn_right = tk.Button(button_frame, text="Move Counter ClockWise", command=self.toggle_right)
        self.btn_right.grid(row=0, column=1, padx=10)

        # Button to take a picture
        self.btn_action = tk.Button(self, text="Take Picture", command=self.do_action)
        self.btn_action.pack(pady=10)

        # Back button to go back to the Home screen
        self.btn_home = tk.Button(self, text="Back", command=lambda: controller.show_frame("HomeScreen"))
        self.btn_home.pack(pady=10)

        # Initial state of the motor and direction
        self.motor_active = False
        self.active_direction = None

    def toggle_left(self):
        # Handles the left (clockwise) button toggle
        self.handle_motor_toggle(richting=0)

    def toggle_right(self):
        # Handles the right (counterclockwise) button toggle
        self.handle_motor_toggle(richting=1)

    def handle_motor_toggle(self, richting):
        # Starts or stops the motor based on its current state
        if self.motor_active:
            self.stop_motor()
        else:
            self.start_motor(richting)

    def start_motor(self, richting):
        # Get the shared speed data from the controller
        snelheid_label = self.controller.shared_data["manual_speed"].get()
        snelheid = self.controller.shared_data["speed_values"][snelheid_label]

        # Start the motor with the specified direction and speed
        print(f"Start motor | richting: {richting} | snelheid: {snelheid}")
        self.motor_active = True
        self.disable_buttons(except_direction=richting)

        script_path = os.path.join("Motor", "Motor_Manual.py")
        
        # Start a subprocess to control the motor using an external script
        self.motor_process = subprocess.Popen(["python3", script_path, str(richting), str(snelheid)])

    def stop_motor(self):
        # Stop the motor and reset the process
        if self.motor_process:
            self.motor_process.terminate()
            self.motor_process = None
            
            print("Motor stopped")

        self.motor_active = False
        self.enable_all_buttons()

    def disable_buttons(self, except_direction=None):
        # Disable all buttons except for the direction that is active
        self.btn_left.config(state="disabled")
        self.btn_right.config(state="disabled")
        self.btn_action.config(state="disabled")
        self.btn_home.config(state="disabled")

        # Highlight the active direction button
        if except_direction == 0:
            self.btn_left.config(state="normal", relief="sunken")
        elif except_direction == 1:
            self.btn_right.config(state="normal", relief="sunken")

    def enable_all_buttons(self):
        # Re-enable all buttons after stopping the motor
        self.btn_left.config(state="normal", relief="raised")
        self.btn_right.config(state="normal", relief="raised")
        self.btn_action.config(state="normal")
        self.btn_home.config(state="normal")

    def do_action(self):
        # Call the function to take a picture
        self.capture_photo()

    def capture_photo(self):
        # Start a subprocess to call an external script to take a picture
        script_path = os.path.join("Camera", "Take_Picture.py")
        
        try:
            subprocess.Popen(["python3", script_path])
            print("Take picture started")
            messagebox.showinfo("Take Picture", "Picture Has been taken")
        except Exception as e:
            # Handle any errors in starting the script
            print(f"An error occurred while starting the script: {e}")
            messagebox.showerror("Error", f"Error taking the picture: {e}")

    def tkraise(self, aboveThis=None):
        # Raise the current frame
        super().tkraise(aboveThis)
