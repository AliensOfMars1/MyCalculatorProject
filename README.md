This Python Calculator is a modern, user-friendly desktop calculator application built with Python, featuring a clean GUI powered by CustomTkinter. This application offers both a standard and scientific mode, with advanced mathematical functions and live features like live currency converter.

Key Features
MVC Architecture:
The calculator is structured using the Model-View-Controller (MVC) pattern for clear separation between business logic, user interface, and user input handling.

Standard and Scientific Modes:
Switch effortlessly between standard calculations and a rich set of scientific operations including trigonometric functions, logarithms, exponentials, and more.

Dynamic Comma Formatting:
Automatically formats numbers with commas as you type, enhancing readability and accuracy—while intelligently bypassing formatting when necessary (for instance, within function calls).

Memory and History Support:
Save your calculations in a persistent history stored in JSON format, recall previous results, and make adjustments using memory add/subtract functionality.

Live Currency Conversion:
Perform live currency conversions (USD to GHS and vice versa) with real-time rate fetching, complete with a non-blocking loading animation.

Customizable and Modern UI:
Enjoy a sleek, responsive interface with a theme toggle that lets you switch between light and dark modes. Intuitive key bindings (e.g., keyboard shortcuts for clearing, deleting, and recalling previous computations) further enhance usability.

Robust Error Handling:
Built-in error messaging delivers user-friendly notifications for invalid inputs, syntax errors, or operation issues, ensuring a smooth and reliable user experience.

Overview
Developed entirely in Python, this calculator leverages industry-standard libraries and techniques to provide a powerful yet accessible computing tool. The integration with CustomTkinter not only gives the application a modern look and feel but also simplifies the creation of advanced GUI components. Whether you're a student, a professional, or simply someone who appreciates a good calculator, this project combines practical features with a streamlined interface for daily use.



        SHORTS CUT FOR FASTER CALCULATOR USE 
ESCAPE KEY functions as CE button, clears the calculator screen
ctrl+ A or a fuctions same as clicking on ANS button, recalls last result.
ctrl + T or t will switch between dark and light theme 
ctrl + H or h brings up the calculator History
backspace functions as DEL button



To run the project,

1. Clone the project
git clone https://github.com/AliensOfMars1/MyCalculatorProject

2. Create a virtual enviroment and activate it.

```bash
python -m venv cal_venv
.\cal_venv/Scripts/activate
```

3. Install the required packages

```bash
pip install -r requirements.txt
```
4. Run main
```bash
python main.py
```