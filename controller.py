import threading
from tkinter import messagebox
from model import CalculatorModel
from view import CalculatorView

class CalculatorController:
    def __init__(self):
        self.model = CalculatorModel()
        self.view = CalculatorView(self)

    # Handles all the button click events.
    def on_button_click(self, button_text):
        current_text = self.view.expression.get()
        if button_text == "CE":
            self.view.update_display("") # Clears the display
        elif button_text == "DEL":
            self.view.update_display(self.model.delete_last(current_text)) # Deletes the last character
        elif button_text == "ANS":
            self.view.update_display(self.model.recall_memory()) # Recalls last result value
        elif button_text == "=":
            try:
                result = self.model.evaluate(current_text) # Evaluates the expression 
                self.view.update_display(f"{result:,}") # and displays results.
            except TypeError:
                self.view.update_display("") #returns an empty screen whiles the model handles the Error returning a user-friendly message
        elif button_text == "M+":   
            value = self.view.expression.get() 
            self.model.memory_plus(value) 
            self.view.update_display("") #  clear display after adding value
        elif button_text == "M-":
            retrieved = self.model.memory_minus()
            self.view.update_display(retrieved)
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
        elif button_text in {"sin", "cos", "tan", "exp", "sinh", "cosh", "tanh", "expm1",
                             "log", "log2", "log10", "factorial", "radians", "degrees", "sqrt", "pow"}:
            self.view.update_display(current_text + button_text + "(")
        else:
            self.view.update_display(current_text + button_text)

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

    #Clears the history notifies the user when the "clear History button is clicked"
    def clear_history(self):
        # Ask the user to confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to clear the history?")
        if confirm:
            self.model.clear_history()
            messagebox.showinfo("History", "Calculation history cleared successfully!")

    def run(self):
        self.view.mainloop()
