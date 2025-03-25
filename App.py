from token import tok_name
import customtkinter as ctk
from tkinter import messagebox
import math
from PIL import Image, ImageTk
import tkinter as tk
import re
from tkinter import font
import os
import json
import requests # for API calls 
from const import CONSTS
import threading


# Set theme and appearance mode
ctk.set_appearance_mode("System")  # Light/Dark mode
ctk.set_default_color_theme("blue")  # Blue theme

#-----------------------------------------------Model start---------------------------------------------------
# MODEL: Handles calculations

class CalculatorModel:
    def __init__(self):
        self.memory = ""  # initialize the memory storage
        self.history_file = "history.json"  # File for history
        self.history = self.load_history()  # Load history at startup
        self.memory_file = "memory.json" #file for memory storage
        # self.memory_stack= self.load_memory() #load memory at startup

    def fetch_live_usd_to_ghs_rate(self):
        try:
            response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
            data = response.json()
            live_rate = data["rates"].get("GHS")
            if live_rate:
                return live_rate
            else:
                raise ValueError("GHS rate not found in API response.")
        except Exception as e:
            messagebox.showerror("No internet connection.", "Failed to get live rate. \nPLEASE CHECK YOUR INTERNET CONNECTION!")

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
                "expm1" : math.expm1 , "pow": math.pow, "factorial" : math.factorial
            })
            self.memory = str(result)  # Store last result
            self.save_to_history(expression, result) # save the exp and result to history
            return result
        except SyntaxError:
            messagebox.showinfo("ERROR", "Syntax Error: Check expression format!")
        except ZeroDivisionError:
            messagebox.showinfo("ERROR", "Math Error: Division by zero!") 
        except ValueError:
            messagebox.showinfo("ERROR", "Math Error: Invalid input for function!")
        except TypeError:
            messagebox.showinfo("ERROR", "Type Error: Incorrect number format!")
        except AttributeError:
            messagebox.showinfo("ERROR", "Function Error: Invalid operation!") 
        except Exception as e:
            return f"Error: {str(e)}"


    def save_to_history(self, expression, result):
        entry = {"expression": expression, "result": result}
        history = self.load_history()
        history.append(entry)
        with open(self.history_file, "w") as file:
            json.dump(history, file, indent=4)

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []
        return []

    def get_history(self):
        return "\n".join([f"{entry['expression']} = {entry['result']}" for entry in self.history[-10:]]) if self.history else "No history available."

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []
        return [] # If no file exists, initialize an empty list

    def load_stack(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as file:  # Open the file in read mode
                try:
                    return json.load(file)  # Load JSON data
                except json.JSONDecodeError:
                    return []  # If the file is empty or corrupt, return an empty list
        return []  # If no file exists, initialize an empty list
    
    # Function to save the stack to the JSON file
    def save_stack(self, stack):
        with open(self.memory_file, "w") as file:
            json.dump(stack, file, indent=4)

    # Adds a value to the memory stack (M+).
    def memory_plus(self, value):
        stack = self.load_stack()
        stack.append(value)
        self.save_stack(stack)
    
    # Retrieves and removes the latest value from the memory stack (M-).
    def memory_minus(self):
        stack = self.load_stack()
        if not stack:  # Check if the list is empty
            messagebox.showinfo("EMPTY STACK", "Oops! Memory stack is empty.")
            return ""  # Return an empty string instead of causing an error
        
        latest_value = stack.pop()  # Get and remove the last stored value
        self.save_stack(stack)
        return latest_value
    
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
        self.geometry("480x600+600+40")  # Fixed UI size 
        self.iconbitmap(CONSTS.CALCULATOR_ICON) #set the window icon
        self.resizable(width=False, height=False)

        # Load the history icon image.
        self.HISTORY_ICON = ctk.CTkImage( 
            light_image = Image.open(CONSTS.HISTORY_ICON),
            # light_image=Image.open("historyicon.png"),
            dark_image=Image.open(r"C:\Users\USER\OneDrive\Desktop\9980 Calculator\assets\icons\historyicon.png"),
            size=(20, 20)
        )
        # Load the history icon image.
        self.SETTINGS_ICON = ctk.CTkImage(
            light_image=Image.open(CONSTS.SETTINGS_ICON),
            dark_image=Image.open(CONSTS.SETTINGS_ICON),
            size=(20, 20)
        )
     #.....................................key bindings...............................................
        #bind escape key to clear the display 
        self.bind("<Escape>", lambda event: self.controller.on_button_click("CE"))
        # Bind "h" or "H" to show history 
        self.bind( "H", lambda event: messagebox.showinfo("History", self.controller.model.get_history()))
        self.bind( "h", lambda event: messagebox.showinfo("History", self.controller.model.get_history()))
        # Bind "=" and "Return" key to execute calculations
        self.bind("<Return>", lambda event: self.controller.on_button_click("="))
        self.bind("=", lambda event: self.controller.on_button_click("="))
        # Bind "m" and "M" to recall memory
        self.bind("A", lambda event: self.controller.on_button_click("ANS"))
        self.bind("a", lambda event: self.controller.on_button_click("ANS"))

        # Entry widget to display expression / results (calculator screen)
        self.expression = ctk.StringVar() 
        vcmd = (self.register(self.validate_input), "%P") # Create validation command
        self.entry = ctk.CTkEntry(
            self, textvariable=self.expression, font=("Lucida Console",24),
            height=60, corner_radius=10, justify="right",
            validate="key", validatecommand=vcmd  # Enable real-time validation
        )
        
        # Bind events to keep the cursor at the left
        self.entry.pack(fill="both", padx=10, pady=10)
        self.entry.after(1000, lambda: self.entry.focus_force())
        self.entry.bind("<FocusIn>", self.force_cursor_right)  # Keeps cursor at right when focused


        # A right-click context menu
        self.context_menu = tk.Menu(self, tearoff=0) # 
        self.context_menu.add_command(label="Cut", command=self.cut_text)
        self.context_menu.add_command(label="Copy", command=self.copy_text)
        self.context_menu.add_command(label="Paste", command=self.paste_text)
        self.context_menu.add_separator()  # Separator line
        self.context_menu.add_command(label="Clear History", command=self.controller.clear_history)

        # Binding right-click event to show the menu
        self.entry.bind("<Button-3>", self.show_context_menu)  # Windows/Linux
        self.entry.bind("<Control-Button-1>", self.show_context_menu) # MacOS        

        #"Settings" drop-down menu
        self.settings_menu = tk.Menu(self, tearoff=0)
        self.settings_menu.add_command(label="Copy", command=self.copy_text)
        self.settings_menu.add_command(label="Cut", command=self.cut_text)
        self.settings_menu.add_command(label="Paste", command=self.paste_text)
        self.settings_menu.add_command(label="Clear History", command=self.controller.clear_history)
        self.settings_menu.add_separator()  # Optional separator for clarity
        self.settings_menu.add_command(label="Click To Change Theme", command=self.toggle_theme)

        #Settings button
        self.settings_button = ctk.CTkButton(self, text="",image= self.SETTINGS_ICON, width=40, height=28)
        self.settings_button.place(x=10, y=84)
        self.settings_button.configure(command=self.show_menu)
        
        #History button 
        self.history_button = ctk.CTkButton(self, text="", image= self.HISTORY_ICON, width=40, height= 28)
        self.history_button.place(x=430, y=84)
        self.history_button.configure(command=self.show_scrollable_history_window)

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

        # ---- NEW: Loading Animation Variables ----
        self.loading = False
        self.loading_dots = ["", ".", "..", "..."]
        self.loading_index = 0

    def force_cursor_right(self, event):
           self.entry.icursor(ctk.END)  # Moves cursor to the end (rightmost position) 

    def show_scrollable_history_window(self):
        # Check if the toplevel window already exists
        if hasattr(self, "history_window") and self.history_window.winfo_exists():
            self.history_window.lift()  # Bring it to the front
            return  # Exit the function if the window is already open

        # Create a new Toplevel window for the history
        self.history_window = ctk.CTkToplevel()
        self.history_window.title("History")
        self.history_window.geometry("300x400")

        # Set the window as transient so it stays on top of the main window
        self.history_window.transient(self)
        self.history_window.grab_set()  # Prevents interaction with the main window until closed
        self.history_window.attributes("-topmost", True)  # Forces it to be on top
        self.history_window.lift()  # Bring to front
        self.history_window.focus_force()  # Ensure it gets focus

        # Text widget to display history
        text_widget = ctk.CTkTextbox(self.history_window, width=280, height=350, wrap="word", font=("Arial", 14))
        text_widget.pack(pady=10, padx=10, fill="both", expand=True)

        # Retrieve history from the model (which now loads from JSON)
        history_text = self.controller.model.get_history()
        text_widget.insert("1.0", history_text)

        # Make the text read-only
        text_widget.configure(state="disabled")    

    # Function to create standard/basic buttons with added M+ and M- buttons.
    def create_standard_buttons(self):
        self.clear_buttons()
        button_layout = [
            ["CE", "ANS", "DEL", "="],
            ["1", "2", "3", "+"],
            ["4", "5", "6", "-"],
            ["7", "8", "9", "*"],
            [".", "0", ",", "/"],
            ["M+", "M-"],           
        ]
        self.create_button_grid(button_layout)

    def create_scientific_buttons(self):
        self.clear_buttons()
        button_layout = [
            ["CE", "ANS", "DEL", "=","sin", "cos", "tan", "exp"],
            ["1", "2", "3" ,"+","sinh", "cosh", "tanh", "expm1"],
            ["4", "5", "6","-","log", "log2", "log10", "factorial"],
            ["7", "8", "9","*","radians","degrees", "sqrt", "pow"],
            [".", "0", ",", "/","e", "pi","(", ")"],
            ["M+", "M-" ,"USD-GHS", "GHS-USD"],              
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

    def update_geometry(self): #Update the window size based on the mode such that the buttons fit
        if self.mode == "Scientific":
            self.geometry("1000x600+200+40")
        else:
            self.geometry("480x600+600+40")

    def update_history_button_position(self): #Update the history button position based on the mode so it fits
        if self.mode == "Scientific":
            self.history_button.place(x=950, y=84)
        else:
            self.history_button.place(x=430, y=84)        

    # Toggle between Standard & Scientific Mode using the switch
    def toggle_mode(self):
        if self.switch_var.get() == "Scientific":
            self.mode = "Scientific"
            self.update_geometry()  # Update UI size for scientific mode
            self.toggle_switch.configure(text="Switch to Standard")
            self.create_scientific_buttons()
            self.update_history_button_position()
        else:
            self.mode = "Standard"
            self.update_geometry()  # Update UI size for scientific mode
            self.toggle_switch.configure(text="Switch to Scientific")
            self.create_standard_buttons()
            self.update_history_button_position()
 
    # Updates the calculator display.
    def update_display(self, text):
        self.expression.set(text)
        current_text = self.expression.get() #To handle the returning of None after an Error 
        if current_text == "None":
            self.update_display("")  

            
    # Displays the settings menu at the position of the settings button.
    def show_menu(self):
        self.settings_menu.post(
            self.settings_button.winfo_rootx(),
            self.settings_button.winfo_rooty() + self.settings_button.winfo_height()
        )

    def show_context_menu(self, event):
        # Create the right-click menu
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Cut", command=self.cut_text)
        menu.add_command(label="Copy", command=self.copy_text)
        menu.add_command(label="Paste", command=self.paste_text)
        menu.add_separator()
        menu.add_command(label="Clear History", command=self.controller.clear_history)
        menu.tk_popup(event.x_root, event.y_root) # Display menu at mouse position
        

        # Create validation command
    def validate_input(self, new_text):
        #Allow only numbers, operators, scientific functions, and specific letters.
        valid_chars =  re.compile(r"^[0-9+\-*/().eπ]*$|^(sin|cos|tan|log|sqrt|exp|pow|log2|log10|cosh|tanh|expm1|pow|factorial|sinh|degrees|radians)?$")
      
        # If new_text is empty (to allow backspacing) or matches the pattern, return True (allow input)
        return new_text == "" or bool(valid_chars.fullmatch(new_text))

    #Show the right-click menu at the cursor position.
    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

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

    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()  # Get current mode ("Light" or "Dark" or "System")
        # Toggle to the opposite theme (ignoring "System" for simplicity)
        if current_mode == "Dark":
            new_mode = "Light"
        else:
            new_mode = "Dark"
        ctk.set_appearance_mode(new_mode)
        messagebox.showinfo("THEME",f"Theme switched to {new_mode}")        

    # Loading Animation Methods ----
    def start_loading_animation(self):
        self.loading = True
        self.loading_index = 0
        self.animate_loading()

    def animate_loading(self):
        if self.loading:
            self.update_display(f"Loading{self.loading_dots[self.loading_index]}")
            self.loading_index = (self.loading_index + 1) % len(self.loading_dots)
            self.after(500, self.animate_loading)

    def stop_loading_animation(self):
        self.loading = False           


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
        elif button_text == "ANS":
            self.view.update_display(self.model.recall_memory())  # Recalls stored value
        elif button_text == "=":
            result = self.model.evaluate(current_text)
            self.view.update_display(str(result))  # Evaluates the expression and displays results
        elif button_text == "M+":  # Add current display value to memory stack
            value = self.view.expression.get()
            self.model.memory_plus(value)
            # Optionally, clear display or notify the user
            self.view.update_display("")
        elif button_text == "M-":  # Retrieve the latest value from memory stack
            retrieved = self.model.memory_minus()
            self.view.update_display(retrieved)

        # --- NEW: Live currency conversion with loading animation ---
        elif button_text == "USD-GHS":
            try:
                usd_value = float(current_text)
            except ValueError:
                messagebox.showerror("Conversion Error", "Please enter a valid numeric value for USD.")
                return
            self.view.start_loading_animation()
            thread = threading.Thread(target=self.convert_usd_to_ghs, args=(usd_value,))
            thread.start()
        elif button_text == "GHS-USD":
            try:
                ghs_value = float(current_text)
            except ValueError:
                messagebox.showerror("Conversion Error", "Please enter a valid numeric value for GHS.")
                return
            self.view.start_loading_animation()
            thread = threading.Thread(target=self.convert_ghs_to_usd, args=(ghs_value,))
            thread.start()

        elif button_text== "sin":
            self.view.update_display("sin(")
        elif button_text== "cos":
            self.view.update_display("cos(")            
        elif button_text== "tan":
            self.view.update_display("tan(")
        elif button_text== "exp":
            self.view.update_display("exp(")
        elif button_text== "sinh":
            self.view.update_display("sinh(")
        elif button_text== "cosh":
            self.view.update_display("cosh(")  
        elif button_text== "tanh":
            self.view.update_display("tanh(")  
        elif button_text== "expm1":
            self.view.update_display("expm1(")  
        elif button_text== "log":
            self.view.update_display("log(")  
        elif button_text== "log2":
            self.view.update_display("log2(")  
        elif button_text== "cos":
            self.view.update_display("cos(")  
        elif button_text== "log10":
            self.view.update_display("log10(")  
        elif button_text== "factorial":
            self.view.update_display("factorial(")  
        elif button_text== "radians":
            self.view.update_display("radians(")
        elif button_text== "degrees":
            self.view.update_display("degrees(")               
        elif button_text== "sqrt":
            self.view.update_display("sqrt(")  
        elif button_text== "pow":
            self.view.update_display("pow(")                                                                                                                                                                                                                     
        else:
            self.view.update_display(current_text + button_text) #appends the button text to the display

    # NEW: Conversion methods run in separate threads
    def convert_usd_to_ghs(self, usd_value):
        live_rate = self.model.fetch_live_usd_to_ghs_rate()
        if live_rate:
            ghs_value = usd_value * live_rate
            result_text = f"₵{ghs_value:.2f}"
        else:
            result_text = ""
        self.view.after(0, lambda: self.finish_conversion(result_text))

    def convert_ghs_to_usd(self, ghs_value):
        live_rate = self.model.fetch_live_usd_to_ghs_rate()
        if live_rate:
            usd_value = ghs_value / live_rate
            result_text = f"${usd_value:.2f}"
        else:
            result_text = ""
        self.view.after(0, lambda: self.finish_conversion(result_text))

    def finish_conversion(self, result_text):
        self.view.stop_loading_animation()
        self.view.update_display(result_text)

    # Clears the history and notifies the user when the "clear History button is clicked"
    def clear_history(self):
        # Ask the user to confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to clear the history?")
        if confirm:
            self.model.clear_history()
            messagebox.showinfo("History", "Calculation history cleared successfully!")

    def run(self):
        self.view.mainloop()
#-----------------------------------------------Controller end-----------------------------------------------

# Run the Calculator
if __name__ == "__main__":
    app = CalculatorController()
    app.run()
