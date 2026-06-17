import tkinter as tk
from tkinter import colorchooser

def choose_color():
    # Открываем диалоговое окно выбора цвета
    # Метод возвращает кортеж: ((R, G, B), '#HEX_код')
    color_info = colorchooser.askcolor(title="Выберите цвет")
    
    # Проверяем, выбрал ли пользователь цвет (не нажал "Отмена")
    if color_info[1]:
        selected_hex = color_info[1]
        print(f"Выбранный цвет: {selected_hex}")
        # Меняем цвет фона кнопки на выбранный цвет
        button.config(bg=selected_hex, activebackground=selected_hex)

root = tk.Tk()
root.title("Выбор цвета")
root.geometry("300x200")

# Кнопка для запуска диалога
button = tk.Button(root, text="Открыть палитру", command=choose_color, width=20, font=("Arial", 12))
button.pack(pady=50)

root.mainloop()
