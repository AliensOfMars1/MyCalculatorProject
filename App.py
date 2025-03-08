from token import tok_name
import customtkinter as ctk
from tkinter import messagebox
import math
from PIL import Image, ImageTk
import tkinter as tk
import re
from tkinter import font
import os


# Set theme and appearance mode
ctk.set_appearance_mode("System")  # Light/Dark mode
ctk.set_default_color_theme("blue")  # Blue theme

#-----------------------------------------------Model start---------------------------------------------------
# MODEL: Handles calculations

class CalculatorModel:
    def __init__(self):
        self.memory = ""  # initialize the memory storage
        self.history_file = "history.txt"  # File for history
        self.history = self.load_history()  # Load history at startup


      # Evaluates mathematical expressions excluding built-in functions so eval() is can be safely used.      
    def evaluate(self, expression): 
        try:
            if not expression.strip():  # If the expression is empty or only spaces
                    return 0  # Return 0 instead of evaluating
            result = eval(expression, {"__builtins__": None}, {
                "sin": math.sin, "cos": math.cos, "tan": math.tan, "log": math.log,
                "sqrt": math.sqrt, "pow": math.pow, "pi": math.pi, "e": math.e,
                "cosh": math.cosh, "tanh": math.tanh, "sinh": math.sinh, "exp": math.exp,
                "log2": math.log2, "log10": math.log10, "degrees": math.degrees, "radians": math.radians,
            })
            self.memory = str(result)  # Store last result
            self.save_to_history(expression, result) # save the exp and result to history
            return result
        except Exception:
            return "Error"
        
    def save_to_history(self, expression, result):
        entry = f"{expression} = {result}\n"
        with open(self.history_file, "a") as file:
            file.write(entry)
        if self.history is None:
            self.history =[]

        self.history.append(entry.strip()) # Append a clean entry to the history list 


    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as file: #open the file in read mode 
                return file.readlines()
        return [] # If no file exists, initialize an empty list
        
    def get_history(self):
        return "".join(self.history[-10:]) if self.history else "No history available."  
        #Returns the last 10 calculations as a string. If history is empty, return a message.      


    # Removes the last entered character.
    def delete_last(self, expression):
        return expression[:-1]

    # Returns stored memory value.
    def recall_memory(self):
        return self.memory
       
    # Clears stored memory.
    def clear_memory(self):
        self.memory = ""
#-----------------------------------------------Model end-----------------------------------------------------







#-----------------------------------------------View start----------------------------------------------------
# VIEW: Handles UI

class CalculatorView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Calculator")
        self.geometry("480x600+250+40")  # Fixed UI size 
        self.iconbitmap("favicon.ico") #set the window icon
        self.resizable(width=False, height=False)


        # Bind "=" and "Return" key to execute calculations
        self.bind("<Return>", lambda event: self.controller.on_button_click("="))
        self.bind("=", lambda event: self.controller.on_button_click("="))

        # Bind "m" and "M" to recall memory
        self.bind("m", lambda event: self.controller.on_button_click("M"))
        self.bind("M", lambda event: self.controller.on_button_click("M"))

        # Entry widget to display expression / results (calculator screen)
        self.expression = ctk.StringVar()
        
        # Create validation command
        vcmd = (self.register(self.validate_input), "%P")

        self.entry = ctk.CTkEntry(
            self, textvariable=self.expression, font=("Lucida Console",24),
            height=60, corner_radius=10, justify="right",
            validate="key", validatecommand=vcmd  # Enable real-time validation
        )

        self.entry.pack(fill="both", padx=10, pady=10)
        


        #"Settings" drop-down menu
        self.settings_menu = tk.Menu(self, tearoff=0)
        self.settings_menu.add_command(label="Copy", command=self.copy_text)
        self.settings_menu.add_command(label="Cut", command=self.cut_text)
        self.settings_menu.add_command(label="Paste", command=self.paste_text)

        #Settings button
        self.settings_button = ctk.CTkButton(self, text="⚙️", width=40, height=28)
        self.settings_button.place(x=10, y=84)
        self.settings_button.configure(command=self.show_menu)

        # Mode toggle switch
        self.mode = "Standard"
        self.switch_var = ctk.StringVar(value="Standard")
        self.toggle_switch = ctk.CTkSwitch(self, text="Switch to Scientific", 
                                           command=self.toggle_mode,
                                           variable=self.switch_var, 
                                           onvalue="Scientific", offvalue="Standard")
        self.toggle_switch.pack(pady=5)

        # Frame to hold calculator buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(expand=True, fill="both")
        self.create_standard_buttons()

    # Function to create standard/basic buttons
    def create_standard_buttons(self):
        self.clear_buttons()
        button_layout = [
            ["CE", "M", "DEL", "HISTORY"],
            ["1", "2", "3", "+"],
            ["4", "5", "6", "-"],
            ["7", "8", "9", "*"],
            [".", "0", "/", "="],
        ]
        self.create_button_grid(button_layout)

    # Function to create scientific buttons
    def create_scientific_buttons(self):
        self.clear_buttons()
        button_layout = [
            ["CE", "M", "DEL", "="],
            ["1", "2", "3", "+"],
            ["4", "5", "6", "-"],
            ["7", "8", "9", "*"],
            [".", "0", "(", ")"],
            ["sin", "cos", "tan", "/"],
            ["sqrt", "log", "pi", "e"]
        ]
        self.create_button_grid(button_layout, scientific=True)

    # Creates button grid
    def create_button_grid(self, button_layout, scientific=False):
        for row in button_layout:
            row_frame = ctk.CTkFrame(self.button_frame)
            row_frame.pack(expand=True, fill="both")
            for button_text in row:
                btn = ctk.CTkButton(row_frame, text=button_text, font=("Segment7", 18),
                                    height=45 if scientific else 50,  # Adjust height for scientific mode
                                    width=80 if scientific else 90,   # Adjust width for scientific mode
                                    corner_radius=5,
                                    command=lambda text=button_text: self.controller.on_button_click(text))
                btn.pack(side="left", expand=True, fill="both", padx=4, pady=4)

    # Removes all existing buttons before updating mode.
    def clear_buttons(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

    # Toggle between Standard & Scientific Mode using the switch
    def toggle_mode(self):
        if self.switch_var.get() == "Scientific":
            self.mode = "Scientific"
            self.toggle_switch.configure(text="Switch to Standard")
            self.create_scientific_buttons()
        else:
            self.mode = "Standard"
            self.toggle_switch.configure(text="Switch to Scientific")
            self.create_standard_buttons()

    # Updates the calculator display.
    def update_display(self, text):
        self.expression.set(text)


    # Displays the settings menu at the position of the settings button.
    def show_menu(self):
        self.settings_menu.post(
            self.settings_button.winfo_rootx(),
            self.settings_button.winfo_rooty() + self.settings_button.winfo_height()
        )


    def validate_input(self, new_text):
        """Allow only numbers, operators, scientific functions, and specific letters."""
        valid_chars =  re.compile(r"^[0-9+\-*/().eπ]*$|^(sin|cos|tan|log|sqrt|exp|pow|log2|log10|cosh|tanh|sinh|degrees|radians)?$")

        
        # If new_text is empty (to allow backspacing) or matches the pattern, return True (allow input)
        return new_text == "" or bool(valid_chars.fullmatch(new_text))


    # Copy text from the entry field.
    def copy_text(self):
        self.clipboard_clear()
        self.clipboard_append(self.entry.get())
        self.update()

    # Cuts text from the entry field.
    def cut_text(self):
        self.copy_text()
        self.entry.delete(0, "end")

    # Pastes text from the clipboard into the entry field.
    def paste_text(self):
        try:
            self.entry.insert("end", self.clipboard_get())
        except tk.TclError:
            pass  # Handle empty clipboard
#-----------------------------------------------View end----------------------------------------------------







#-----------------------------------------------Controller start---------------------------------------------
# CONTROLLER: Manages interactions between Model and View

class CalculatorController:
    def __init__(self):
        self.model = CalculatorModel()
        self.view = CalculatorView(self)
    
    # Handles the button click event.
    def on_button_click(self, button_text):
        current_text = self.view.expression.get()
        if button_text == "CE":
            self.view.update_display("")  # Clears the display
        elif button_text == "DEL":
            self.view.update_display(self.model.delete_last(current_text))  # Deletes the last character
        elif button_text == "M":
            self.view.update_display(self.model.recall_memory())  # Recalls stored value
        elif button_text == "=":
            result = self.model.evaluate(current_text)
            self.view.update_display(str(result))  # Evaluates the expression and displays results
        elif button_text == "HISTORY":
            messagebox.showinfo("History", self.model.get_history()) #Displays the last 10 calculations     
        else:
            self.view.update_display(current_text + button_text) #appends the button text to the display
    # Runs the calculator.
    def run(self):
        self.view.mainloop()
#-----------------------------------------------Controller end-----------------------------------------------

# Run the Calculator
if __name__ == "__main__":
    app = CalculatorController()
    app.run()
