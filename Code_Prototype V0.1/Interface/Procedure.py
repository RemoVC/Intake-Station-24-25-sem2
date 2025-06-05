import tkinter as tk
from tkinter import messagebox  # Added for messagebox functionality
import os
import subprocess

class Procedure(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Title label
        label = tk.Label(self, text="Procedure", font=("Arial", 24))
        label.pack(pady=20)

        # Info label (this will be filled in by update_info_display)
        self.info_label = tk.Label(self, text="", font=("Arial", 12), fg="gray")
        self.info_label.pack(pady=10)

        self.update_info_display()  # ← Display chosen settings when the frame is opened

        # Product ID entry field
        tk.Label(self, text="Product ID:").pack()
        self.object_name = tk.StringVar()
        self.object_entry = tk.Entry(self, textvariable=self.object_name)
        self.object_entry.pack(pady=5)

        # Confirm button to validate object name
        tk.Button(self, text="Confirm", command=self.confirm_object).pack(pady=5)

        # Start Procedure button, initially disabled
        self.btn_start = tk.Button(self, text="Start Procedure", command=self.start_procedure, state="disabled")
        self.btn_start.pack(pady=10)

        # Back button to navigate to Home
        btn_home = tk.Button(self, text="Back", command=lambda: controller.show_frame("HomeScreen"))
        btn_home.pack(pady=10)

    def update_info_display(self):
        # Update the info label with the chosen speed and number of photos
        speed = self.controller.shared_data["auto_speed"].get()
        count = self.controller.shared_data["photo_count"].get()
        self.info_label.config(text=f"Chosen speed: {speed}\nAmount of pictures: {count}")

    def confirm_object(self):
        # Confirm that the object name is not empty
        name = self.object_name.get().strip()
        if not name:
            messagebox.showwarning("Empty", "Fill in a name.")  # Show warning if name is empty
        else:
            print(f"Object name confirmed: {name}")
            # Enable the "Start Procedure" button once the name is valid
            self.btn_start.config(state="normal")

    def tkraise(self, aboveThis=None):
        # Raise this frame to the top and update the info display
        super().tkraise(aboveThis)
        self.update_info_display()  # Update info when frame is brought to the front

    def start_procedure(self):
        # Start the procedure and get values like photo count, speed, and object name
        print("Procedure started")

        photo_count = self.controller.shared_data["photo_count"].get()
        selected_speed = self.controller.shared_data["auto_speed"].get()
        object_name = self.object_name.get().strip()

        # Create a pop-up window while the procedure is running
        self.popup = tk.Toplevel(self)
        self.popup.title("Procedure")
        tk.Label(self.popup, text="Procedure is busy...", font=("Arial", 14)).pack(padx=20, pady=10)
        btn_stop = tk.Button(self.popup, text="STOP", fg="white", bg="red", command=self.stop_procedure)
        btn_stop.pack(pady=10)

        # Start the external Python script with arguments
        script_path = os.path.join("Procedure", "Procedure_Bezig.py")
        try:
            self.procedure_process = subprocess.Popen([
              "python3", script_path, str(photo_count), object_name, str(selected_speed)
            ])
            self.check_process_done()
        except Exception as e:
            messagebox.showerror("Error", f"Can't start procedure:\n{e}")  # Show error if script fails
            self.popup.destroy()

    def stop_procedure(self):
        # Stop the procedure if running and close the pop-up
        if hasattr(self, 'procedure_process') and self.procedure_process:
            self.procedure_process.terminate()
            print("Procedure Interrupted")
        if hasattr(self, 'popup') and self.popup:
            self.popup.destroy()

    def check_process_done(self):
        # Check if the external process is done
        if self.procedure_process.poll() is not None:
            # Process is finished, close the pop-up and show success message
            self.popup.destroy()
            messagebox.showinfo("FINISHED", "The procedure has finished.")
        else:
            # Re-check after 500ms if process is still running
            self.after(500, self.check_process_done)
