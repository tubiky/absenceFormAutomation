import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from reportManager import ReportManager
from utility import utils
from settings import constants


class InputForm(ttk.Frame):
    def __init__(self, parent, database, back_to_menu):
        super().__init__(parent)

        # 업데이트 시 선택 항목
        self.locked_item = {"id": None}

        # DB Manager
        self.db = database
        self.back_to_menu = back_to_menu

        self.abs_label = tk.Label(self, text="결석생 등록 화면", font=("Arial", 20))
        self.abs_label.pack(pady=20)

        # 학생 번호 입력
        self.stdNo_label = tk.Label(self, text="번호:", font=("Arial", 14))
        self.stdNo_label.pack(anchor="w", padx=10)
        self.stdNo_entry = ttk.Entry(
            self,
        )
        self.stdNo_entry.pack(fill="x", ipadx=30, ipady=6, padx=10, pady=10)

        # 결석 기간 입력
        self.period_label = tk.Label(
            self, text="결석 기간 (시작일):", font=("Arial", 14)
        )
        self.period_label.pack(anchor="w", padx=10)

        self.frame_start_date = tk.Frame(self)
        self.frame_start_date.pack(fill="x", padx=10)

        self.start_year_combobox = ttk.Combobox(
            self.frame_start_date,
            values=[str(y) for y in range(2024, 2050)],
            width=5,
            height=18,
        )
        self.start_year_combobox.pack(side="left", pady=10)
        self.start_year_combobox.set("년")

        self.start_month_combobox = ttk.Combobox(
            self.frame_start_date,
            values=[f"{m:02}" for m in range(1, 13)],
            width=4,
            height=18,
        )
        self.start_month_combobox.pack(side="left", padx=5, pady=10)
        self.start_month_combobox.set("월")

        self.start_day_combobox = ttk.Combobox(
            self.frame_start_date,
            values=[f"{d:02}" for d in range(1, 32)],
            width=4,
            height=18,
        )
        self.start_day_combobox.pack(side="left", pady=10)
        self.start_day_combobox.set("일")

        self.period_end_label = tk.Label(
            self, text="결석 기간 (종료일):", font=("Arial", 14)
        )
        self.period_end_label.pack(anchor="w", padx=10)

        self.frame_end_date = tk.Frame(self)
        self.frame_end_date.pack(fill="x", padx=10)

        # 결석 종료일 입력
        self.end_year_combobox = ttk.Combobox(
            self.frame_end_date, values=[str(y) for y in range(2024, 2050)], width=5
        )
        self.end_year_combobox.pack(side="left", pady=10)
        self.end_year_combobox.set("")

        self.end_month_combobox = ttk.Combobox(
            self.frame_end_date, values=[f"{m:02}" for m in range(1, 13)], width=4
        )
        self.end_month_combobox.pack(side="left", padx=5, pady=10)
        self.end_month_combobox.set("")

        self.end_day_combobox = ttk.Combobox(
            self.frame_end_date, values=[f"{d:02}" for d in range(1, 32)], width=4
        )
        self.end_day_combobox.pack(side="left", pady=10)
        self.end_day_combobox.set("")

        # 결석 종류 선택
        self.reason_label = tk.Label(self, text="결석 종류:", font=("Arial", 14))
        self.reason_label.pack(anchor="w", padx=10)
        self.reason_combobox = ttk.Combobox(self, values=["인정", "질병", "기타"])
        self.reason_combobox.pack(fill="x", ipadx=30, ipady=6, padx=10, pady=10)

        # 상세 사유 입력
        self.detailed_reason_label = tk.Label(
            self, text="결석 사유:", font=("Arial", 14)
        )
        self.detailed_reason_label.pack(anchor="w", padx=10)
        self.detailed_reason_entry = ttk.Entry(self)
        self.detailed_reason_entry.pack(fill="x", ipadx=30, ipady=6, padx=10, pady=10)

        # 저장 버튼
        self.save_button = tk.Button(
            self, text="결석생 등록[Enter]", command=self.save_absence
        )
        self.save_button.pack(pady=10)

        # 데이터 표시
        # id, std_class, std_no, name, start_date, end_date, reason, detailed_reason
        self.tree = ttk.Treeview(
            self,
            columns=(
                "id",
                "std_class",
                "std_no",
                "name",
                "start_date",
                "end_date",
                "type",
                "reason",
            ),
            show="headings",
        )
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=40, anchor="center")
        self.tree.heading("std_class", text="반")
        self.tree.column("std_class", width=40, anchor="center")
        self.tree.heading("std_no", text="번호")
        self.tree.column("std_no", width=40, anchor="center")
        self.tree.heading("name", text="이름")
        self.tree.column("name", width=40, anchor="center")
        self.tree.heading("start_date", text="결석 시작일")
        self.tree.column("start_date", width=50, anchor="center")
        self.tree.heading("end_date", text="결석 종료일")
        self.tree.column("end_date", width=50, anchor="center")
        self.tree.heading("type", text="결석 종류")
        self.tree.column("type", width=40, anchor="center")
        self.tree.heading("reason", text="결석 사유", anchor="center")
        self.tree.column("reason", width=50, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # 삭제 버튼
        self.delete_button = tk.Button(
            self, text="삭제[Ctrl+d]", command=self.delete_absence
        )
        self.delete_button.pack(side="left", padx=10, pady=10)

        # 수정 버튼
        self.edit_button = tk.Button(
            self, text="수정[Ctrl+m]", command=self.edit_absence
        )
        self.edit_button.pack(side="left", padx=10, pady=10)

        # 돌아가기 버튼
        self.back_button = tk.Button(
            self, text="돌아가기[Ctrl+b]", command=self.back_to_menu
        )
        self.back_button.pack(side="right", padx=10, pady=10)

    def pack_input_form(self):
        self.pack(fill="both", expand=True)

    # 결석 데이터 저장
    def save_absence(self, event=None):
        student_no = self.stdNo_entry.get()

        # 학생 번호를 미입력한 경우 정지
        if student_no == "":
            messagebox.showerror("학생 번호 누락", "학생 번호를 입력하세요.")
            return

        # 학생 번호가 정확한 경우 실행
        else:
            std_info = utils.find_student(int(student_no))
            name = std_info["name"]
            stdClass = int(std_info["class"])
            stdNo = int(std_info["no"])
            start_year = self.start_year_combobox.get()
            start_month = self.start_month_combobox.get()
            start_day = self.start_day_combobox.get()
            end_year = self.end_year_combobox.get()
            end_month = self.end_month_combobox.get()
            end_day = self.end_day_combobox.get()
            abs_type = self.reason_combobox.get()
            reason = self.detailed_reason_entry.get()

            if (
                stdNo == ""
                or not name
                or not start_year
                or not start_month
                or not start_day
                or not reason
            ):
                messagebox.showerror("입력 오류", "모든 필드를 입력해주세요.")
                return

            if not end_year or not end_month or not end_day:
                end_year, end_month, end_day = start_year, start_month, start_day

            start_date = f"{start_year}-{start_month}-{start_day}"
            end_date = f"{end_year}-{end_month}-{end_day}"

        with self.db.conn:
            self.db.cursor.execute(
                "INSERT INTO absences (std_class, std_no, name, start_date, end_date, abs_type, reason) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (stdClass, stdNo, name, start_date, end_date, abs_type, reason),
            )

        self.display_absences()

        # 입력 칸을 모두 초기화
        self.clear_all_input_entry()

    def clear_all_input_entry(self):
        self.stdNo_entry.delete(0, tk.END)
        self.start_year_combobox.set("")
        self.start_month_combobox.set("")
        self.start_day_combobox.set("")
        self.end_year_combobox.set("")
        self.end_month_combobox.set("")
        self.end_day_combobox.set("")
        self.reason_combobox.set("")
        self.detailed_reason_entry.delete(0, tk.END)

    def display_absences(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        with self.db.conn:
            # id, std_class, std_no, name, start_date, end_date, reason, detailed_reason
            self.db.cursor.execute(
                "SELECT id, std_class, std_no, name, start_date, end_date, abs_type, reason FROM absences"
            )
            rows = self.db.cursor.fetchall()

            for row in rows:
                self.tree.insert(
                    "", tk.END, values=row, iid=row[0]
                )  # iid stands for Item ID

    # 결석계 데이터 DataFrame형태로 리턴
    def create_dataframe_from_sqlite(self, *args):
        with self.db.conn:
            query = "SELECT id, std_class, std_no, name, start_date, end_date, abs_type, reason FROM absences"
            df = pd.read_sql_query(query, self.db.conn)
            df = df.astype(
                {"start_date": "datetime64[ns]", "end_date": "datetime64[ns]"}
            )

            # Localize to UTC timezone

            df["start_date"] = df["start_date"].dt.tz_localize("UTC")
            df["end_date"] = df["end_date"].dt.tz_localize("UTC")

            return df

    # 데이터 초기화 함수
    def reset_database(self, *args):
        if messagebox.askyesno(
            "데이터 초기화", "정말로 모든 데이터를 초기화하시겠습니까?"
        ):
            with self.db.conn:
                # id, std_class, std_no, name, start_date, end_date, reason, detailed_reason
                self.db.cursor.execute("DELETE from absences")
                self.db.cursor.execute(
                    "DELETE FROM sqlite_sequence WHERE name = 'absences'"
                )
                self.display_absences()
                messagebox.showinfo("초기화 완료", "모든 데이터가 초기화되었습니다.")

    def delete_absence(self, event=None):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("선택 오류", "삭제할 항목을 선택해주세요.")
            return

        for item in selected_item:
            with self.db.conn:
                # id, std_class, std_no, name, start_date, end_date, abs_type, reason
                self.db.cursor.execute(
                    "DELETE FROM absences WHERE id = ?",
                    (self.tree.item(item)["values"][0],),
                )

                self.tree.delete(item)

    def edit_absence(self, event=None):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("선택 오류", "수정할 항목을 선택해주세요.")
            return

        if self.locked_item["id"] is None:
            # 첫 선택 → 고정
            self.locked_item["id"] = selected_item[0]

        self.edit_button.config(state="disabled")

        # 업데이트 버튼
        self.update_button = tk.Button(
            self, text="업데이트", command=self.update_absence
        )
        self.update_button.pack(side="left", padx=10, pady=10)
        item_id = selected_item[0]
        values = self.tree.item(item_id)["values"]

        # id, std_class, std_no, name, start_date, end_date, abs_type, reason
        self.stdNo_entry.delete(0, tk.END)
        self.stdNo_entry.insert(0, values[2])

        start_year, start_month, start_day = values[4].split("-")
        self.start_year_combobox.set(start_year)
        self.start_month_combobox.set(start_month)
        self.start_day_combobox.set(start_day)

        end_year, end_month, end_day = values[5].split("-")
        self.end_year_combobox.set(end_year)
        self.end_month_combobox.set(end_month)
        self.end_day_combobox.set(end_day)

        self.reason_combobox.set(values[6])
        self.detailed_reason_entry.delete(0, tk.END)
        self.detailed_reason_entry.insert(0, values[7])

    def update_absence(self, *args):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("선택 오류", "수정할 항목을 선택해주세요.")
            return

        if selected_item[0] != self.locked_item["id"]:
            print(f"선택된 항목이 수정하려는 항목과 다릅니다.")
            self.tree.selection_set(self.locked_item["id"])

        item_id = self.locked_item["id"]
        values = self.tree.item(item_id)["values"]

        # id, std_class, std_no, name, start_date, end_date, abs_type, reason
        std_no = self.stdNo_entry.get()
        stdInfo = utils.find_student(int(std_no))
        name = stdInfo["name"]
        std_class = int(stdInfo["class"])
        start_year = self.start_year_combobox.get()
        start_month = self.start_month_combobox.get()
        start_day = self.start_day_combobox.get()
        end_year = self.end_year_combobox.get()
        end_month = self.end_month_combobox.get()
        end_day = self.end_day_combobox.get()
        reason = self.reason_combobox.get()
        detailed_reason = self.detailed_reason_entry.get()

        if not name or not start_year or not start_month or not start_day or not reason:
            messagebox.showerror("입력 오류", "모든 필드를 입력해주세요.")
            return

        if not end_year or not end_month or not end_day:
            end_year, end_month, end_day = start_year, start_month, start_day

        start_date = f"{start_year}-{start_month}-{start_day}"
        end_date = f"{end_year}-{end_month}-{end_day}"

        with self.db.conn:
            # id, std_class, std_no, name, start_date, end_date, abs_type, reason
            self.db.cursor.execute(
                "UPDATE absences SET std_class = ?, std_no = ?, name = ?, start_date = ?, end_date = ?, abs_type = ?, reason = ? WHERE id = ?",
                (
                    std_class,
                    std_no,
                    name,
                    start_date,
                    end_date,
                    reason,
                    detailed_reason,
                    values[0],
                ),
            )
        self.display_absences()
        self.update_button.destroy()

        self.clear_all_input_entry()
        self.unlock()
        self.edit_button.config(state="normal")

    def unlock(self):
        # 락 해제
        self.locked_item["id"] = None
        self.tree.selection_remove(self.tree.selection())  # 선택 해제

    def create_report(self, *args):
        df = self.create_dataframe_from_sqlite()
        document = ReportManager(df)
        document.open()
        document.makeCopies()
        document.fill_in_absence_info()
