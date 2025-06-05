import tkinter as tk

class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Initialize the parent class (tk.Frame) and pass the controller to this frame
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Add a title label for the Home screen
        label = tk.Label(self, text="Welcome to the Home Screen", font=("Arial", 24))
        label.pack(pady=20)  # Add some padding around the label

        # Button to navigate to the FreeMode screen
        btn_freemode = tk.Button(self, text="Go to FreeMode", command=lambda: controller.show_frame("FreeMode"))
        btn_freemode.pack(pady=10)  # Add padding between buttons

        # Button to navigate to the Procedure screen
        btn_procedure = tk.Button(self, text="Go to Procedure", command=lambda: controller.show_frame("Procedure"))
        btn_procedure.pack(pady=10)  # Add padding between buttons

        # Button to navigate to the Settings screen
        btn_settings = tk.Button(self, text="Go to Settings", command=lambda: controller.show_frame("Settings"))
        btn_settings.pack(pady=10)  # Add padding between buttons

        # Button to navigate to the Results screen
        btn_results = tk.Button(self, text="Go to Results", command=lambda: controller.show_frame("Results"))
        btn_results.pack(pady=10)  # Add padding between buttons
