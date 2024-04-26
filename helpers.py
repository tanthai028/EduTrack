import os
import platform

def clear_screen():
    """Clear the console based on the operating system."""
    if platform.system() == "Windows":
        os.system('cls')  # Clears the console for Windows
    else:
        os.system('clear')  # Clears the console for Unix/Linux/MacOS

