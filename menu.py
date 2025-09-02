import sys
import tkinter as tk
from tkinter import ttk, simpledialog
from settings.constants import *
from utility import utils


class Menu(ttk.Frame):
    def __init__(self, parent, database, inputForm):
        super().__init__(master=parent)

        # 데이터 베이스 셋업
        self.db = database
        self.inputForm = inputForm

        # 위젯 생성
        self.label = tk.Label(master=self, text="담임교사 성명:", font=FONT_NORMAL)
        self.teacher_enroll_btn = tk.Button(
            master=self,
            text="담임교사 성명 등록<F2>",
            font=FONT_NORMAL,
            command=self.set_teacher_name,
        )
        self.absence_info_edit_btn = tk.Button(
            master=self,
            text="결석 정보 입력 및 수정<F3>",
            font=FONT_NORMAL,
            command=self.pack_inputForm,
        )
        self.absence_info_reset_btn = tk.Button(
            master=self,
            text="결석 정보 초기화<F4>",
            font=FONT_NORMAL,
            command=self.inputForm.reset_database,
        )
        self.generate_btn = tk.Button(
            master=self,
            text="결석계 생성<F5>",
            font=FONT_NORMAL,
            command=self.inputForm.create_report,
        )
        self.quit_btn = tk.Button(
            master=self, text="종료<F8>", font=FONT_NORMAL, command=self.turn_off
        )

        self.pack_widgets()

    def pack_widgets(self):
        self.label.pack(pady=20)
        self.teacher_enroll_btn.pack(pady=20)
        self.absence_info_edit_btn.pack(pady=20)
        self.absence_info_reset_btn.pack(pady=20)
        self.generate_btn.pack(pady=20)
        self.quit_btn.pack(pady=20)

    def pack_menu(self):
        self.pack()

    def pack_inputForm(self, *args):
        self.pack_forget()
        self.inputForm.pack_input_form()
        self.inputForm.display_absences()

    def set_teacher_name(self, *args):
        name = simpledialog.askstring(
            "담임교사 성명 등록", "담임교사 성명을 입력해주세요:"
        )
        if name:
            utils.teacher_name = name
            self.label.config(text=f"담임교사 성명: {utils.teacher_name}")

    def turn_off(self, *args):
        sys.exit()
