import customtkinter as ctk
import json


def update_main_frame(result, expression):
    expression_label.configure(text=result)
    history_expression_label.configure(text=expression)


def calculate():
    global expression
    try:
        result = str(eval(expression.replace("x", "*")))
    except Exception as e:
        print("Error : ", e)
        update_main_frame(result, expression)


expression = ""


def action(x):
    global expression
    if x == "AC":
        expression = ""
    elif x == "<":
        expression = expression[:-1]
    elif x == "=":
        calculate()
    else:
        expression = expression + x


app = ctk.CTk()
app.title("M. Arif A.")
app.geometry("250x280")
app.resizable(False, False)

ctk.set_appearance_mode("light")

# frame
main_frame = ctk.CTkFrame(app)
main_frame.pack(expand=True, fill="both")

history_expression_frame = ctk.CTkFrame(main_frame)
history_expression_frame.pack(expand=True, fill="both")

expression_frame = ctk.CTkFrame(main_frame)
expression_frame.pack(fill="x")

action_frame = ctk.CTkFrame(main_frame)
action_frame.pack(fill="x", padx=2, pady=2)
action_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

# content
history_expression_label = ctk.CTkLabel(
    history_expression_frame,
    text="2+2",
    text_color="#a1a1aa",
    font=("Helvetica", 14, "bold"),
)
history_expression_label.pack(side="right", fill="both", padx=10, pady=0)

expression_label = ctk.CTkLabel(
    expression_frame,
    text="120",
    text_color="#1f2937",
    font=("Helvetica", 16, "bold"),
)
expression_label.pack(side="right", fill="x", padx=10, pady=0)

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
row_btn = 0
col_btn = 0
for i, button in enumerate(buttons):
    if button == "0":
        btn = ctk.CTkButton(
            action_frame,
            text=button,
            font=("Helvetica", 20, "bold"),
        )
        btn.grid(
            row=row_btn,
            column=col_btn,
            columnspan=2,
            padx=1,
            pady=1,
            ipady=5,
            sticky="we",
        )
        col_btn += 1
    else:
        btn = ctk.CTkButton(
            action_frame,
            text=button,
            font=("Helvetica", 20, "bold"),
        )
        btn.grid(row=row_btn, column=col_btn, padx=1, pady=1, ipady=5, sticky="we")
    col_btn += 1
    if col_btn == 4:
        row_btn += 1
        col_btn = 0

if __name__ == "__main__":
    app.mainloop()
