import tkinter as tk
from menu import Menu
from databaseManager import DataManager
from inputForm import InputForm
from settings.constants import *


class Application(tk.Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title)
        self.geometry("800x800")

        # Activate Widgets
        self.db = DataManager("attendance.db")
        self.inputForm = InputForm(self, self.db, self.show_menu)
        self.menu = Menu(self, self.db, self.inputForm)
        self.menu.pack_menu()

        # Shortcuts bind
        self.shortcuts()

        # Run
        self.mainloop()

    def show_menu(self, *args):
        self.inputForm.pack_forget()
        self.menu.pack()

    def shortcuts(self, *args):
        self.bind("<F2>", self.menu.set_teacher_name)  # 담임교사 성명 등록
        self.bind("<F3>", self.menu.pack_inputForm)  # 결석생 데이터 등록 및 수정
        self.bind("<F4>", self.inputForm.reset_database)  # 결석생 데이터 초기화
        self.bind("<F5>", self.inputForm.create_report)  # 결석계 생성
        self.bind("<F8>", self.menu.turn_off)  # 프로그램 종료
        self.bind("<Return>", self.inputForm.save_absence)
        self.bind("<Control-m>", self.inputForm.edit_absence)
        self.bind("<Control-d>", self.inputForm.delete_absence)
        self.bind("<Control-b>", self.inputForm.back_to_menu)


Application("결석계 자동화 프로그램 Ver 2.0")
