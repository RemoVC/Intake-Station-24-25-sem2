# Import the MainApplication class from interface_main.py (located in the Interface folder)
from Interface.Interface_main import MainApplication

def main():
    # Create an instance of the MainApplication
    app = MainApplication()

    # Start the Tkinter event loop (keeps the window open)
    app.mainloop()

# If this file is run directly (not imported), execute the main function
if __name__ == "__main__":
    main()
