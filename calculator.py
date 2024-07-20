import customtkinter as ctk


def update_expression(new_expression):
    global expression
    expression_label.configure(text=new_expression)
    expression = new_expression


def update_history_expression(new_history_expression):
    history_expression_label.configure(text=new_history_expression)


def calculate_expression(expression):
    global histories
    try:
        result = str(eval(expression.replace('x', '*')))
        if result.endswith('.0'):
            result = result[:-2]
        update_expression(result)
        update_history_expression(expression)
        histories.insert(0, (expression, result))
    except Exception as e:
        print(e)


def button_action(button_value):
    global expression
    if button_value == 'AC':
        if expression == '':
            update_history_expression('')
        expression = ''
        update_expression(expression)
    elif button_value == '<':
        expression = expression[:-1]
        update_expression(expression)
    elif button_value == '=':
        calculate_expression(expression)
    else:
        expression += button_value
        update_expression(expression)


def history():
    global histories
    history_window = ctk.CTkToplevel(app)
    history_window.title('History')
    history_window.geometry('250x300')
    history_window.resizable(False, False)

    main_frame = ctk.CTkScrollableFrame(history_window, bg_color='#d1d5db', fg_color='#d1d5db')
    main_frame.pack(expand=True, fill='both')
    main_frame.grid_columnconfigure(0, weight=1)
    
    def button_action(x):
        update_expression(x)
        history_window.destroy()

    for i, (expr, result) in enumerate(histories):
        expr_label = ctk.CTkButton(main_frame, text=f'{expr} = ', width=0, font=('Helvetica', 12, 'bold'), command=lambda x=expr: button_action(x), fg_color='#d4d4d8', text_color='#52525b')
        expr_label.grid(row=i, column=0, pady=2, sticky='e')
        result_button = ctk.CTkButton(main_frame, text=result, width=0, font=('Helvetica', 12, 'bold'), command=lambda x=result: button_action(x), fg_color='#d4d4d8', text_color='#52525b')
        result_button.grid(row=i, column=1, padx=(0, 5), pady=2, sticky='w')
    
    history_window.transient(app)
    history_window.grab_set()
    history_window.focus()
    app.wait_window(history_window)


histories = []
expression = ''

app = ctk.CTk()
app.title('M Arif A')
app.geometry('250x300')
app.resizable(False, False)

ctk.set_appearance_mode('light')

# Frame
container_frame = ctk.CTkFrame(app, bg_color='#d4d4d8', fg_color='#d4d4d8')
container_frame.pack(expand=True, fill='both')

history_expression_frame = ctk.CTkFrame(container_frame, bg_color='#d4d4d8', fg_color='#d4d4d8')
history_expression_frame.pack(fill='x')

expression_frame = ctk.CTkFrame(container_frame, bg_color='#d4d4d8', fg_color='#d4d4d8')
expression_frame.pack(expand=True, fill='both')

button_frame = ctk.CTkFrame(container_frame, bg_color='#d4d4d8', fg_color='#d4d4d8')
button_frame.pack(fill='x', padx=2, pady=2)
button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

# Label
button_history = ctk.CTkButton(
    history_expression_frame, text='History', anchor='w', width=0,
    font=('Helvetica', 12, 'bold'), command=lambda: history()
)
button_history.pack(side='left', padx=5, pady=(5, 0))

history_expression_label = ctk.CTkLabel(
    history_expression_frame, text='', font=('Helvetica', 14, 'bold'),
    anchor='e', text_color='#a1a1aa'
)
history_expression_label.pack(side='right', padx=5, pady=(5, 0))

expression_label = ctk.CTkLabel(
    expression_frame, text='', font=('Helvetica', 16, 'bold'),
    anchor='e', text_color='#52525b'
)
expression_label.pack(expand=True, fill='both', padx=5)

# Buttons
buttons = [
    'AC', '<', '%', '/',
    '7', '8', '9', 'x',
    '4', '5', '6', '-',
    '1', '2', '3', '+',
    '0', '.', '=',
]

row, col = 0, 0
for button in buttons:
    btn = ctk.CTkButton(
        button_frame, text=button, font=('Helvetica', 16, 'bold'),
        fg_color='#e4e4e7', text_color='#52525b',
        command=lambda x=button: button_action(x)
    )
    if button == '0':
        btn.grid(row=row, column=col, columnspan=2, padx=1, pady=1, ipady=5, sticky='we')
        col += 1
    else:
        btn.grid(row=row, column=col, padx=1, pady=1, ipady=5, sticky='we')
    col += 1
    if col == 4:
        col = 0
        row += 1

if __name__ == '__main__':
    app.mainloop()