from .functions_script import *
from .utils import ensure_folder_exists, ho
from .gui import run_gui
def main():
# Ensure necessary folder and files are in place
    ho()

    # Launch the GUI
    run_gui()

if __name__ == "__main__":
    main()