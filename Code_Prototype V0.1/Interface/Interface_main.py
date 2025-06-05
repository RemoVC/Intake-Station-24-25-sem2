import tkinter as tk
from Interface.Home import HomeScreen      # Use relative import for home.py
from Interface.Freemode import FreeMode    # Use relative import for freemode.py
from Interface.Procedure import Procedure  # Use relative import for procedure.py
from Interface.Settings import Settings    # Use relative import for Settings.py
from Interface.Results import Results      # Use relative import for Results.py


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Intake Station V0.1")  # Set the window title
        self.geometry("450x500")  # Set the window size (can be adjusted as needed)

        # Container for the pages (frames)
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Shared data (this can also be set from a configuration file)
        self.shared_data = {
            "auto_speed": tk.StringVar(value="Med"),  # Initial speed set to "Med" (Medium)
            "manual_speed": tk.StringVar(value="Med"),  # Initial manual speed set to "Med"
            "photo_count": tk.IntVar(value=6),  # Number of photos set to 6 by default
            "speed_values": {
                "Slow": 0.0008,  # Slow speed
                "Med": 0.0001,   # Medium speed
                "Fast": 0.00005  # Fast speed
            }
        }

        self.frames = {}  # This will store the different pages (frames)

        # Create an instance of each screen and store them in self.frames
        for F in (HomeScreen, FreeMode, Procedure, Settings, Results):
            page_name = F.__name__  # Get the name of the class (e.g., 'HomeScreen')
            frame = F(parent=self.container, controller=self)  # Create an instance of the class
            self.frames[page_name] = frame  # Add the instance to the frames dictionary
            frame.grid(row=0, column=0, sticky="nsew")  # Place the frame in the container

        # Display the home screen on startup
        self.show_frame("HomeScreen")

    def show_frame(self, page_name):
        """Ensures the correct frame is shown."""
        frame = self.frames[page_name]  # Get the frame by name
        frame.tkraise()  # Raise the frame to the front

# This line ensures the application is started only if this file is run directly
if __name__ == "__main__":
    app = MainApplication()  # Create an instance of the MainApplication
    app.mainloop()  # Start the Tkinter event loop (keeping the window open)
