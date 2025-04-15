import re
import tkinter as tk
from tkinter import messagebox, font
from PIL import Image, ImageTk
import customtkinter as ctk
from const import CONSTS  # CONSTS is defined in const.py

class CalculatorView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Calculator")
        self.geometry("480x600+600+40")
        self.iconbitmap(CONSTS.CALCULATOR_ICON)
        self.resizable(width=False, height=False)

        # Load icon images
        self.HISTORY_ICON = ctk.CTkImage(
            light_image=Image.open(CONSTS.HISTORY_ICON),
            dark_image=Image.open(CONSTS.HISTORY_ICON),
            size=(20, 20)
        )
        self.SETTINGS_ICON = ctk.CTkImage(
            light_image=Image.open(CONSTS.SETTINGS_ICON),
            dark_image=Image.open(CONSTS.SETTINGS_ICON),
            size=(20, 20)
        )

        # --------------------------------------------Key bindings

        #bind escape key to clear the display 
        self.bind("<Escape>", lambda event: self.controller.on_button_click("CE"))

        # Binding ctrl plus "h" or "H" to show history
        self.bind("<Control-H>", lambda event: self.show_scrollable_history_window())
        self.bind("<Control-h>", lambda event: self.show_scrollable_history_window())

        #binding ctrl plus T or t to switch between light and dark mode
        self.bind("<Control-T>", lambda event: self.toggle_theme())
        self.bind("<Control-t>", lambda event: self.toggle_theme())

        #Binding backspace to delete the last entered character 
        self.bind("<BackSpace>", lambda event: self.controller.on_button_click("DEL"))

        # Bind "=" and "Return" key to execute calculations
        self.bind("<Return>", lambda event: self.controller.on_button_click("="))
        self.bind("=", lambda event: self.controller.on_button_click("="))

        # Binding ctrl plus "A" and "a" to copy text
        self.bind("<Control-A>", lambda event: self.controller.on_button_click("ANS"))
        self.bind("<Control-a>", lambda event: self.controller.on_button_click("ANS"))

        # Binding ctrl plus "C" and "c" to recall ANS (last result)
        self.bind("<Control-c>", lambda event: self.copy_text())
        self.bind("<Control-C>", lambda event: self.copy_text())

        # Binding ctrl plus "v" and "V" to paste
        self.bind("<Control-v>", lambda event: self.paste_text())
        self.bind("<Control-V>", lambda event: self.paste_text())

        # Binding ctrl plus "x" and "X" to paste
        self.bind("<Control-x>", lambda event: self.cut_text())
        self.bind("<Control-X>", lambda event: self.cut_text())



        # Entry widget for expression / results
        self.expression = ctk.StringVar()
        """ Using validating command to prevent random entry into the calculator so only that numbers and simple operations 
        can be entered from the keyboard and the cursor can still be used to navigate expression on the screen for seamless user experience 
         rather than simply configuring the entry state to 'disabled' which make app too rigid such that if there is a slight mis-entered value
          user need to delete to the part to correct the experession instead of sinmply moving the curser to that specific character. """
        # Create validation command        
        validating_entry_input = (self.register(self.validate_input), "%P")
        self.entry = ctk.CTkEntry(
            self, textvariable=self.expression, font=("Lucida Console", 24),
            height=60, corner_radius=10, justify="right",
            validate="key", validatecommand=validating_entry_input
        )
        self.entry.pack(fill="both", padx=10, pady=10)


        current_mode = ctk.get_appearance_mode()  # Get current mode ("Light" or "Dark")
        new_mode = "Light" if current_mode == "Dark" else "Dark"
        # A right-click context menu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Cut", command=self.cut_text)
        self.context_menu.add_command(label="Copy", command=self.copy_text)
        self.context_menu.add_command(label="Paste", command=self.paste_text)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Clear History", command=self.controller.clear_history)
        self.context_menu.add_separator()
        self.context_menu.add_command(label=f'"Switch To {new_mode}"', command=self.toggle_theme)
        self.entry.bind("<Button-3>", self.show_context_menu)
        self.entry.bind("<Control-Button-1>", self.show_context_menu)

        # Settings drop down menu
        self.settings_menu = tk.Menu(self, tearoff=0)
        self.settings_menu.add_command(label="Copy", command=self.copy_text)
        self.settings_menu.add_command(label="Cut", command=self.cut_text)
        self.settings_menu.add_command(label="Paste", command=self.paste_text)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(label="Clear History", command=self.controller.clear_history)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(label=f"Switch To {new_mode}", command=self.toggle_theme)

        # Settings button
        self.settings_button = ctk.CTkButton(self, text="", image=self.SETTINGS_ICON, width=40, height=28)
        self.settings_button.place(x=10, y=84)
        self.settings_button.configure(command=self.show_menu)

        # History button
        self.history_button = ctk.CTkButton(self, text="", image=self.HISTORY_ICON, width=40, height=28)
        self.history_button.place(x=430, y=84)
        self.history_button.configure(command=self.show_scrollable_history_window)

        # Mode toggle switch
        self.mode = "Standard"
        self.switch_var = ctk.StringVar(value="Standard")
        self.toggle_switch = ctk.CTkSwitch(
            self, text="Switch to Scientific",
            command=self.toggle_mode,
            variable=self.switch_var,
            onvalue="Scientific", offvalue="Standard"
        )
        self.toggle_switch.pack(pady=5)

        # Frame to hold calculator buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(expand=True, fill="both")
        self.create_standard_buttons()

        # Loading Animation Variables
        self.loading = False
        self.loading_dots = ["", ".", "..", "..."]
        self.loading_index = 0

    def show_scrollable_history_window(self):
        # Check if the toplevel window already exists
        if hasattr(self, "history_window") and self.history_window.winfo_exists():
            self.history_window.lift() # Bring it to the front
            return  # Exit the function if the window is already open
        self.history_window = ctk.CTkToplevel()
        self.history_window.title("History")
        self.history_window.geometry("200x300")
        # Set the window as transient so it stays on top of the main window
        self.history_window.transient(self)
        self.history_window.attributes("-topmost", True)  # Forces it to be on top
        self.history_window.lift() # Bring to front
        self.history_window.focus_force()
        # Create a scrollable textbox
        text_widget = ctk.CTkTextbox(self.history_window, width=480, height=350, wrap="word", font=("Arial", 14))
        text_widget.pack(pady=10, padx=10, fill="both", expand=True)

        # Get the history from the model and insert it
        history_text = self.controller.model.get_history()
        text_widget.insert("1.0", history_text if history_text else "No history available.")

        text_widget.configure(state="disabled") # Make the text read-only

# Function to create standard/basic buttons and memory [M+, M-] buttons.
    def create_standard_buttons(self):
        self.clear_buttons()
        button_layout = [
            ["CE", "ANS", "DEL", "="],
            ["1", "2", "3", "+"],
            ["4", "5", "6", "-"],
            ["7", "8", "9", "x"],
            [".", "0", " +/- ", "/"],
            ["M+", "M-"],
        ]
        self.create_button_grid(button_layout)

# Function to create scientific buttons, currency exchange and memory [M+, M-] buttons.
    def create_scientific_buttons(self):
        self.clear_buttons()
        button_layout = [
            ["CE", "ANS", "DEL", "=","sin", "cos", "tan", "exp"],
            ["1", "2", "3" ,"+","sinh", "cosh", "tanh", "expm1"],
            ["4", "5", "6","-","log", "log2", "log10", "factorial"],
            ["7", "8", "9","x","radians","abs", "sqrt", "degrees"],
            [".", "0", " +/- ", "/","e", "pi","(", ")"],
            ["M+", "M-" ,"USD-GHS", "GHS-USD"],
        ]
        self.create_button_grid(button_layout, scientific=True)

    # Creates button grid
    def create_button_grid(self, button_layout, scientific=False):
        for row in button_layout:
            row_frame = ctk.CTkFrame(self.button_frame)
            row_frame.pack(expand=True, fill="both")
            for button_text in row:
                btn = ctk.CTkButton(
                    row_frame,
                    text=button_text,
                    font=("Segment7", 18),
                    height=45 if scientific else 50,
                    width=80 if scientific else 90,
                    corner_radius=5,
                    command=lambda text=button_text: self.controller.on_button_click(text)
                )
                btn.pack(side="left", expand=True, fill="both", padx=4, pady=4)

    # Removes all existing buttons before updating mode.
    def clear_buttons(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

 #Update the window size based on the mode such that the buttons fit
    def update_geometry(self):
        if self.mode == "Scientific":
            self.geometry("1000x600+200+40")
            self.history_button.place(x=950, y=84)
        else:
            self.geometry("480x600+600+40")
            self.history_button.place(x=430, y=84)

    # Toggle between Standard & Scientific Mode using the switch
    def toggle_mode(self):
        if self.switch_var.get() == "Scientific":
            self.mode = "Scientific"
            self.update_geometry()
            self.toggle_switch.configure(text="Switch to Standard")
            self.create_scientific_buttons()
        else:
            self.mode = "Standard"
            self.update_geometry()
            self.toggle_switch.configure(text="Switch to Scientific")
            self.create_standard_buttons()

    # Updates the calculator display.
    def update_display(self, text):
        self.expression.set(text)
        current_text = self.expression.get()
        # Some exception after being handled return "None" on the screen; this check and remove the None
        if current_text == "None":
            self.update_display("")

    # Displays the settings menu at the position of the settings button.
    def show_menu(self):
        self.settings_menu.post(
            self.settings_button.winfo_rootx(),
            self.settings_button.winfo_rooty() + self.settings_button.winfo_height()
        )

        # right-click menu drop down
    def show_context_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Cut", command=self.cut_text)
        menu.add_command(label="Copy", command=self.copy_text)
        menu.add_command(label="Paste", command=self.paste_text)
        menu.add_separator()
        menu.add_command(label="Clear History", command=self.controller.clear_history)
        menu.tk_popup(event.x_root, event.y_root)

    #validation command that allows only digits, basic arithmetic operators, parentheses, and a decimal point.
    def validate_input(self, new_text):
        valid_chars = re.compile(r"^[0-9+\-*/().]*$")
        return new_text == "" or bool(valid_chars.fullmatch(new_text))

    def copy_text(self):
        self.clipboard_clear()
        self.clipboard_append(self.entry.get())
        self.update()

    def cut_text(self):
        self.copy_text()
        self.entry.delete(0, "end")

    def paste_text(self):
        try:
            self.entry.insert("end", self.clipboard_get())
        except tk.TclError:
            pass

    # def toggle_theme(self):
    #     current_mode = ctk.get_appearance_mode()  # Get current mode ("Light" or "Dark")
    #     new_mode = "Light" if current_mode == "Dark" else "Dark"
    #     ctk.set_appearance_mode(new_mode)
    #     # Update the settings menu to reflect the new mode 
    #     self.settings_menu.configure(5, label=f"Switch To {new_mode}")

    #     messagebox.showinfo("THEME", f"Theme switched to {current_mode} Mode")

    def toggle_theme(self):
        # Get the current appearance mode using ctk
        current_mode = ctk.get_appearance_mode()  # Returns "Light" or "Dark" 
        new_mode = "Light" if current_mode == "Dark" else "Dark"  # Determines the new mode
        ctk.set_appearance_mode(new_mode) # Set the new appearance mode
        # The setting menu label for toggling theme is set to "Switch to Light mode" when in dark mode and vice versa
        new_label = "Switch to Dark Mode" if new_mode == "Light" else "Switch to Light Mode"
        
        # Update the settings menu entry; index 6 is the theme toggle command (0-indexed)
        # (0: Copy, 1: Cut, 2: Paste, 3: separator, 4: Clear History, 5: separator, 6: Theme Toggle)
        self.settings_menu.entryconfigure(6, label=new_label)
        messagebox.showinfo("Theme", f"Theme switched to {new_mode} Mode")



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


    def format_expression(self, expression):
        """
        Returns the expression string with numbers formatted with commas.
        Example: "1234+56789" becomes "1,234+56,789"
        """
        # Remove any existing commas returning the expr clean and ready for spliting and formatting
        expression = expression.replace(",", "") 

        # helps to format each number match
        def format_match(match):
            num_str = match.group(0)
            if '.' in num_str:
                integer_part, decimal_part = num_str.split('.', 1) #splits expr into integer and decimal for easy formatting with commas
                try:
                    formatted_int = f"{int(integer_part):,}" if integer_part else "0"
                    return f"{formatted_int}.{decimal_part}" # and re-attach it back together.
                except ValueError:
                    return num_str #if formatting fails fallback to original expression 
            else:
                try:
                    return f"{int(num_str):,}"
                except ValueError:
                    return num_str #if formatting fails fallback to original expression

        formatted_expression = re.sub(r'-?\d+(?:\.\d+)?', format_match, expression) 
        return formatted_expression
    
    

    def on_key_release(self, event):
        current_expression = self.expression.get()
        formatted_expression = self.format_expression(current_expression)
        # Save current cursor position 
        cursor_position = self.entry.index(tk.INSERT)
        self.update_display(formatted_expression)
        # Restore cursor position (adjust if necessary)
        self.entry.icursor(cursor_position)