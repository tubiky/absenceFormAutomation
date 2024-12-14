import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
import sqlite3
import pandas as pd

# 데이터베이스 초기화
def initialize_database():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS absences (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        start_date TEXT NOT NULL,
                        end_date TEXT NOT NULL,
                        reason TEXT NOT NULL,
                        detailed_reason TEXT)''')
    conn.commit()
    conn.close()

# 담임교사 성명 설정
teacher_name = ""
def set_teacher_name():
    global teacher_name, teacher_name_label
    name = simpledialog.askstring("담임교사 성명 등록", "담임교사 성명을 입력해주세요:")
    if name:
        teacher_name = name
        teacher_name_label.config(text=f"담임교사 성명: {teacher_name}")

def edit_teacher_name():
    set_teacher_name()

# 데이터 초기화 함수
def reset_database():
    if messagebox.askyesno("데이터 초기화", "정말로 모든 데이터를 초기화하시겠습니까?"):
        conn = sqlite3.connect("attendance.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM absences")
        conn.commit()
        conn.close()
        display_absences()
        messagebox.showinfo("초기화 완료", "모든 데이터가 초기화되었습니다.")

# 결석 데이터 저장
def save_absence():
    name = name_entry.get()
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
    cursor.execute("INSERT INTO absences (name, start_date, end_date, reason, detailed_reason) VALUES (?, ?, ?, ?, ?)", (name, start_date, end_date, reason, detailed_reason))
    conn.commit()
    conn.close()

    display_absences()
    name_entry.delete(0, tk.END)
    start_year_combobox.set("")
    start_month_combobox.set("")
    start_day_combobox.set("")
    end_year_combobox.set("")
    end_month_combobox.set("")
    end_day_combobox.set("")
    reason_combobox.set("")
    detailed_reason_entry.delete(0, tk.END)

# 저장된 데이터 표시
def display_absences():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, start_date, end_date, reason, detailed_reason FROM absences")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row, iid=row[0])

def delete_absence():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("선택 오류", "삭제할 항목을 선택해주세요.")
        return

    for item in selected_item:
        conn = sqlite3.connect("attendance.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM absences WHERE id = ?", (tree.item(item)['values'][0],))
        conn.commit()
        conn.close()
        tree.delete(item)

def edit_absence():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("선택 오류", "수정할 항목을 선택해주세요.")
        return

    item_id = selected_item[0]
    values = tree.item(item_id)['values']

    name_entry.delete(0, tk.END)
    name_entry.insert(0, values[1])

    start_year, start_month, start_day = values[2].split("-")
    start_year_combobox.set(start_year)
    start_month_combobox.set(start_month)
    start_day_combobox.set(start_day)

    end_year, end_month, end_day = values[3].split("-")
    end_year_combobox.set(end_year)
    end_month_combobox.set(end_month)
    end_day_combobox.set(end_day)

    reason_combobox.set(values[4])
    detailed_reason_entry.delete(0, tk.END)
    detailed_reason_entry.insert(0, values[5])

    def update_absence():
        name = name_entry.get()
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
        cursor.execute("UPDATE absences SET name = ?, start_date = ?, end_date = ?, reason = ?, detailed_reason = ? WHERE id = ?", (name, start_date, end_date, reason, detailed_reason, values[0]))
        conn.commit()
        conn.close()

        display_absences()
        update_button.destroy()

    update_button = tk.Button(abs_frame, text="업데이트", command=update_absence)
    update_button.pack(pady=10)

def generate_absence_report():
    conn = sqlite3.connect("attendance.db")
    query = "SELECT id, name, start_date, end_date, reason, detailed_reason FROM absences"
    df = pd.read_sql_query(query, conn)
    conn.close()
    print(df)

def show_absence_frame():
    main_frame.pack_forget()
    abs_frame.pack(fill="both", expand=True)
    display_absences()

def show_main_frame():
    abs_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

root = tk.Tk()
root.title("화면 전환 예제")
root.geometry("900x600")

initialize_database()

# 메인 화면
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

main_label = tk.Label(main_frame, text="메인 화면", font=("Arial", 16))
main_label.pack(pady=20)

teacher_name_label = tk.Label(main_frame, text="담임교사 성명: 없음", font=("Arial", 12))
teacher_name_label.pack(pady=5)

set_teacher_button = tk.Button(main_frame, text="담임교사 성명 등록", command=set_teacher_name)
set_teacher_button.pack(pady=5)

edit_teacher_button = tk.Button(main_frame, text="담임교사 성명 수정", command=edit_teacher_name)
edit_teacher_button.pack(pady=5)

reset_button = tk.Button(main_frame, text="결석생 데이터 초기화", command=reset_database)
reset_button.pack(pady=10)

register_button = tk.Button(main_frame, text="결석생 등록", command=show_absence_frame)
register_button.pack(pady=10)

report_button = tk.Button(main_frame, text="결석계 생성", command=generate_absence_report)
report_button.pack(pady=10)

# 결석생 등록 화면
abs_frame = tk.Frame(root)

abs_label = tk.Label(abs_frame, text="결석생 등록 화면", font=("Arial", 16))
abs_label.pack(pady=20)

# 이름 입력
name_label = tk.Label(abs_frame, text="이름:")
name_label.pack(anchor="w", padx=10)
name_entry = tk.Entry(abs_frame)
name_entry.pack(fill="x", padx=10)

# 결석 기간 입력
period_label = tk.Label(abs_frame, text="결석 기간 (시작일):")
period_label.pack(anchor="w", padx=10)

frame_start_date = tk.Frame(abs_frame)
frame_start_date.pack(fill="x", padx=10)

start_year_combobox = ttk.Combobox(frame_start_date, values=[str(y) for y in range(2000, 2031)], width=5)
start_year_combobox.pack(side="left")
start_year_combobox.set("연")

start_month_combobox = ttk.Combobox(frame_start_date, values=[f"{m:02}" for m in range(1, 13)], width=3)
start_month_combobox.pack(side="left", padx=5)
start_month_combobox.set("월")

start_day_combobox = ttk.Combobox(frame_start_date, values=[f"{d:02}" for d in range(1, 32)], width=3)
start_day_combobox.pack(side="left")
start_day_combobox.set("일")

period_end_label = tk.Label(abs_frame, text="결석 기간 (종료일):")
period_end_label.pack(anchor="w", padx=10)

frame_end_date = tk.Frame(abs_frame)
frame_end_date.pack(fill="x", padx=10)

end_year_combobox = ttk.Combobox(frame_end_date, values=[str(y) for y in range(2000, 2031)], width=5)
end_year_combobox.pack(side="left")
end_year_combobox.set("")

end_month_combobox = ttk.Combobox(frame_end_date, values=[f"{m:02}" for m in range(1, 13)], width=3)
end_month_combobox.pack(side="left", padx=5)
end_month_combobox.set("")

end_day_combobox = ttk.Combobox(frame_end_date, values=[f"{d:02}" for d in range(1, 32)], width=3)
end_day_combobox.pack(side="left")
end_day_combobox.set("")

# 결석 종류 선택
reason_label = tk.Label(abs_frame, text="결석 종류:")
reason_label.pack(anchor="w", padx=10)
reason_combobox = ttk.Combobox(abs_frame, values=["인정", "질병", "기타"])
reason_combobox.pack(fill="x", padx=10)

# 상세 사유 입력
detailed_reason_label = tk.Label(abs_frame, text="결석 사유:")
detailed_reason_label.pack(anchor="w", padx=10)
detailed_reason_entry = tk.Entry(abs_frame)
detailed_reason_entry.pack(fill="x", padx=10)

# 저장 버튼
save_button = tk.Button(abs_frame, text="결석생 등록", command=save_absence)
save_button.pack(pady=10)

# 데이터 표시
tree = ttk.Treeview(abs_frame, columns=("id", "name", "start_date", "end_date", "reason", "detailed_reason"), show="headings")
tree.heading("id", text="ID")
tree.heading("name", text="이름")
tree.heading("start_date", text="결석 시작일")
tree.heading("end_date", text="결석 종료일")
tree.heading("reason", text="결석 종류")
tree.heading("detailed_reason", text="결석 사유")
tree.column("id", width=50)
tree.pack(fill="both", expand=True, padx=10, pady=10)

# 삭제 버튼
delete_button = tk.Button(abs_frame, text="삭제", command=delete_absence)
delete_button.pack(side="left", padx=10, pady=10)

# 수정 버튼
edit_button = tk.Button(abs_frame, text="수정", command=edit_absence)
edit_button.pack(side="left", padx=10, pady=10)

# 돌아가기 버튼
back_button = tk.Button(abs_frame, text="돌아가기", command=show_main_frame)
back_button.pack(side="right", padx=10, pady=10)

root.mainloop()
