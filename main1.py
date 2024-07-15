import customtkinter as ctk
import json


def save_data(data):
    try:
        with open("history.json", "w") as f:
            json.dump(data, f)
    except Exception as e:
        print("Gagal menyimpan histori:", e)


def load_data():
    history = []
    try:
        with open("history.json", "r") as f:
            history = json.load(f)
    except Exception as e:
        print("Gagal memuat histori:", e)
    return history


def update_expression_label():
    global expression
    expression_label.configure(text=expression)


def update_history_frame():
    global history
    # Hapus semua widget di dalam history_frame
    for widget in history_frame.winfo_children():
        widget.destroy()

    # Muat ulang data histori dari file
    history = load_data()

    row_history = 0
    for i, data in enumerate(history):
        history_expression_label = ctk.CTkLabel(
            history_frame,
            text=data["expression"],
            font=("Helvetica", 12, "bold"),
            text_color="#a1a1aa",
        )
        history_expression_label.grid(
            row=row_history, column=0, padx=6, pady=0, sticky="e"
        )

        history_result_label = ctk.CTkLabel(
            history_frame,
            text=data["result"],
            font=("Helvetica", 14, "bold"),
            text_color="#71717a",
        )
        history_result_label.grid(
            row=row_history + 1, column=0, padx=6, pady=(0), sticky="e"
        )
        row_history += 2


def calculate():
    global expression
    try:
        history = load_data()
    except Exception as e:
        history = []
        print("Gagal memuat data : ", e)

    try:
        result = str(eval(expression.replace("x", "*")))
        history.append({"expression": expression, "result": result})
        save_data(history)
        expression = result
        update_expression_label()
        update_history_frame()  # Perbarui frame histori setelah perhitungan
    except Exception as e:
        print("Error : ", e)


def action(x):
    global expression
    if x == "AC":
        if expression == "":
            save_data([])
        expression = ""
        update_expression_label()
        update_history_frame()  # Perbarui frame histori setelah aksi AC
    elif x == "<":
        expression = expression[:-1]
        update_expression_label()
    elif x == "=":
        calculate()
    else:
        expression = expression + x
        update_expression_label()


app = ctk.CTk()
app.title("M. Arif A.")
app.geometry("300x350")

ctk.set_appearance_mode("light")

main_frame = ctk.CTkFrame(app, bg_color="#d4d4d8")
main_frame.pack(expand=True, fill="both")

# Buat history frame dengan tinggi yang diinginkan
history_frame = ctk.CTkScrollableFrame(
    main_frame, width=50, height=50, bg_color="#d4d4d8", fg_color="#d4d4d8"
)
history_frame.pack(expand=True, fill="both")
history_frame.grid_columnconfigure(0, weight=1)

expression_frame = ctk.CTkFrame(main_frame, bg_color="#d4d4d8", fg_color="#d4d4d8")
expression_frame.pack(fill="x")

action_frame = ctk.CTkFrame(main_frame, bg_color="#d4d4d8", fg_color="#d4d4d8")
action_frame.pack(fill="x", padx=3, pady=(0, 3))
action_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

# Load data histori saat aplikasi dimulai
history = load_data()
update_history_frame()  # Perbarui frame histori saat aplikasi dimulai

expression = ""
expression_label = ctk.CTkLabel(
    expression_frame, text=expression, font=("Helvetica", 16, "bold")
)
expression_label.pack(side="right", padx=6, pady=6)

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

row, col = 0, 0
for i, button in enumerate(buttons):
    if button == "0":
        btn = ctk.CTkButton(
            action_frame, text=button, command=lambda x=button: action(x)
        )
        btn.grid(
            row=row, column=col, columnspan=2, padx=3, pady=3, ipady=5, sticky="we"
        )
        col += 1
    else:
        btn = ctk.CTkButton(
            action_frame, text=button, command=lambda x=button: action(x)
        )
        btn.grid(row=row, column=col, padx=3, pady=3, ipady=5, sticky="we")

    col += 1
    if col == 4:
        col = 0
        row += 1

app.mainloop()
