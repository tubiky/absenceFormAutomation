from settings.constants import *
from utility import utils
from pyhwpx import Hwp


class ReportManager:
    def __init__(self, df):
        self.df = df
        self.document = Hwp(new=False, visible=True)

    def open(self):
        self.document.Open(CURRENT_PATH + "/hwp_file_form/결석계.hwp")
        self.document.MoveDocEnd()
        self.document.CopyPage()

    def makeCopies(self):
        # 결석생 데이터 만큼 결석계표 복사하기
        num_of_copies = len(self.df) - 1

        for _ in range(num_of_copies):
            self.document.Paste()

    def fill_in_absence_info(self):
        num_of_copies = len(self.df)

        # df를 학번 또는 이름순 정렬 > 결석 시작일 기준 오름차순 정렬 > 인덱스 재설정 과정 추가하기
        self.df = self.df.sort_values(
            by=["std_no", "start_date"], ascending=[True, True], ignore_index=True
        )

        # 반복문을 활용하여 각 결석계의 양식에 데이터 입력하기
        for n in range(num_of_copies):
            # id, std_class, std_no, name, start_date, end_date, abs_type, reason
            std_class = self.df.iloc[n]["std_class"]
            std_no = self.df.iloc[n]["std_no"]
            student_name = self.df.iloc[n]["name"]
            from_day = self.df.iloc[n]["start_date"]
            until_day = self.df.iloc[n]["end_date"]
            absence_type = self.df.iloc[n]["abs_type"]
            detailed_absence_reason = self.df.iloc[n]["reason"]

            # 텍스트를 입력하는 함수를 만들어서 대체할 수 있을것 같다.
            # 함수에 필요한 인자는 입력 위치, 입력할 내용 이렇게 2가지
            # 담임 교사 이름 입력
            self.document.move_to_field(f"teacher_name_1{{{{{n}}}}}")
            self.document.insert_text(" ".join(utils.teacher_name))
            self.document.move_to_field(f"teacher_name_2{{{{{n}}}}}")
            self.document.insert_text(" ".join(utils.teacher_name))

            # 학생 이름 입력
            self.document.move_to_field(f"name{{{{{n}}}}}")
            self.document.insert_text(" ".join(student_name))

            # 결석 종류 입력
            self.document.move_to_field(f"absence_type{{{{{n}}}}}")
            if absence_type == "질병":
                self.document.insert_text(SICK)
            elif absence_type == "인정":
                self.document.insert_text(ADMITTED)
            elif absence_type == "기타":
                self.document.insert_text(ETC)
            else:
                pass

            # 상세 결석 사유 입력
            self.document.move_to_field(f"detailed_reason{{{{{n}}}}}")
            self.document.insert_text(detailed_absence_reason)

            # 요일 및 기간을 계산하는 함수 필요
            self.document.move_to_field(f"period{{{{{n}}}}}")

            date_info = utils.extract_date_info(from_day, until_day)
            start_date = (
                date_info["year"]
                + "년 "
                + date_info["month"]
                + "월 "
                + date_info["day_from"]
                + "일 "
                + "["
                + date_info["from_weekday"]
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
                + date_info["to_weekday"]
                + "]"
            )

            absence_period = "(" + date_info["for_day"] + "일간)"
            period_string = start_date + " - " + end_date + absence_period
            self.document.insert_text(period_string)

            confirmed_date_string = (
                str(date_info["confirmed_date"].year)
                + "년 "
                + str(date_info["confirmed_date"].month)
                + "월 "
                + str(date_info["confirmed_date"].day)
                + "일"
            )
            self.document.move_to_field(f"confirmed_date_1{{{{{n}}}}}")
            self.document.insert_text(confirmed_date_string)
            self.document.move_to_field(f"confirmed_date_2{{{{{n}}}}}")
            self.document.insert_text(confirmed_date_string)

            # id, std_class, std_no, name, start_date, end_date, reason, detailed_reason
            self.document.move_to_field(f"class_and_std_num{{{{{n}}}}}")
            class_and_std_num = str(std_class) + " 반 " + str(std_no) + " 번"
            self.document.insert_text(class_and_std_num)

        utils.convert_engWeekdays_to_korWeekdays(self.document)

        # 다른이름으로 저장
        self.document.save_as("./결석계 " + date_info["month"] + "월.hwp")
