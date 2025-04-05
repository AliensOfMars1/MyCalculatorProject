import re
import tkinter as tk
from tkinter import messagebox, font
from PIL import Image, ImageTk
import customtkinter as ctk
from const import CONSTS  # Assumes CONSTS is defined in const.py

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

        # Key bindings
        self.bind("<Escape>", lambda event: self.controller.on_button_click("CE"))
        self.bind("<Control-H>", lambda event: self.show_scrollable_history_window())
        self.bind("<Control-h>", lambda event: self.show_scrollable_history_window())
        self.bind("<Control-T>", lambda event: self.toggle_theme())
        self.bind("<Control-t>", lambda event: self.toggle_theme())
        self.bind("<BackSpace>", lambda event: self.controller.on_button_click("DEL"))
        self.bind("<Return>", lambda event: self.controller.on_button_click("="))
        self.bind("=", lambda event: self.controller.on_button_click("="))
        self.bind("<Control-A>", lambda event: self.controller.on_button_click("ANS"))
        self.bind("<Control-a>", lambda event: self.controller.on_button_click("ANS"))

        # Entry widget for expression / results
        self.expression = ctk.StringVar()
        validating_entry_input = (self.register(self.validate_input), "%P")
        self.entry = ctk.CTkEntry(
            self, textvariable=self.expression, font=("Lucida Console", 24),
            height=60, corner_radius=10, justify="right",
            validate="key", validatecommand=validating_entry_input
        )
        self.entry.pack(fill="both", padx=10, pady=10)

        # Context menu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Cut", command=self.cut_text)
        self.context_menu.add_command(label="Copy", command=self.copy_text)
        self.context_menu.add_command(label="Paste", command=self.paste_text)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Clear History", command=self.controller.clear_history)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Click To Change Theme", command=self.toggle_theme)
        self.entry.bind("<Button-3>", self.show_context_menu)
        self.entry.bind("<Control-Button-1>", self.show_context_menu)

        # Settings menu
        self.settings_menu = tk.Menu(self, tearoff=0)
        self.settings_menu.add_command(label="Copy", command=self.copy_text)
        self.settings_menu.add_command(label="Cut", command=self.cut_text)
        self.settings_menu.add_command(label="Paste", command=self.paste_text)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(label="Clear History", command=self.controller.clear_history)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(label="Click To Change Theme", command=self.toggle_theme)

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

        # Frame for buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(expand=True, fill="both")
        self.create_standard_buttons()

        # Loading Animation Variables
        self.loading = False
        self.loading_dots = ["", ".", "..", "..."]
        self.loading_index = 0

    def show_scrollable_history_window(self):
        if hasattr(self, "history_window") and self.history_window.winfo_exists():
            self.history_window.lift()
            return

        self.history_window = ctk.CTkToplevel()
        self.history_window.title("History")
        self.history_window.geometry("200x300")
        self.history_window.transient(self)
        self.history_window.grab_set()
        self.history_window.attributes("-topmost", True)
        self.history_window.lift()
        self.history_window.focus_force()

        text_widget = ctk.CTkTextbox(self.history_window, width=480, height=350, wrap="word", font=("Arial", 14))
        text_widget.pack(pady=10, padx=10, fill="both", expand=True)
        try:
            with open("history.txt", "r", encoding="utf-8") as file:
                text_content = file.read()
                text_widget.insert("1.0", text_content)
        except FileNotFoundError:
            text_widget.insert("1.0", "File not found!")
        text_widget.configure(state="disabled")

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

    def clear_buttons(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

    def update_geometry(self):
        if self.mode == "Scientific":
            self.geometry("1000x600+200+40")
            self.history_button.place(x=950, y=84)
        else:
            self.geometry("480x600+600+40")
            self.history_button.place(x=430, y=84)

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

    def update_display(self, text):
        self.expression.set(text)
        current_text = self.expression.get()
        if current_text == "None":
            self.update_display("")

    def show_menu(self):
        self.settings_menu.post(
            self.settings_button.winfo_rootx(),
            self.settings_button.winfo_rooty() + self.settings_button.winfo_height()
        )

    def show_context_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Cut", command=self.cut_text)
        menu.add_command(label="Copy", command=self.copy_text)
        menu.add_command(label="Paste", command=self.paste_text)
        menu.add_separator()
        menu.add_command(label="Clear History", command=self.controller.clear_history)
        menu.tk_popup(event.x_root, event.y_root)

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

    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        new_mode = "Light" if current_mode == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        messagebox.showinfo("THEME", f"Theme switched to {new_mode} Mode")

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
