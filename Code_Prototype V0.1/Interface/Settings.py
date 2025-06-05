import tkinter as tk
from tkinter import messagebox
from picamera2 import Picamera2, Preview

class Settings(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Link shared_data variables from the main app
        self.auto_speed = controller.shared_data["auto_speed"]
        self.manual_speed = controller.shared_data["manual_speed"]
        self.photo_count = controller.shared_data["photo_count"]
        self.speed_values = controller.shared_data["speed_values"]

        # Title label
        tk.Label(self, text="Settings", font=("Arial", 16)).pack(pady=10)

        # AUTO Settings
        auto_frame = tk.LabelFrame(self, text="Procedure Settings", padx=10, pady=10)
        auto_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(auto_frame, text="Speed:").grid(row=0, column=0, sticky="w")
        tk.OptionMenu(auto_frame, self.auto_speed, "Slow", "Med", "Fast").grid(row=0, column=1, sticky="w")

        tk.Label(auto_frame, text="Amount of pictures:").grid(row=1, column=0, sticky="w")
        tk.Entry(auto_frame, textvariable=self.photo_count, width=5).grid(row=1, column=1, sticky="w")

        # MANUAL Settings
        manual_frame = tk.LabelFrame(self, text="FreeMode Settings", padx=10, pady=10)
        manual_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(manual_frame, text="Speed:").grid(row=0, column=0, sticky="w")
        tk.OptionMenu(manual_frame, self.manual_speed, "Slow", "Med", "Fast").grid(row=0, column=1, sticky="w")
        
        # Information block
        info_frame = tk.Frame(self)
        info_frame.pack(pady=10)
        tk.Label(info_frame, text="ℹ Gear ratio = 9 | Microstepping = 6400", fg="gray").pack()

        # SET button
        set_button = tk.Button(self, text="SET", command=self.set_values, bg="green", fg="white")
        set_button.pack(pady=10)

        # Preview button to show camera feed
        preview_button = tk.Button(self, text="Preview Camera", command=self.preview_camera, bg="blue", fg="white")
        preview_button.pack(pady=5)

        # Back button to return to Home screen
        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame("HomeScreen"))
        back_button.pack(pady=5, anchor="w", padx=20)

    def set_values(self):
        # Values are automatically updated via StringVar and IntVar bindings
        messagebox.showinfo("Settings Saved",
                            f"Procedure speed: {self.auto_speed.get()}\n"
                            f"FreeMode speed: {self.manual_speed.get()}\n"
                            f"Pictures: {self.photo_count.get()}")

    def preview_camera(self):
        try:
            picam2 = Picamera2()

            # Configure the camera with the highest resolution
            config = picam2.create_preview_configuration(main={"size": (4056, 3040)})
            picam2.configure(config)

            picam2.start_preview(Preview.QTGL)  # Use QTGL preview for better performance
            picam2.start()

            # Info popup and instructions
            messagebox.showinfo("Preview", "CLOSE PREVIEW WITH THIS")

            # Preview will stay active until the user closes it
            picam2.stop_preview()
            picam2.close()

        except Exception as e:
            messagebox.showerror("Camera Error", f"Failed to open camera:\n{e}")
