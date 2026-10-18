"""A four-function desktop calculator. Run with: python3 calculator.py"""

from decimal import Decimal, InvalidOperation, localcontext
import tkinter as tk
from tkinter import ttk


def calculate(left, operator, right):
    """Calculate using decimal arithmetic without evaluating Python code."""
    left, right = Decimal(left), Decimal(right)
    with localcontext() as context:
        context.prec = 28
        if operator == "+":
            return left + right
        if operator == "-":
            return left - right
        if operator == "*":
            return left * right
        if operator == "/":
            if right == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            return left / right
    raise ValueError("Unknown operator")


class Calculator:
    def __init__(self, root):
        self.root = root
        root.title("Calculator")
        root.minsize(300, 380)
        self.display = tk.StringVar(value="0")
        self.history = tk.StringVar()
        self.left = None
        self.operator = None
        self.new_entry = True

        frame = ttk.Frame(root, padding=16)
        frame.grid(sticky="nsew")
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        ttk.Label(frame, textvariable=self.history, anchor="e").grid(
            row=0, column=0, columnspan=4, sticky="ew"
        )
        ttk.Entry(
            frame, textvariable=self.display, justify="right",
            font=("Helvetica", 24), state="readonly", width=16
        ).grid(row=1, column=0, columnspan=4, sticky="ew", pady=(8, 16))

        rows = [
            ["C", "⌫", "±", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["0", ".", "=", ""],
        ]
        for row_index, row in enumerate(rows, start=2):
            frame.rowconfigure(row_index, weight=1)
            for column, label in enumerate(row):
                if label:
                    ttk.Button(
                        frame, text=label,
                        command=lambda key=label: self.press(key)
                    ).grid(row=row_index, column=column,
                           columnspan=2 if label == "=" else 1,
                           sticky="nsew", padx=3, pady=3, ipady=10)
        for column in range(4):
            frame.columnconfigure(column, weight=1, uniform="buttons")
        root.bind("<Key>", self.on_key)

    def clear(self):
        self.display.set("0")
        self.history.set("")
        self.left = self.operator = None
        self.new_entry = True

    def press(self, key):
        operators = {"+": "+", "−": "-", "×": "*", "÷": "/"}
        if key == "C":
            self.clear()
            return
        if self.display.get().startswith("Error"):
            self.clear()
        if key in "0123456789.":
            value = "0" if self.new_entry else self.display.get()
            if key == ".":
                if "." not in value:
                    value += "."
            else:
                value = key if value == "0" else value + key
            self.display.set(value)
            self.new_entry = False
        elif key == "±":
            value = self.display.get()
            if Decimal(value) != 0:
                self.display.set(value[1:] if value.startswith("-") else "-" + value)
        elif key == "⌫":
            if not self.new_entry:
                value = self.display.get()[:-1]
                self.display.set(value if value not in ("", "-") else "0")
        elif key in operators or key == "=":
            try:
                if self.operator and not self.new_entry:
                    result = calculate(self.left, self.operator, self.display.get())
                    self.display.set(format(result, "f"))
                if key in operators:
                    self.left = self.display.get()
                    self.operator = operators[key]
                    self.history.set(f"{self.left} {key}")
                else:
                    self.left = self.operator = None
                    self.history.set("")
                self.new_entry = True
            except (ZeroDivisionError, InvalidOperation, OverflowError) as error:
                self.clear()
                self.display.set("Error: divide by zero" if isinstance(error, ZeroDivisionError)
                                 else "Error: invalid calculation")

    def on_key(self, event):
        special = {"Return": "=", "KP_Enter": "=", "Escape": "C",
                   "BackSpace": "⌫", "Delete": "C"}
        key = special.get(event.keysym, event.char)
        key = {"*": "×", "/": "÷", "-": "−", "c": "C", "C": "C"}.get(key, key)
        if key and key in "0123456789.+−×÷=C⌫":
            self.press(key)
            return "break"


if __name__ == "__main__":
    window = tk.Tk()
    Calculator(window)
    window.mainloop()
