import tkinter as tk
import os
import platform
import subprocess
import tkinter.messagebox as messagebox

class Results(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)  # Initialize the parent Frame
        self.controller = controller

        # Title label
        label = tk.Label(self, text="Results", font=("Arial", 24))
        label.pack(pady=20)

        # Button to open the folder
        btn_open_folder = tk.Button(self, text="Open Photo Folder", command=self.open_folder)
        btn_open_folder.pack(pady=10)

        # Button to go back to the Home screen
        btn_home = tk.Button(self, text="Back", command=lambda: controller.show_frame("HomeScreen"))
        btn_home.pack(pady=10)

    def open_folder(self):
        """
        Opens the folder containing result images.
        Path: /home/IntakeStation/Documents/Code_Prototype V0.1/Results
        """
        folder_path = "/home/IntakeStation/Documents/Code_Prototype V0.1/Results"

        # Check if folder exists
        if not os.path.isdir(folder_path):
            messagebox.showerror("Error", f"Folder does not exist:\n{folder_path}")
            return

        system_platform = platform.system()  # Detect OS: Windows, macOS (Darwin), or Linux

        try:
            if system_platform == "Windows":
                os.startfile(folder_path)
            elif system_platform == "Darwin":  # macOS
                subprocess.Popen(["open", folder_path])
            else:  # Linux
                subprocess.Popen(["xdg-open", folder_path])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder:\n{e}")
