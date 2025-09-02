import pandas as pd
from datetime import date, datetime, timedelta
from tkinter import messagebox
from settings.constants import *


teacher_name = ""


def load_students_data(path):
    # 엑셀의 학생 정보 불러오기
    df = pd.read_excel(path)

    return df


STUDENTS_DF = load_students_data(EXCEL_PATH)


def find_student(idx: int) -> dict:
    std_info = {}

    if idx not in STUDENTS_DF["번호"].values.tolist():
        messagebox.showerror("학생 조회 실패", "입력한 번호의 학생 정보가 없습니다.")
        return

    else:
        num_filter = STUDENTS_DF["번호"] == idx
        std_name, std_class = (
            STUDENTS_DF[num_filter]["이름"].iloc[0],
            STUDENTS_DF[num_filter]["반"].iloc[0],
        )

        std_info["name"] = std_name
        std_info["class"] = std_class
        std_info["no"] = idx

    return std_info


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


def extract_date_info(from_date, to_date):
    period_information = {}

    period_information["year"] = str(from_date.year)
    period_information["month"] = str(from_date.month)
    period_information["day_from"] = str(from_date.day)
    period_information["day_to"] = str(to_date.day)

    # 결석 기간: 현재는 단순 빼기 > 개선: 토요일, 일요일은 제외, const에 포함된 휴업일 제외
    period_information["for_day"] = count_absent_days(from_date, to_date)

    # 결석 시작일 요일
    period_information["from_weekday"] = str(from_date.strftime("%a"))
    # 결석 종료일 요일
    period_information["to_weekday"] = str(to_date.strftime("%a"))
    period_information["confirmed_date"] = (
        to_date + pd.Timedelta(days=3) if to_date.strftime("%a") == "Fri" else to_date
    )

    return period_information


# 실제 결석일수 계산 함수
def count_absent_days(from_date, to_date):
    cnt = 0
    start = from_date.date()
    end = to_date.date()

    if start > end:  # 이후의 날짜일 수록 크다고 판단
        start, end = end, start

    while start <= end:
        if start.weekday() < 5 and start not in HOLIDAYS_DATE:  # 0~4 = 월~금
            cnt += 1
        start += timedelta(days=1)

    return str(cnt)
