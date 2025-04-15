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


if __name__ == "__main__":
    print("HISTORY_FILE:", CONSTS.HISTORY_FILE)
    print("MEMORY_FILE:", CONSTS.MEMORY_FILE)
    print("CURRENCY_API_URL:", CONSTS.CURRENCY_API_URL)
    print("SETTINGS_ICON:", CONSTS.SETTINGS_ICON)
    print("HISTORY_ICON:", CONSTS.HISTORY_ICON)
    print("CALCULATOR_ICON:", CONSTS.CALCULATOR_ICON)
