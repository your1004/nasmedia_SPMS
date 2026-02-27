import openpyxl
print("Starting...")
try:
    wb = openpyxl.load_workbook(
        r'C:\Users\Administrator\Downloads\나스미디어 2024년 12월 취급고 현황_0116(f) (2).xlsx',
        data_only=True
    )
    print("Sheets:", wb.sheetnames)
except Exception as e:
    print("ERROR:", e)
