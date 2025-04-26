import threading
import re
from tkinter import messagebox
from models.model import CalculatorModel
from views.view import CalculatorView

class CalculatorController:
    def __init__(self):
        self.model = CalculatorModel()
        self.view = CalculatorView(self)

    # Handles all the button click events.
    def on_button_click(self, button_text):

        current_text = self.view.expression.get()

        SCIENTIFIC_FUNCS = {
        "sin", "cos", "tan", "exp", "sinh", "cosh", "tanh", "expm1",
        "log", "log2", "log10", "factorial", "radians", "degrees", "sqrt", "abs"}

        if button_text == "CE":
            self.view.update_display("") # Clears the display

        elif button_text == "DEL":
            # Work with a raw (unformatted) version of the expression
            raw_text = current_text.replace(",", "")
            new_text = self.model.delete_last(raw_text)
            formatted_expr = self.view.format_expression(new_text)
            self.view.update_display(formatted_expr) # Deletes the last character
        elif button_text == " +/- "  :     
            self.toggle_last_number_sign()
          
        elif button_text == "ANS":
            ans_text = self.model.recall_memory() # Recalls last result value
            formatted__expression = self.view.format_expression(ans_text)
            self.view.update_display(formatted__expression) 
        elif button_text == "=":
            try:
                # Evaluate after cleaning the expression
                result = self.model.evaluate(current_text.replace(",", ""))
                if isinstance(result, (int, float)): #if result is an interger or Float.
                    display_text = f"{result:,}"# and displays results with formatted commas.
                else:
                    # if result is not numeric, simply use it as is
                    display_text = result
                self.view.update_display(display_text)    
            except TypeError: 
                self.view.update_display("") #returns an empty screen whiles/after the model handles the Error returning a user-friendly message

        elif button_text == "M+":
            value = self.view.expression.get().strip()
            if not value:
                messagebox.showinfo("Memory", "Nothing to add. Please enter a value first.")
                return
            # Optional: you could also validate that value is a number here
            self.model.memory_plus(value)
            self.view.update_display("")  # clear display after adding value for good flow
            messagebox.showinfo("Memory", f'{value} added to memory!')
    
        elif button_text == "M-":
            retrieved = self.model.memory_minus()
            formatted_expression = self.view.format_expression(retrieved)
            self.view.update_display(formatted_expression)
        # --- Live currency conversion with loading animation ---            
        elif button_text == "USD-GHS":
            try:
                usd_value = float(current_text.replace(",", "").replace("$", ""))
            except ValueError:
                messagebox.showerror("Conversion Error", "Please enter a valid numeric value for USD.")
                return
            self.view.start_loading_animation()
            thread = threading.Thread(target=self.convert_usd_to_ghs, args=(usd_value,))
            thread.start()
        elif button_text == "GHS-USD":
            try:
                ghs_value = float(current_text.replace(",", "").replace("₵", ""))
            except ValueError:
                messagebox.showerror("Conversion Error", "Please enter a valid numeric value for GHS.")
                return
            self.view.start_loading_animation()
            thread = threading.Thread(target=self.convert_ghs_to_usd, args=(ghs_value,))
            thread.start()
        #appending  Scientific operations with "(" to the existing text so the user will only have to close them with ')'
        elif button_text in SCIENTIFIC_FUNCS:
            self.append_to_expression(button_text + "(")
        else:
            self.append_to_expression(button_text)

    def append_to_expression(self, text):
        new_text = self.view.expression.get() + text
        formatted = self.view.format_expression(new_text)
        self.view.update_display(formatted)

    #Conversion methods
    def convert_usd_to_ghs(self, usd_value):
        live_rate = self.model.fetch_live_usd_to_ghs_rate()
        if live_rate:
            ghs_value = usd_value * live_rate
            result_text = f"₵{ghs_value:,.2f}"
        else:
            result_text = ""
        self.view.after(0, lambda: self.finish_conversion(result_text))

    def convert_ghs_to_usd(self, ghs_value):
        live_rate = self.model.fetch_live_usd_to_ghs_rate()
        if live_rate:
            usd_value = ghs_value / live_rate
            result_text = f"${usd_value:,.2f}"
        else:
            result_text = ""
        self.view.after(0, lambda: self.finish_conversion(result_text))

    def finish_conversion(self, result_text):
        self.view.stop_loading_animation()
        self.view.update_display(result_text)

    def on_theme_toggle(self): # Toggles the theme for the calculator 
        self.view.toggle_theme()

    def toggle_last_number_sign(self):
        current_expr = self.view.expression.get().replace(",", "")
        if not current_expr:
            return

        # Match patterns ending in a number or expression in parentheses (e.g., sin(40))
        # We find the *last* part of the expression that could be negated.
        # Examples:
        # - 100 -> (-100)
        # - 100 + 2 -> 100 + (-2)
        # - sin(40) -> sin(-40)
        # - sqrt(16) -> sqrt(-16)

        # This regex captures the last number or inner expression that should be negated.
        pattern = r'(.*?)(\b(?:sin|cos|tan|log|sqrt|exp|abs|factorial|sinh|cosh|tanh|expm1|log2|log10|radians|degrees)\s*\(\s*)(-?\s*[^()]+)(\))$'
        match = re.match(pattern, current_expr)

        if match:
            # Negate the value inside the function call
            before_func, func_call, value, closing = match.groups()
            if value.strip().startswith('-'):
                value = value.strip()[1:]  # Remove the negative sign
            else:
                value = '-' + value.strip()
            new_expr = before_func + func_call + value + closing
        else:
            # Try to match the last numeric expression
            pattern2 = r'(.*?)(\(?-?\d*\.?\d+\)?)(\s*)$'
            match2 = re.match(pattern2, current_expr)
            if match2:
                before, number, space = match2.groups()
                number = number.strip()
                if number.startswith('(-'):
                    number = number[2:-1]  # Remove wrapping (-x)
                elif number.startswith('-'):
                    number = number[1:]  # Remove just the -
                else:
                    number = f"(-{number})"
                new_expr = before + number + space
            else:
                # Nothing to toggle
                return

        # Update the display
        formatted = self.view.format_expression(new_expr)
        self.view.update_display(formatted)
        

    #Clears the history notifies the user when the "clear History button is clicked"
    def clear_history(self):
        # Ask the user to confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to clear the history?")
        if confirm:
            self.model.clear_history()
            # Close the history window if it's open
            if hasattr(self.view, "history_window") and self.view.history_window.winfo_exists():
                self.view.history_window.destroy()
                del self.view.history_window  # Optionally remove the attribute
            messagebox.showinfo("History", "Calculation history cleared successfully!")



    def run(self):
        self.view.mainloop()
