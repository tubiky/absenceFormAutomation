pyinstaller -w main.py ^
  --add-data ".\excel_form\*.*;excel_form" ^
  --add-data ".\hwp_file_form\*.*;hwp_file_form" ^
  --add-data ".\settings\*.*;settings" ^
  --add-data ".\utility\*.*;utility" ^
  --add-data ".\*.*;." ^
