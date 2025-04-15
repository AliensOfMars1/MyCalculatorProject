import math
import os
import json
import requests
from tkinter import messagebox
from const import CONSTS  # Assumes CONSTS is defined in const.py

class CalculatorModel:
    def __init__(self):
        self.memory = ""  # initialize the memory storage
        self.history_file = "history.json"  # File for history
        self.history = self.load_history()  # Load history at startup
        self.memory_file = "memory.json"  # File for memory storage

    def fetch_live_usd_to_ghs_rate(self):
        try:
            response = requests.get(CONSTS.CURRENCY_API_URL)
            data = response.json()
            live_rate = data["rates"].get("GHS")
            if live_rate:
                return live_rate
            else:
                raise ValueError("GHS rate not found in API response.")
        except Exception as e:
            messagebox.showerror("No internet connection.", "Failed to get live rate. \nPLEASE CHECK YOUR INTERNET CONNECTION!")

    def evaluate(self, expression):
        try:
            # Remove commas and currency symbols to prevent eval() from misinterpreting the formatted result
            expression = expression.replace(",", "").replace("₵", "").replace("$", "").replace("x", "*")
            if not expression.strip():  # If the expression is empty or only spaces
                return 0  # Return 0 instead of evaluating
            result = eval(expression, {"__builtins__": None}, {
                "sin": math.sin, "cos": math.cos, "tan": math.tan, "log": math.log,
                "sqrt": math.sqrt, "pow": math.pow, "pi": math.pi, "e": math.e,
                "cosh": math.cosh, "tanh": math.tanh, "sinh": math.sinh, "exp": math.exp,
                "log2": math.log2, "log10": math.log10, "degrees": math.degrees, "radians": math.radians,
                "expm1": math.expm1, "pow": math.pow, "factorial": math.factorial
            })
            self.memory = str(result)
            self.save_to_history(expression, result)
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
        except OverflowError:
            messagebox.showinfo("ERROR", "Math Error: The result is too large to compute.")    
        except Exception as e:
            return f"Error: {str(e)}"


    def save_to_history(self, expression, result):
        entry = f"{expression} = {result}"
        # Append the new entry to the history list
        self.history.append(entry)
        # Save the updated history list to the JSON file
        try:
            with open(self.history_file, "w", encoding="utf-8") as file:
                json.dump(self.history, file, indent=4)
        except Exception as e:
            messagebox.showerror("History Save Error", f"Failed to save history:\n{e}")

    def load_history(self):
         # Check if the file exists before attempting to open it
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    # Ensure the data is a list before returning
                    if isinstance(data, list):
                        return data
                    return []
            except json.JSONDecodeError:
                return []  # Handle the case where the file exist but is not valid JSON
        return []  # while this Handle the case where the file does not exist at all 

    def get_history(self):
        # Returns the most recent 100 entries with the latest at the top (or all entries if fewer than 100)
        if self.history:
            # Retrieve the most recent 100 entries, reversing to show the latest first
            recent_history = self.history[-100:][::-1]
            # Join entries with two newline characters to add a blank line between them
            return "\n\n".join(recent_history)
        return "No history available."
    
    def clear_history(self):
        # Reset the in-memory history list and write an empty list to file.
        self.history = []
        with open(self.history_file, "w") as file:
            json.dump(self.history, file, indent=4)


    def load_stack(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []
        return []

    def save_stack(self, stack):
        with open(self.memory_file, "w") as file:
            json.dump(stack, file, indent=4)

    def memory_plus(self, value):
        stack = self.load_stack()
        stack.append(value)
        self.save_stack(stack)

    def memory_minus(self):
        stack = self.load_stack()
        if not stack:
            messagebox.showinfo("EMPTY", "Oops, No memory stored!")
            return ""
        latest_value = stack.pop()
        self.save_stack(stack)
        return latest_value

    def delete_last(self, expression):
        return expression[:-1]

    def recall_memory(self):
        return self.memory

    def clear_memory(self):
        self.memory = ""
