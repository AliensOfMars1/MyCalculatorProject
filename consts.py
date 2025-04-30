import os

class CONSTS : 
    # Get the directory of the current file (i.e. the project root if consts.py is in it)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the all_data folder 
    DATA_DIR = os.path.join(BASE_DIR, "all_data")
    
    # Defining asset paths using the BASE_DIR
    SETTINGS_ICON = os.path.join(BASE_DIR, "assets", "icons", "settingsicon.png")
    HISTORY_ICON = os.path.join(BASE_DIR, "assets", "icons", "historyicon.png")
    CALCULATOR_ICON = os.path.join(BASE_DIR, "assets", "icons", "calculator_icon.ico")
    
    # Other constants
    CURRENCY_API_URL = "https://api.exchangerate-api.com/v4/latest/USD"
    APP_TITLE = "Calculator"
    SCIENTIFIC_FUNCS = {
        "sin", "cos", "tan", "exp", "sinh", "cosh", "tanh", "expm1",
        "log", "log2", "log10", "factorial", "radians", "degrees", "sqrt", "abs"}
    # Defining the absolute paths for history and memory JSON files in all_data folder
    HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
    MEMORY_FILE = os.path.join(DATA_DIR, "memory.json")
    VERSION = "1.0.0"
    APP_AUTHOR = "CodesOfAnAlien.Org"
    APP_DESCRIPTION = "A modern, user-friendly desktop calculator application with basic and scientific functions."
    AUTHORS_EMAIL = "princemolly405@gmail.com"
    HELP_TEXT = (
        f"{APP_DESCRIPTION}.\n\n" 
        "You can perform basic arithmetic operations and scientific calculations.\n\n"
        "Use the buttons to input numbers and operations.\n\n"
        "You can enter numbers and operational sign from your keyboard.\n\n"
        "For scientific functions, toggle on the 'Switch to Scientific' button to access them.\n\n"
        "You can also view your calculation history and memory.\n\n"
        "You can convert between USD dollar and Ghana cedis.\n\n\n"
                "SHORTS CUT FOR FASTER CALCULATOR USE:\n\n"
        "ESCAPE KEY functions as CE button, clears the calculator screen.\n\n"
        "ctrl+ A or a fuctions same as clicking on ANS button, recalls last result.\n\n"
        "ctrl + T or t will switch between dark and light theme.\n\n" 
        "ctrl + H or h brings up the calculator History.\n\n"
        "backspace functions as DEL button.\n\n"
        f"Application By: {APP_AUTHOR}\n\n"
        f"Version: {VERSION}\n\n"
        f"For any questions or suggestions email {APP_AUTHOR} at: {AUTHORS_EMAIL}."
    )


if __name__ == "__main__":
    print("HISTORY_FILE:", CONSTS.HISTORY_FILE)
    print("MEMORY_FILE:", CONSTS.MEMORY_FILE)
    print("CURRENCY_API_URL:", CONSTS.CURRENCY_API_URL)
    print("SETTINGS_ICON:", CONSTS.SETTINGS_ICON)
    print("HISTORY_ICON:", CONSTS.HISTORY_ICON)
    print("CALCULATOR_ICON:", CONSTS.CALCULATOR_ICON)
