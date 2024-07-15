import tkinter as tk
from tkinter import ttk
import json


def save_data(data):
    with open("history.json", "w") as f:
        json.dump(data, f)


def load_data():
    try:
        with open("history.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def update_result_label():
    result_label.config(text=num)


def update_history_label():
    history_text.config(state=tk.NORMAL)
    history_text.delete("1.0", tk.END)
    for item in history[::-1]:
        history_text.insert(tk.END, f"{item['expression']} = {item['result']}\n")
    history_text.config(state=tk.DISABLED)


def clear():
    global num
    num = ""
    update_result_label()


def backspace():
    global num
    num = num[:-1]
    update_result_label()


def calculate():
    global num
    try:
        result = str(eval(num.replace("x", "*")))
        history.append({"expression": num, "result": result})
        save_data(history)
        num = result
    except Exception as e:
        print(f"Calculation error: {e}")
        num = "Error"

    update_result_label()
    update_history_label()


app = tk.Tk()
app.title("Calculator")
app.geometry("350x400")

result_frame = ttk.Frame(app)
result_frame.pack(expand=True, fill="both")

history_frame = ttk.Frame(app)
history_frame.pack(expand=True, fill="both")

action_frame = ttk.Frame(app)
action_frame.pack(fill="x", padx=1, pady=1)
action_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

buttons = [
    "AC",
    "<",
    "%",
    "/",
    "7",
    "8",
    "9",
    "x",
    "4",
    "5",
    "6",
    "-",
    "1",
    "2",
    "3",
    "+",
    "0",
    ".",
    "=",
]

num = ""


def action(x):
    global num
    if x == "AC":
        clear()
    elif x == "<":
        backspace()
    elif x == "=":
        calculate()
    else:
        num = num + x
        update_result_label()


row = 0
col = 0

result_label = ttk.Label(result_frame, text=num, font=("Helvetica", 24))
result_label.pack(side="right", padx=10, pady=10)

history_label = ttk.Label(history_frame, text="History:")
history_label.pack(side="top", padx=10, pady=10)

history_text = tk.Text(history_frame, height=10, width=40, wrap=tk.WORD)
history_text.pack(side="bottom", padx=10, pady=10)
history_text.config(state=tk.DISABLED)

history = load_data()
update_history_label()

for i, btn in enumerate(buttons):
    if btn == "0":
        button = ttk.Button(action_frame, text=btn, command=lambda x=btn: action(x))
        button.grid(
            row=row, column=col, columnspan=2, ipady=10, padx=1, pady=1, sticky="we"
        )
        col += 1
    else:
        button = ttk.Button(action_frame, text=btn, command=lambda x=btn: action(x))
        button.grid(row=row, column=col, ipady=10, padx=1, pady=1, sticky="we")

    col += 1
    if col > 3:
        col = 0
        row += 1

app.mainloop()
