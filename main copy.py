import os
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
import sqlite3
import pandas as pd
from pyhwpx import Hwp

# 담임교사 성명 설정
teacher_name = ""

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()


# 데이터베이스 초기화
def initialize_database():
    with conn:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS absences (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            std_class INTEGER NOT NULL,
                            std_no INTEGER NOT NULL,
                            name TEXT NOT NULL,
                            start_date TEXT NOT NULL,
                            end_date TEXT NOT NULL,
                            reason TEXT NOT NULL,
                            detailed_reason TEXT)"""
        )


def set_teacher_name(*args):
    global teacher_name, teacher_name_label
    name = simpledialog.askstring("담임교사 성명 등록", "담임교사 성명을 입력해주세요:")
    if name:
        teacher_name = name
        teacher_name_label.config(text=f"담임교사 성명: {teacher_name}")


def edit_teacher_name(*args):
    set_teacher_name()


# 데이터 초기화 함수
def reset_database(*args):
    if messagebox.askyesno("데이터 초기화", "정말로 모든 데이터를 초기화하시겠습니까?"):
        with conn:
            cursor.execute("DELETE FROM absences")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name = ?;", ("absences",))
            display_absences()
            messagebox.showinfo("초기화 완료", "모든 데이터가 초기화되었습니다.")


# 결석 데이터 저장
def save_absence(*args):
    student_no = stdNo_entry.get()
    if find_student(int(student_no)) == None:
        return

    # 학생의 반과 번호를 Dictionary형태로 return
    std_info = find_student(int(student_no))
    name = std_info["name"]
    stdClass = int(std_info["class"])
    stdNo = int(std_info["no"])
    start_year = start_year_combobox.get()
    start_month = start_month_combobox.get()
    start_day = start_day_combobox.get()
    end_year = end_year_combobox.get()
    end_month = end_month_combobox.get()
    end_day = end_day_combobox.get()
    reason = reason_combobox.get()
    detailed_reason = detailed_reason_entry.get()

    if not name or not start_year or not start_month or not start_day or not reason:
        messagebox.showerror("입력 오류", "모든 필드를 입력해주세요.")
        return

    if not end_year or not end_month or not end_day:
        end_year, end_month, end_day = start_year, start_month, start_day

    start_date = f"{start_year}-{start_month}-{start_day}"
    end_date = f"{end_year}-{end_month}-{end_day}"

    with conn:
        cursor.execute(
            "INSERT INTO absences (std_class, std_no, name, start_date, end_date, reason, detailed_reason) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (stdClass, stdNo, name, start_date, end_date, reason, detailed_reason),
        )

    display_absences()

    # 입력 칸을 모두 초기화
    stdNo_entry.delete(0, tk.END)
    start_year_combobox.set("")
    start_month_combobox.set("")
    start_day_combobox.set("")
    end_year_combobox.set("")
    end_month_combobox.set("")
    end_day_combobox.set("")
    reason_combobox.set("")
    detailed_reason_entry.delete(0, tk.END)


def convert_stdInfo_to_dataframe():
    base = os.getcwd()
    file_path = base + "/excel_form/students.xlsx"

    students_df = pd.read_excel(file_path)
    students_df.set_index("번호", inplace=True)

    return students_df


def find_student(idx):
    std_info = {}
    if idx not in students_df.index.values:
        messagebox.showerror("학생 조회 실패", "입력한 번호의 학생 정보가 없습니다.")
        return
    else:
        std_name, std_class = (
            students_df.loc[idx]["이름"],
            students_df.loc[idx]["반"],
        )

        std_info["name"] = std_name
        std_info["class"] = std_class
        std_info["no"] = idx

    return std_info


# 저장된 데이터 표시
def display_absences():
    for row in tree.get_children():
        tree.delete(row)

    with conn:
        # id, std_class, std_no, name, start_date, end_date, reason, detailed_reason
        cursor.execute(
            "SELECT id, std_class, std_no, name, start_date, end_date, reason, detailed_reason FROM absences"
        )
        rows = cursor.fetchall()

        for row in rows:
            tree.insert("", tk.END, values=row, iid=row[0])  # iid stands for Item ID


def delete_absence(*args):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("선택 오류", "삭제할 항목을 선택해주세요.")
        return

    for item in selected_item:
        conn = sqlite3.connect("attendance.db")
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM absences WHERE id = ?", (tree.item(item)["values"][0],)
        )
        conn.commit()
        conn.close()
        tree.delete(item)


def edit_absence(*args):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("선택 오류", "수정할 항목을 선택해주세요.")
        return

    item_id = selected_item[0]
    values = tree.item(item_id)["values"]
    print(values)

    # id, std_class, std_no, name, start_date, end_date, reason, detailed_reason
    stdNo_entry.delete(0, tk.END)
    stdNo_entry.insert(0, values[2])

    start_year, start_month, start_day = values[3].split("-")
    start_year_combobox.set(start_year)
    start_month_combobox.set(start_month)
    start_day_combobox.set(start_day)

    end_year, end_month, end_day = values[4].split("-")
    end_year_combobox.set(end_year)
    end_month_combobox.set(end_month)
    end_day_combobox.set(end_day)

    reason_combobox.set(values[5])
    detailed_reason_entry.delete(0, tk.END)
    detailed_reason_entry.insert(0, values[6])

    def update_absence():
        # id, std_class, std_no, name, start_date, end_date, reason, detailed_reason
        std_no = stdNo_entry.get()
        stdInfo = find_student(std_no)
        name = stdInfo["name"]
        std_class = stdInfo["class"]
        start_year = start_year_combobox.get()
        start_month = start_month_combobox.get()
        start_day = start_day_combobox.get()
        end_year = end_year_combobox.get()
        end_month = end_month_combobox.get()
        end_day = end_day_combobox.get()
        reason = reason_combobox.get()
        detailed_reason = detailed_reason_entry.get()

        if not name or not start_year or not start_month or not start_day or not reason:
            messagebox.showerror("입력 오류", "모든 필드를 입력해주세요.")
            return

        if not end_year or not end_month or not end_day:
            end_year, end_month, end_day = start_year, start_month, start_day

        start_date = f"{start_year}-{start_month}-{start_day}"
        end_date = f"{end_year}-{end_month}-{end_day}"

        conn = sqlite3.connect("attendance.db")
        cursor = conn.cursor()
        # id, std_class, std_no, name, start_date, end_date, reason, detailed_reason
        cursor.execute(
            "UPDATE absences SET std_class = ?, std_no = ?, name = ?, start_date = ?, end_date = ?, reason = ?, detailed_reason = ? WHERE id = ?",
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
        conn.commit()
        conn.close()

        display_absences()
        update_button.destroy()

    update_button = tk.Button(abs_frame, text="업데이트", command=update_absence)
    update_button.pack(pady=10)


def extract_date_info(from_date, to_date):
    period_information = {}

    day_from = from_date.day
    day_to = to_date.day
    period_information["year"] = str(from_date.year)
    period_information["month"] = str(from_date.month)
    period_information["day_from"] = str(from_date.day)
    period_information["day_to"] = str(to_date.day)
    period_information["for_day"] = str(int(day_to + 1) - int(day_from))
    period_information["weekday"] = str(from_date.strftime("%a"))
    period_information["confirmed_date"] = (
        to_date + pd.Timedelta(days=3) if to_date.strftime("%a") == "Fri" else to_date
    )

    return period_information


def generate_absence_report(*args):
    # id, std_class, std_no, name, start_date, end_date, reason, detailed_reason
    conn = sqlite3.connect("attendance.db")
    query = "SELECT id, std_class, std_no, name, start_date, end_date, reason, detailed_reason FROM absences"
    df = pd.read_sql_query(query, conn)

    df = df.astype({"start_date": "datetime64[ns]", "end_date": "datetime64[ns]"})

    # Localize to UTC timezone
    df["start_date"] = df["start_date"].dt.tz_localize("UTC")
    df["end_date"] = df["end_date"].dt.tz_localize("UTC")

    conn.close()

    current_path = os.getcwd()

    # 양식 파일과 hwp 개체 연결하기
    hwp = Hwp(new=True, visible=True)
    hwp.Open(current_path + "/hwp_file_form/결석계.hwp")
    hwp.MoveDocEnd()
    hwp.CopyPage()

    # 결석생 데이터 만큼 결석계표 복사하기
    num_of_absent_students = len(df)

    for _ in range(num_of_absent_students):
        hwp.Paste()

    # 반복문을 활용하여 각 결석계의 양식에 데이터 입력하기
    for n in range(num_of_absent_students):
        # id, std_class, std_no, name, start_date, end_date, reason, detailed_reason
        std_class = df.iloc[n]["std_class"]
        std_no = df.iloc[n]["std_no"]
        student_name = df.iloc[n]["name"]
        from_day = df.iloc[n]["start_date"]
        until_day = df.iloc[n]["end_date"]
        absence_type = df.iloc[n]["reason"]
        detailed_absence_reason = df.iloc[n]["detailed_reason"]

        # 담임 교사 이름 입력
        hwp.move_to_field(f"teacher_name_1{{{{{n}}}}}")
        hwp.insert_text(" ".join(teacher_name))
        hwp.move_to_field(f"teacher_name_2{{{{{n}}}}}")
        hwp.insert_text(" ".join(teacher_name))

        # 학생 이름 입력
        hwp.move_to_field(f"name{{{{{n}}}}}")
        hwp.insert_text(" ".join(student_name))

        # 결석 종류 입력
        hwp.move_to_field(f"absence_type{{{{{n}}}}}")
        if absence_type == "질병":
            hwp.insert_text("인정 (   )   질병 ( O )   기타 (   )")
        elif absence_type == "인정":
            hwp.insert_text("인정 ( O )   질병 (   )   기타 (   )")
        elif absence_type == "기타":
            hwp.insert_text("인정 (   )   질병 (   )   기타 ( O )")
        else:
            pass

        # 상세 결석 사유 입력
        hwp.move_to_field(f"detailed_reason{{{{{n}}}}}")
        hwp.insert_text(detailed_absence_reason)

        # 요일 및 기간을 계산하는 함수 필요
        hwp.move_to_field(f"period{{{{{n}}}}}")

        date_info = extract_date_info(from_day, until_day)
        start_date = (
            date_info["year"]
            + "년 "
            + date_info["month"]
            + "월 "
            + date_info["day_from"]
            + "일 "
            + "["
            + date_info["weekday"]
            + "]"
        )
        end_date = (
            date_info["year"]
            + "년 "
            + date_info["month"]
            + "월 "
            + date_info["day_to"]
            + "일 "
            + "["
            + date_info["weekday"]
            + "]"
        )

        absence_period = "(" + date_info["for_day"] + "일간)"
        period_string = start_date + " - " + end_date + absence_period
        hwp.insert_text(period_string)

        # 요일 및 기간을 계산하는 함수 필요
        confirmed_date_string = (
            str(date_info["confirmed_date"].year)
            + "년 "
            + str(date_info["confirmed_date"].month)
            + "월 "
            + str(date_info["confirmed_date"].day)
            + "일"
        )
        hwp.move_to_field(f"confirmed_date_1{{{{{n}}}}}")
        hwp.insert_text(confirmed_date_string)
        hwp.move_to_field(f"confirmed_date_2{{{{{n}}}}}")
        hwp.insert_text(confirmed_date_string)

        # id, std_class, std_no, name, start_date, end_date, reason, detailed_reason
        hwp.move_to_field(f"class_and_std_num{{{{{n}}}}}")
        class_and_std_num = str(std_class) + " 반 " + str(std_no) + " 번"
        hwp.insert_text(class_and_std_num)

    convert_engWeekdays_to_korWeekdays(hwp)

    # 다른이름으로 저장
    hwp.save_as("./결석계 " + date_info["month"] + "월.hwp")


def convert_engWeekdays_to_korWeekdays(hwpObject):
    target_document = hwpObject
    weekdays_eng = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    weekdays_kor = [
        "월요일",
        "화요일",
        "수요일",
        "목요일",
        "금요일",
        "토요일",
        "일요일",
    ]
    for n in range(len(weekdays_eng)):
        target_document.find_replace_all(weekdays_eng[n], weekdays_kor[n])


def show_absence_frame(*args):
    main_frame.pack_forget()
    abs_frame.pack(fill="both", expand=True)
    display_absences()


def show_main_frame(*args):
    abs_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)


root = tk.Tk()
root.title("결석계 자동 생성기")
root.geometry("800x800")

# Create a style
style = ttk.Style(root)

# Set the theme with the theme_use method
style.theme_use("clam")  # put the theme name here, that you want to use

initialize_database()
students_df = convert_stdInfo_to_dataframe()


# 메인 화면
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

main_label = tk.Label(
    main_frame,
    text="메인 화면",
    font=("Arial", 20),
)
main_label.pack(pady=20)

teacher_name_label = tk.Label(
    main_frame, text="담임교사 성명: 없음", font=("Arial", 14)
)
teacher_name_label.pack(pady=20)

set_teacher_button = tk.Button(
    main_frame,
    text="담임교사 성명 등록 [F1]",
    font=("Arial", 14),
    command=set_teacher_name,
)
set_teacher_button.pack(pady=20)
root.bind("<F1>", set_teacher_name)

edit_teacher_button = tk.Button(
    main_frame,
    text="담임교사 성명 수정 [F2]",
    font=("Arial", 14),
    command=edit_teacher_name,
)
edit_teacher_button.pack(pady=20)
root.bind("<F2>", edit_teacher_name)

reset_button = tk.Button(
    main_frame,
    text="결석생 데이터 초기화 [F3]",
    font=("Arial", 14),
    command=reset_database,
)
reset_button.pack(pady=10)
root.bind("<F3>", reset_database)

register_button = tk.Button(
    main_frame, text="결석생 등록 [F4]", font=("Arial", 14), command=show_absence_frame
)
register_button.pack(pady=10)
root.bind("<F4>", show_absence_frame)

report_button = tk.Button(
    main_frame,
    text="결석계 생성 [F5]",
    font=("Arial", 14),
    command=generate_absence_report,
)
report_button.pack(pady=10)
root.bind("<F5>", generate_absence_report)

creator_banner = tk.Label(main_frame, text="Created by tubiky", font=("Arial", 10))
creator_banner.pack(fill="x", anchor="se", padx=10, pady=100)

# 결석생 등록 화면
abs_frame = tk.Frame(root)

abs_label = tk.Label(abs_frame, text="결석생 등록 화면", font=("Arial", 20))
abs_label.pack(pady=20)

# 학생 번호 입력
stdNo_label = tk.Label(abs_frame, text="번호:", font=("Arial", 14))
stdNo_label.pack(anchor="w", padx=10)
stdNo_entry = ttk.Entry(
    abs_frame,
)
stdNo_entry.pack(fill="x", ipadx=30, ipady=6, padx=10, pady=10)

# 결석 기간 입력
period_label = tk.Label(abs_frame, text="결석 기간 (시작일):", font=("Arial", 14))
period_label.pack(anchor="w", padx=10)

frame_start_date = tk.Frame(abs_frame)
frame_start_date.pack(fill="x", padx=10)

start_year_combobox = ttk.Combobox(
    frame_start_date, values=[str(y) for y in range(2024, 2050)], width=5, height=18
)
start_year_combobox.pack(side="left", pady=10)
start_year_combobox.set("연")

start_month_combobox = ttk.Combobox(
    frame_start_date, values=[f"{m:02}" for m in range(1, 13)], width=4, height=18
)
start_month_combobox.pack(side="left", padx=5, pady=10)
start_month_combobox.set("월")

start_day_combobox = ttk.Combobox(
    frame_start_date, values=[f"{d:02}" for d in range(1, 32)], width=4, height=18
)
start_day_combobox.pack(side="left", pady=10)
start_day_combobox.set("일")

period_end_label = tk.Label(abs_frame, text="결석 기간 (종료일):", font=("Arial", 14))
period_end_label.pack(anchor="w", padx=10)

frame_end_date = tk.Frame(abs_frame)
frame_end_date.pack(fill="x", padx=10)

end_year_combobox = ttk.Combobox(
    frame_end_date, values=[str(y) for y in range(2024, 2050)], width=5
)
end_year_combobox.pack(side="left", pady=10)
end_year_combobox.set("")

end_month_combobox = ttk.Combobox(
    frame_end_date, values=[f"{m:02}" for m in range(1, 13)], width=4
)
end_month_combobox.pack(side="left", padx=5, pady=10)
end_month_combobox.set("")

end_day_combobox = ttk.Combobox(
    frame_end_date, values=[f"{d:02}" for d in range(1, 32)], width=4
)
end_day_combobox.pack(side="left", pady=10)
end_day_combobox.set("")

# 결석 종류 선택
reason_label = tk.Label(abs_frame, text="결석 종류:", font=("Arial", 14))
reason_label.pack(anchor="w", padx=10)
reason_combobox = ttk.Combobox(abs_frame, values=["인정", "질병", "기타"])
reason_combobox.pack(fill="x", ipadx=30, ipady=6, padx=10, pady=10)

# 상세 사유 입력
detailed_reason_label = tk.Label(abs_frame, text="결석 사유:", font=("Arial", 14))
detailed_reason_label.pack(anchor="w", padx=10)
detailed_reason_entry = ttk.Entry(abs_frame)
detailed_reason_entry.pack(fill="x", ipadx=30, ipady=6, padx=10, pady=10)

# 저장 버튼
save_button = tk.Button(abs_frame, text="결석생 등록[Enter]", command=save_absence)
save_button.pack(pady=10)
root.bind("<Return>", save_absence)

# 데이터 표시
# id, std_class, std_no, name, start_date, end_date, reason, detailed_reason
tree = ttk.Treeview(
    abs_frame,
    columns=(
        "id",
        "std_class",
        "std_no",
        "name",
        "start_date",
        "end_date",
        "reason",
        "detailed_reason",
    ),
    show="headings",
)
tree.heading("id", text="ID")
tree.column("id", width=40, anchor="center")
tree.heading("std_class", text="반")
tree.column("std_class", width=40, anchor="center")
tree.heading("std_no", text="번호")
tree.column("std_no", width=40, anchor="center")
tree.heading("name", text="이름")
tree.column("name", width=40, anchor="center")
tree.heading("start_date", text="결석 시작일")
tree.column("start_date", width=50, anchor="center")
tree.heading("end_date", text="결석 종료일")
tree.column("end_date", width=50, anchor="center")
tree.heading("reason", text="결석 종류")
tree.column("reason", width=40, anchor="center")
tree.heading("detailed_reason", text="결석 사유", anchor="center")
tree.column("detailed_reason", width=50, anchor="center")
tree.pack(fill="both", expand=True, padx=10, pady=10)

# 삭제 버튼
delete_button = tk.Button(abs_frame, text="삭제[Ctrl+d]", command=delete_absence)
delete_button.pack(side="left", padx=10, pady=10)
root.bind("<Control-d>", delete_absence)
root.bind("<Control-D>", delete_absence)

# 수정 버튼
edit_button = tk.Button(abs_frame, text="수정[Ctrl+m]", command=edit_absence)
edit_button.pack(side="left", padx=10, pady=10)
root.bind("<Control-m>", edit_absence)
root.bind("<Control-M>", edit_absence)

# 돌아가기 버튼
back_button = tk.Button(abs_frame, text="돌아가기[Ctrl+b]", command=show_main_frame)
back_button.pack(side="right", padx=10, pady=10)
root.bind("<Control-b>", show_main_frame)
root.bind("<Control-B>", show_main_frame)

root.mainloop()
