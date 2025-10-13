import os
import pandas as pd
from datetime import date, datetime, timedelta


CURRENT_PATH = os.getcwd()

FONT_LARGE = ("Arial", 20)
FONT_NORMAL = ("Arial", 14)
FONT_SMALL = ("Arial", 12)


HWP_PATH = "./hwp_file_form/결석계.hwp"
EXCEL_PATH = "./excel_form/students.xlsx"


SICK = "인정 (   )   질병 ( O )   기타 (   )"
ADMITTED = "인정 ( O )   질병 (   )   기타 (   )"
ETC = "인정 (   )   질병 (   )   기타 ( O )"

WEEKDAYS_ENG = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
WEEKDAYS_KOR = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일",
]

HOLIDAYS = [
    "2025-08-15",
    "2025-10-03",
    "2025-10-05",
    "2025-10-06",
    "2025-10-07",
    "2025-10-08",
    "2025-10-09",
    "2025-10-10",
    "2025-11-13",
    "2025-12-25",
    "2026-01-01",
    "2026-01-28",
    "2026-01-29",
    "2026-01-30",
    "2026-03-01",
]

HOLIDAYS_DATE = [datetime.strptime(e, "%Y-%m-%d").date() for e in HOLIDAYS]
