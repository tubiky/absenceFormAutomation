pyinstaller -w main.py ^
  --add-data ".\excel_form\students.xlsx;excel_form" ^
  --add-data ".\hwp_file_form\form.hwp;hwp_file_form" ^
  --add-data ".\settings\constants.py;settings" ^
  --add-data ".\utility\*.*;utility" ^
  --add-data ".\*.*;." ^
