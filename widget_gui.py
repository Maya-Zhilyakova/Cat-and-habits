from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, askyesno, showwarning
from PIL import Image, ImageTk

from utils import *
from base_data import DataBase

class Gui:
    def __init__(self):
        self.root = Tk()
        self.left_conteiner = None
        self.right_container = None
        self.up_right_container = None
        self.canvas = None
        self.db = DataBase()
        self.db.create_table()
        self.text_cat = None

    def all_part(self):
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

        self.db.add_null_day()

        self.left_panel()
        self.up_right_panel()

        self.cat()

        update_color = Button()

        self.root.mainloop()

    def cat(self):
        self.right_container = Frame(self.root, bg=bg_light, width=420, height=240)
        self.right_container.place(relx=0.3, rely=0.24)
        self.right_container.pack_propagate(False)
        import random

        img = Image.open(random.choice(['Images/cat_one.jpg', 'Images/cat_two.jpg', 'Images/cat_three.jpg'])).resize((190, 190), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        cat = Label(self.right_container, width=190, height=190, image=photo, borderwidth=0)
        cat.image = photo

        Label(self.right_container, text=random.choice([get_random_phrase("cat_main")]), bg=bg_light, fg=fg_white, justify='left', font=("Comic Sans MS", 10)).place(relx=0.55, rely=0.05)


        cat.place(relx=0.1, rely=0.1)

        btn_menu = btn_left(self.left_container, '😺 Кот', self.cat)
        btn_menu.place(relx=0.05, rely=0.02)

        btn_3_back = btn_left(self.left_container, '⚙️ Трекер\nпривычек', self.add_habit)
        btn_3_back.place(relx=0.05, rely=0.2)

        btn_3_forward = btn_left(self.left_container, '📊 Статистика\n выполнения', self.statistic_habits)
        btn_3_forward.place(relx=0.05, rely=0.465)

        btn_statistic_mb = btn_left(self.left_container, '♻️ Сбросить\n данные', self.delete_datas)
        btn_statistic_mb.place(relx=0.05, rely=0.73)

        line = Frame(self.root, height=2, width=600, bg=bg_title)
        line.place(relx=0.3, rely=0.24)

        line2 = Frame(self.root, height=600, width=2, bg=bg_title)
        line2.place(relx=0.3, rely=0.08)

    def left_panel(self):
        self.left_container = Frame(self.root, bg=bg_dark, width=210)
        self.left_container.pack(fill=Y, expand=True, side=LEFT, anchor='w')
        self.left_container.pack_propagate(False)

    def up_right_panel(self):
        self.up_right_container = Frame(self.root, bg=bg_dark, width=420, height=60)
        self.up_right_container.place(relx=0.3, rely=0.08)
        self.up_right_container.pack_propagate(False)

        self.text_cat = Label(self.up_right_container, text=f"😺 — Посмотри статистику сейчас.\nПосле добавления новых данные удалятся.", bg=bg_dark, fg=fg_white, font=("Comic Sans MS", 10), justify='left')
        self.text_cat.place(x=8, y=-3)
        self.text_cat.config(text=get_random_phrase("main_menu"))

    def add_habit(self):

        for widget in self.right_container.winfo_children():
            widget.destroy()
        if self.db.count_habits() > 0:
            self.make_habits()
        else:
            self.text_cat.config(text=get_random_phrase("add_habit"))
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
        if place_1.get() != "" and place_2.get() != "" and place_3.get() != "":
            self.db.create_table()
            habit_1 = place_1.get()
            self.db.insert_habit(habit_1)

            habit_2 = place_2.get()
            self.db.insert_habit(habit_2)

            habit_3 = place_3.get()
            self.db.insert_habit(habit_3)

            self.make_habits()
        else:
            self.exination_empty()

    def delete_btn(self):
        self.db.delete_21()
        self.add_habit()

    def delete_datas(self):
        result = askyesno(title="Подтвержение удаления данных", message="Ты точно уверен(а), что хочешь стереть весь прогресс?😿")
        if result:
            showinfo("Удаление", "Данные все стерты")
            self.delete_btn()
        else:
            showinfo("Сохранение", "Данные остались нетронутыми")

    def exination_empty(self):
        showwarning(title="Предупреждение", message="Введите данные во все поля")

    def make_habits(self):
        for widget in self.right_container.winfo_children():
            widget.destroy()

        if self.db.exmntn_21():
            self.text_cat.config(text=get_random_phrase("21_day"))
            Label(self.right_container, text='Есть привычка!\n🔥 21 день — ты доказал(а) себе,\nчто можешь\n😺💗', font=('Comic Sans MS', 13), bg=bg_light, fg=fg_white).place(relx=0.03, rely=0.1)
            next = Button(self.right_container, text = "Новые победы не ждут, let's go ещё :)", bg=bg_dark, fg=fg_white, font=('Comic Sans MS', 10))
            next.place(relx=0.075, rely=0.7)
            next.bind('<Button-1>', self.delete_btn)

        else:
            self.text_cat.config(text=get_random_phrase("make_habit"))
            today_count = self.db.count_active()
        
            if today_count == 3:
            
                for widget in self.right_container.winfo_children():
                    widget.destroy()
                Label(self.right_container, text='На сегодня все привычки отмечены.\nПриходите завтра  😺💗', font=('Comic Sans MS', 12), bg=bg_light, fg=fg_white).place(relx=0.03, rely=0.3)
            
            else:
                Label(self.right_container, text="✅ Отметка привычек",  font=("Comic Sans MS", 12, "bold", "underline"), bg=bg_light, fg=fg_white).pack(padx=(0, 20))
                Label(self.right_container, text=f'▶ {self.db.text_habits()[0]}', 
                bg=bg_light, fg=fg_black, font=("Comic Sans MS", 11, "bold")).pack(anchor='w', padx=7, pady=(5, 0))
                compl_1 = Label(self.right_container, text='Вы выполнили эту привычку?', 
                bg=bg_light, fg=fg_white, font=("Comic Sans MS", 9))
                compl_1.pack(anchor='w', padx=10)

                btn_yes_1 = btn_yes(self.right_container)
                btn_yes_1.place(relx=0.58, rely=0.28)
                btn_yes_1.bind('<Button-1>',  lambda event: self.save_active(self.db.text_habits()[0], 1))

                btn_no_1 = btn_no(self.right_container)
                btn_no_1.place(relx=0.68, rely=0.28)
                btn_no_1.bind('<Button-1>',  lambda event: self.save_active(self.db.text_habits()[0], 0))

                if self.db.get_today_completed_status(self.db.text_habits()[0]) != None:
                    compl_1.config(text="✅ Выполнено") if self.db.get_today_completed_status(self.db.text_habits()[0]) == 1 else compl_1.config(text="❌ Не выполнено")
                    btn_yes_1.destroy()
                    btn_no_1.destroy()

                Label(self.right_container, text=f'▶ {self.db.text_habits()[1]}', 
                bg=bg_light, fg=fg_black, font=("Comic Sans MS", 11, "bold")).pack(anchor='w', padx=7, pady=(5, 0))
                compl_2 = Label(self.right_container, text='Вы выполнили эту привычку?', 
                bg=bg_light, fg=fg_white, font=("Comic Sans MS", 9))
                compl_2.pack(anchor='w', padx=10)

                btn_yes_2 = btn_yes(self.right_container)
                btn_yes_2.place(relx=0.58, rely=0.56)
                btn_yes_2.bind('<Button-1>',  lambda event: self.save_active(self.db.text_habits()[1], 1))

                btn_no_2 = btn_no(self.right_container)
                btn_no_2.place(relx=0.68, rely=0.56)
                btn_no_2.bind('<Button-1>',  lambda event: self.save_active(self.db.text_habits()[1], 0))

                if self.db.get_today_completed_status(self.db.text_habits()[1]) != None:
                    compl_2.config(text="✅ Выполнено") if self.db.get_today_completed_status(self.db.text_habits()[1]) == 1 else compl_2.config(text="❌ Не выполнено")
                    btn_yes_2.destroy()
                    btn_no_2.destroy()
                    
                Label(self.right_container, text=f'▶ {self.db.text_habits()[2]}', 
                bg=bg_light, fg=fg_black, font=("Comic Sans MS", 11, "bold")).pack(anchor='w', padx=7, pady=(5, 0))
                compl_3 = Label(self.right_container, text='Вы выполнили эту привычку?', 
                bg=bg_light, fg=fg_white, font=("Comic Sans MS", 9))
                compl_3.pack(anchor='w', padx=10)

                btn_yes_3 = btn_yes(self.right_container)
                btn_yes_3.place(relx=0.58, rely=0.81)
                btn_yes_3.bind('<Button-1>',  lambda event:  self.save_active(self.db.text_habits()[2], 1))

                btn_no_3 = btn_no(self.right_container)
                btn_no_3.place(relx=0.68, rely=0.81)
                btn_no_3.bind('<Button-1>',  lambda event: self.save_active(self.db.text_habits()[2], 0))

                if self.db.get_today_completed_status(self.db.text_habits()[2]) != None:
                    compl_3.config(text="✅ Выполнено") if self.db.get_today_completed_status(self.db.text_habits()[2]) == 1 else compl_3.config(text="❌ Не выполнено")
                    btn_yes_3.destroy()
                    btn_no_3.destroy()

    def save_active(self, text, type, event=None):
        self.db.add_habit_log(text, type)
        self.make_habits()

    def statistic_habits(self):
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
        # Позиция клика
        self.root.start_x = event.x_root - self.root.winfo_x()
        self.root.start_y = event.y_root - self.root.winfo_y()

    def on_move(self, event):
        # Перемещение окна
        x = event.x_root - self.root.start_x
        y = event.y_root - self.root.start_y
        self.root.geometry(f'+{x}+{y}')