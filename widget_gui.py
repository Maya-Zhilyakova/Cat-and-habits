"""
Модуль графического интерфейса приложения "Кот и привычки".

Содержит класс Gui, который управляет:
- Главным окном (без рамки, с возможностью перемещения)
- Левым меню навигации
- Отображением кота с мотивирующими фразами
- Добавлением новых привычек
- Отметкой выполнения привычек
- Статистикой прогресса
- Сбросом данных
"""

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, askyesno, showwarning
from PIL import Image, ImageTk

from utils import *
from base_data import DataBase
import random

class Gui:
    """
    Главный класс приложения.
    
    Атрибуты:
        root (Tk): Корневое окно Tkinter
        left_container (Frame): Левая панель с кнопками меню
        right_container (Frame): Правая панель с контентом
        up_right_container (Frame): Верхняя панель с текстом кота
        canvas (Canvas): Для будущего скролла (не используется)
        db (DataBase): Экземпляр для работы с БД
        text_cat (Label): Метка с текстом кота-мотиватора
    """
    def __init__(self):
        """Инициализация: создание окна и подключение к БД."""
        self.root = Tk()
        self.left_conteiner = None
        self.right_container = None
        self.up_right_container = None
        self.canvas = None
        self.db = DataBase()
        self.db.create_table()
        self.text_cat = None

    def all_part(self):
        """
        Основной метод сборки интерфейса.
        
        Создаёт:
        - Кастомную строку заголовка (без системной рамки)
        - Кнопку закрытия
        - Возможность перетаскивать окно за заголовок
        - Левое меню
        - Верхнюю панель с текстом
        - Кота в правой части
        """
        self.root.iconbitmap(resource_path("Images/cat_ico.ico"))
        self.root.overrideredirect(True)
        self.root.geometry("550x300+500+300")

        title_bar = Frame(self.root, bg=bg_title, height=25)
        title_bar.pack(fill=X)
        title_bar.pack_propagate(False)

        title_label = Label(title_bar, text='💫 Кот и ты ', bg=bg_title, cursor='fleur', font=('Times New Roman', 10), fg=fg_white)
        title_label.pack(side=LEFT, padx=5)

        close_btn = Button(title_bar, text='✕', command=self.root.destroy, bg='lightcoral', bd=0, padx=5)
        close_btn.pack(side=RIGHT)

        title_bar.bind('<Button-1>', self.start_move)
        title_bar.bind('<B1-Motion>', self.on_move)

        self.left_panel()
        self.up_right_panel()

        self.cat()

        self.root.mainloop()

    def cat(self):
        """
        Отображение кота и панели навигации.
        
        Создаёт:
        - Изображение кота (случайное из трёх)
        - Текст рядом с котом (из категории "cat_main")
        - Кнопки левого меню: Кот, Трекер привычек, Статистика, Сброс данных
        - Разделительные линии
        """
        self.right_container = Frame(self.root, bg=bg_light, width=420, height=240)
        self.right_container.place(relx=0.3, rely=0.24)
        self.right_container.pack_propagate(False)

        img = Image.open(random.choice([resource_path('Images/cat_one.jpg'), resource_path('Images/cat_two.jpg'), resource_path('Images/cat_three.jpg')])).resize((190, 190), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        cat = Label(self.right_container, width=190, height=190, image=photo, borderwidth=0)
        cat.image = photo
        cat.place(relx=0.05, rely=0.1)

        txt_cat = Label(self.right_container, justify='left',  text=get_random_phrase("cat_main"),font=("Comic Sans MS", 10, "bold"), bg=bg_light, fg=fg_white, borderwidth=0)
        txt_cat.place(relx=0.53,rely=0.05)

        btn_menu = btn_left(self.left_container, '😺 Кот', self.cat)
        btn_menu.place(relx=0.05, rely=0.02)

        btn_3_back = btn_left(self.left_container, '⚙️ Трекер\nпривычек', self.add_habit)
        btn_3_back.place(relx=0.05, rely=0.2)

        btn_3_forward = btn_left(self.left_container, '📊 Статистика\n выполнения', self.statystic_habits)
        btn_3_forward.place(relx=0.05, rely=0.465)

        btn_statistic_mb = btn_left(self.left_container, '♻️ Сбросить\n данные', self.delete_datas)
        btn_statistic_mb.place(relx=0.05, rely=0.73)

        line = Frame(self.root, height=2, width=600, bg=bg_title)
        line.place(relx=0.3, rely=0.24)

        line2 = Frame(self.root, height=600, width=2, bg=bg_title)
        line2.place(relx=0.3, rely=0.08)
        self.text_cat.config(text=get_random_phrase("main_menu"))

    def left_panel(self):
        """Создаёт левую панель для размещения кнопок навигации."""
        self.left_container = Frame(self.root, bg=bg_dark, width=210)
        self.left_container.pack(fill=Y, expand=True, side=LEFT, anchor='w')
        self.left_container.pack_propagate(False)

    def up_right_panel(self):
        """
        Создаёт верхнюю правую панель.
        
        Здесь отображается текущая мотивирующая фраза кота,
        которая меняется в зависимости от раздела приложения.
        """
        self.up_right_container = Frame(self.root, bg=bg_dark, width=420, height=60)
        self.up_right_container.place(relx=0.3, rely=0.08)
        self.up_right_container.pack_propagate(False)

        self.text_cat = Label(self.up_right_container, text=f"😺 — Посмотри статистику сейчас.\nПосле добавления новых данные удалятся.", bg=bg_dark, fg=fg_white, font=("Comic Sans MS", 10), justify='left')
        self.text_cat.place(x=8, y=-3)
        self.text_cat.config(text=get_random_phrase("main_menu"))

    def add_habit(self):
        """
        Переход в режим добавления/отслеживания привычек.
        
        Если привычек нет (count_habits() == 0):
            - Показывает 3 поля ввода для новых привычек
            - Кнопка "Начать серию"
        Если привычки есть:
            - Вызывает make_habits() для отображения списка
        """
        for widget in self.right_container.winfo_children():
            widget.destroy()

        self.text_cat.config(text=get_random_phrase("add_habit"))

        if self.db.count_habits() > 0:
            
            self.make_habits()
        else:
            Label(self.right_container, text='Введите 3 привычки на 21 день:', font=("Comic Sans MS", 12, "bold", "underline"), bg=bg_light, fg=fg_black).place(relx=0.02, rely=0.02)
            for i in range(1, 4):
                if i == 1:
                    x = 45
                else:
                    x= 6
                Label(self.right_container, text=f'{i})', font=("Comic Sans MS", 12, "bold"), bg=bg_light, fg=fg_black).pack(padx=5, pady=(x, 6), anchor='w')

            first = Entry(self.right_container, bg=entry, fg=fg_black, width=37, font=("Times New Roman", 11))
            first.place(relx=0.08, rely=0.215)
            second = Entry(self.right_container, bg=entry, fg=fg_black, width=37, font=("Times New Roman", 11))
            second.place(relx=0.08, rely=0.415)
            third = Entry(self.right_container, bg=entry, fg=fg_black, width=37, font=("Times New Roman", 11))
            third.place(relx=0.08, rely=0.615)
            ok_habit = Button(self.right_container, bg=bg_dark, fg=fg_white, text='Начать серию', font=("Times New Roman", 12), command=lambda: self.save_habits(first, second, third)).place(relx=0.3,rely=0.752)

    def save_habits(self, place_1, place_2, place_3):
        """
        Сохраняет три введённые привычки в базу данных.
        
        Проверяет, чтобы все три названия были разными.
        
        Аргументы:
            place_1, place_2, place_3: виджеты Entry с текстом привычек
        """
        habit_1 = place_1.get()
        habit_2 = place_2.get()
        habit_3 = place_3.get()

        if (habit_1 != habit_2) and (habit_2 != habit_3) and (habit_1 != habit_3):
            self.db.create_table()
            self.db.insert_habit(habit_1)
            self.db.insert_habit(habit_2)
            self.db.insert_habit(habit_3)

            self.make_habits()
        else:
            showwarning(title='Предупреждение', message='Тексты привычек не может быть идентичными')

    def delete_btn(self):
        """Полностью удаляет все привычки и логи, перезапуская режим добавления."""
        self.db.delete_21()
        self.add_habit()

    def delete_datas(self):
        """
        Запрашивает подтверждение и сбрасывает все данные.
        
        При подтверждении:
            - Удаляет все привычки и историю
            - Переходит в режим добавления новых привычек
        """
        result = askyesno(title="Подтвержение удаления данных", message="Ты точно уверен(а), что хочешь стереть весь прогресс?😿")
        if result:
            showinfo("Удаление", "Данные все стерты")
            self.delete_btn()
        else:
            showinfo("Сохранение", "Данные остались нетронутыми")

    def make_habits(self):
        """
        Отображает список привычек с кнопками "Да"/"Нет".
        
        Если все 3 привычки отмечены за сегодня:
            - Показывает сообщение "На сегодня все привычки отмечены"
        Если прошёл 21 день:
            - Поздравление и предложение начать новый цикл
        Иначе:
            - Для каждой привычки показывает кнопки выбора статуса
            - Если ответ уже дан сегодня — показывает статус (✅/❌)
        """
        for widget in self.right_container.winfo_children():
            widget.destroy()

        self.text_cat.config(text=get_random_phrase("make_habit"))

        # Проверка: прошло ли 21 день с создания привычек
        if self.db.exmntn_21():
            self.text_cat.config(text=get_random_phrase("21_day"))
            Label(self.right_container, text='Есть привычка!\n🔥 21 день — ты доказал(а) себе,\nчто можешь\n😺💗', font=('Comic Sans MS', 13), bg=bg_light, fg=fg_white).place(relx=0.03, rely=0.1)
            next = Button(self.right_container, text="Новые победы не ждут, let's go ещё :)", bg=bg_dark, fg=fg_white, font=('Comic Sans MS', 10))
            next.place(relx=0.075, rely=0.7)
            next.bind('<Button-1>', lambda e: self.delete_btn())

        else:
            # Проверка: все ли привычки на сегодня отмечены
            if int(self.db.count_active()) % 3 == 0 and int(self.db.count_active()) != 0:
                for widget in self.right_container.winfo_children():
                    widget.destroy()
                Label(self.right_container, text='На сегодня все привычки отмечены.\nПриходите завтра  😺💗', font=('Comic Sans MS', 12), bg=bg_light, fg=fg_white).place(relx=0.03, rely=0.3)
            
            else:
                habits = self.db.text_habits()
                
                # Отображение трёх привычек с кнопками
                status_1 = self.db.get_today_completed_status(habits[0])
                status_2 = self.db.get_today_completed_status(habits[1])
                status_3 = self.db.get_today_completed_status(habits[2])

                # Привычка №1
                Label(self.right_container, text=f'▶ {habits[0]}', 
                    bg=bg_light, fg=fg_black, font=("Comic Sans MS", 11, "bold")).pack(anchor='w', padx=7, pady=(15, 0))
                
                if status_1 is None:
                    Label(self.right_container, text='Вы выполнили эту привычку?', 
                        bg=bg_light, fg=fg_white, font=("Comic Sans MS", 9)).pack(anchor='w', padx=10)
                    
                    btn_yes_1 = btn_yes(self.right_container)
                    btn_no_1 = btn_no(self.right_container)
                    btn_yes_1.place(relx=0.6, rely=0.18)
                    btn_no_1.place(relx=0.7, rely=0.18)
                    
                    btn_yes_1.bind('<Button-1>', lambda event, h=habits[0], by=btn_yes_1, bn=btn_no_1: self.save_active(h, 1, by, bn))
                    btn_no_1.bind('<Button-1>', lambda event, h=habits[0], by=btn_yes_1, bn=btn_no_1: self.save_active(h, 0, by, bn))
                else:
                    status_text = "✅ Выполнено" if status_1 == 1 else "❌ Не выполнено"
                    Label(self.right_container, text=status_text, 
                        bg=bg_light, fg=fg_white, font=("Comic Sans MS", 9)).pack(anchor='w', padx=10)

                # Привычка №2
                Label(self.right_container, text=f'▶ {habits[1]}', 
                    bg=bg_light, fg=fg_black, font=("Comic Sans MS", 11, "bold")).pack(anchor='w', padx=7, pady=(10, 0))
                
                if status_2 is None:
                    Label(self.right_container, text='Вы выполнили эту привычку?', 
                        bg=bg_light, fg=fg_white, font=("Comic Sans MS", 9)).pack(anchor='w', padx=10)
                    
                    btn_yes_2 = btn_yes(self.right_container)
                    btn_no_2 = btn_no(self.right_container)
                    btn_yes_2.place(relx=0.6, rely=0.46)
                    btn_no_2.place(relx=0.7, rely=0.46)
                    
                    btn_yes_2.bind('<Button-1>', lambda event, h=habits[1], by=btn_yes_2, bn=btn_no_2: self.save_active(h, 1, by, bn))
                    btn_no_2.bind('<Button-1>', lambda event, h=habits[1], by=btn_yes_2, bn=btn_no_2: self.save_active(h, 0, by, bn))
                else:
                    status_text = "✅ Выполнено" if status_2 == 1 else "❌ Не выполнено"
                    Label(self.right_container, text=status_text, 
                        bg=bg_light, fg=fg_white, font=("Comic Sans MS", 9)).pack(anchor='w', padx=10)

                # Привычка №3
                Label(self.right_container, text=f'▶ {habits[2]}', 
                    bg=bg_light, fg=fg_black, font=("Comic Sans MS", 11, "bold")).pack(anchor='w', padx=7, pady=(10, 0))
                
                if status_3 is None:
                    Label(self.right_container, text='Вы выполнили эту привычку?', 
                        bg=bg_light, fg=fg_white, font=("Comic Sans MS", 9)).pack(anchor='w', padx=10)
                    
                    btn_yes_3 = btn_yes(self.right_container)
                    btn_no_3 = btn_no(self.right_container)
                    btn_yes_3.place(relx=0.6, rely=0.74)
                    btn_no_3.place(relx=0.7, rely=0.74)
                    
                    btn_yes_3.bind('<Button-1>', lambda event, h=habits[2], by=btn_yes_3, bn=btn_no_3: self.save_active(h, 1, by, bn))
                    btn_no_3.bind('<Button-1>', lambda event, h=habits[2], by=btn_yes_3, bn=btn_no_3: self.save_active(h, 0, by, bn))
                else:
                    status_text = "✅ Выполнено" if status_3 == 1 else "❌ Не выполнено"
                    Label(self.right_container, text=status_text, 
                        bg=bg_light, fg=fg_white, font=("Comic Sans MS", 9)).pack(anchor='w', padx=10)

    def save_active(self, text, type, widget1, widget2, event=None):
        """
        Сохраняет ответ пользователя о выполнении привычки.
        
        Аргументы:
            text (str): Название привычки
            type (int): 1 — выполнено, 0 — не выполнено
            widget1, widget2 (Button): Кнопки "Да"/"Нет" (удаляются после ответа)
        """
        # Защита от повторного ответа
        if self.db.get_today_completed_status(text) is not None:
            widget1.destroy()
            widget2.destroy()
            return
        
        self.db.add_habit_log(text, type)
        widget1.destroy()
        widget2.destroy()
        
        self.make_habits()

        # Если все привычки сегодня отмечены
        if int(self.db.count_active()) % 3 == 0 and int(self.db.count_active()) != 0:
            for widget in self.right_container.winfo_children():
                widget.destroy()
            Label(self.right_container, text='На сегодня все привычки отмечены.\nПриходи завтра  😺💗', font=('Comic Sans MS', 12), bg=bg_light, fg=fg_white).place(relx=0.03, rely=0.3)

    def statystic_habits(self):
        """
        Отображает статистику по каждой привычке:
        - Процент выполнения
        - Текущий стрик (дней подряд)
        - Максимальный стрик
        """
        for widget in self.right_container.winfo_children():
            widget.destroy()

        self.text_cat.config(text=get_random_phrase("statistics"))
        
        if not(int(self.db.count_habits()) > 0):
            Label(self.right_container, text='Здесь появятся данные о проценте\nвыполнения привычек, а также\nо текущем и максимальном стриках\n📊', bg=bg_light, fg=fg_white,font=('Comic Sans MS', 12)).place(relx=0.03, rely=0.2)
        else:
            Label(self.right_container, text="📊 Статистика привычек",  font=("Comic Sans MS", 12, "bold", "underline"), bg=bg_light, fg=fg_white).pack(padx=(0, 20))

            Label(self.right_container, text=f'▶ {self.db.text_habits()[0]}', 
            bg=bg_light, fg=fg_black, font=("Comic Sans MS", 11, "bold")).pack(anchor='w', padx=7, pady=(5, 1))
            Label(self.right_container, text=f'Выполнение: {self.db.get_procent_completed(self.db.text_habits()[0])}% | Стрик: {self.db.strik(self.db.text_habits()[0])}д | Макс. стрик: {self.db.max_strik(self.db.text_habits()[0])}д', 
            bg=bg_light, fg=fg_white, font=("Comic Sans MS", 9)).pack(anchor='w', padx=8)

            Label(self.right_container, text=f'▶ {self.db.text_habits()[1]}', 
            bg=bg_light, fg=fg_black, font=("Comic Sans MS", 11, "bold")).pack(anchor='w', padx=7, pady=(5, 1))
            Label(self.right_container, text=f'Выполнение: {self.db.get_procent_completed(self.db.text_habits()[1])}% | Стрик: {self.db.strik(self.db.text_habits()[1])}д | Макс. стрик: {self.db.max_strik(self.db.text_habits()[1])}д', 
            bg=bg_light, fg=fg_white, font=("Comic Sans MS", 9)).pack(anchor='w', padx=8)

            Label(self.right_container, text=f'▶ {self.db.text_habits()[2]}', 
            bg=bg_light, fg=fg_black, font=("Comic Sans MS", 11, "bold")).pack(anchor='w', padx=7, pady=(5, 1))
            Label(self.right_container, text=f'Выполнение: {self.db.get_procent_completed(self.db.text_habits()[2])}% | Стрик: {self.db.strik(self.db.text_habits()[2])}д | Макс. стрик: {self.db.max_strik(self.db.text_habits()[2])}д', 
            bg=bg_light, fg=fg_white, font=("Comic Sans MS", 9)).pack(anchor='w', padx=8)

    def start_move(self, event):
        """Позиция клика"""
        self.root.start_x = event.x_root - self.root.winfo_x()
        self.root.start_y = event.y_root - self.root.winfo_y()

    def on_move(self, event):
        """Перемещение окна"""
        x = event.x_root - self.root.start_x
        y = event.y_root - self.root.start_y
        self.root.geometry(f'+{x}+{y}')