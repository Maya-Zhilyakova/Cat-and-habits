from tkinter import Button, Checkbutton, BooleanVar
import json
import random
import sys
import os

fg_white = "#e7dede"
fg_black = "#181327"

bg_dark = "#26124C"
bg_info = "#513B68"
fg_info_right = "#7F6A95"
entry = "#e0d4ec"
bg_light = "#7C5E9A"
bg_btn_close = "#d63232"
bg_btn_open = "#5ed632"
bg_btn_ok = "#7821cf"
bg_btn_left = "#7632BA"
bg_title = "#533e6b"
bg_active = "#653892"
'''
bg_dark = "#2D1B4E"
bg_info = "#513B68"
fg_info_right = "#7F6A95"
entry = "#e0d4ec"
bg_light = "#7C5E9A"
bg_btn_close = "#d63232"
bg_btn_open = "#5ed632"
bg_btn_ok = "#7821cf"
bg_btn_left = "#653892"
bg_title = "#533e6b"
bg_active = "#653892"
'''
# Загрузка фраз кота с корректным путём для .exe


def get_random_phrase(category):
    return random.choice(phrases['categories'][category])

def resource_path(relative_path):
    """Получить абсолютный путь к файлу, работает и в .exe и в .py"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

json_path = resource_path('text_for_little.json')
with open(json_path, 'r', encoding='utf-8') as file:
    phrases = json.load(file)

def btn_left(window, text, command):
    return Button(
        window,
        bg=bg_btn_left,
        fg=fg_white,
        text=text,
        command=command,
        borderwidth=0,
        font=('Comic Sans MS', 11)
    )

def btn_checkbutton(window, text):
    var = BooleanVar()
    return Checkbutton(
        window, 
        text=text, 
        variable=var, 
        bg=bg_active, 
        font=("Comic Sans MS", 10), 
        indicatoron=False, 
        width=20, 
        height=1, 
        selectcolor=bg_dark, 
        activebackground=bg_active,
        fg=fg_white,
        justify='left'
    )

def btn_yes(window):
    return  Button(
        window,
        bg=bg_btn_open,
        fg=fg_black,
        text='Да',
        borderwidth=0,
        font=('Comic Sans MS', 9)
    )

def btn_no(window):
    return  Button(
        window,
        bg=bg_btn_close,
        fg=fg_black,
        text='Нет',
        height=1,
        borderwidth=0,
        font=('Comic Sans MS', 9)
    )