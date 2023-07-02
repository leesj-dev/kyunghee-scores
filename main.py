import os
import pdfplumber
from tkinter import *
import xlwings
import math

PDF_PATH = os.path.join(os.path.dirname(__file__), "2023학년도 경희대학교 입학전형 통계자료.pdf")
EXCEL_PATH = os.path.join(os.path.dirname(__file__), "result.xlsx")
BOUND_HIGH = 807.64  # p.10에 내신 1.0 나옴
BOUND_LOW = 1128.08  # p.18에 내신 9.0 나옴
RESOLUTION = 0.01

app = Tk()
app.title("Lines")
app.geometry("1191x842")
width = 1190.55
height = 841.89
canvas = Canvas(app, width=width, height=height, bg="white")
canvas.pack()
passed, failed = {}, {}
x_dict = {}

# 0.02 단위로 이산화 (오차 보정, 인접 값 중복 방지)
def round_partial (value, resolution):
    return round(round(value / resolution) * resolution, -math.floor(math.log(resolution, 10)))

def calc_score (x):
    return 9 - round(8 * (BOUND_LOW - x) / (BOUND_LOW - BOUND_HIGH), 2)  # 온도계 보정과 같은 원리

with pdfplumber.open(PDF_PATH) as pdf:
    page = pdf.pages[9]
    obj = page.objects
    # width, height 확인용
    "print(page.width, page.height)"

    # object 구조 파악용
    """
    with open("out.txt", "w") as fout:
        pprint(obj, fout)
    """

    # X 추출 및 그리기
    for item in obj["line"]:
        if item["stroking_color"] == (1, 0, 0):  # red color
            x_round = calc_score(round_partial((item["x0"] + item["x1"]) / 2, RESOLUTION))
            y_round = round_partial(height - (item["y0"] + item["y1"]) / 2, RESOLUTION)
            if y_round in failed.keys():
                failed[y_round].append(x_round)
            else:
                failed[y_round] = [x_round]
            """
            if x_round in x_dict.keys():
                x_dict[x_round].add(y_round)
            else:
                x_dict[x_round] = {y_round}
            """
            canvas.create_line(item["x0"], height - item["y0"], item["x1"], height - item["y1"], fill="red", width=0.3)
            canvas.create_line(item["x0"], height - item["y1"], item["x1"], height - item["y0"], fill="red", width=0.3)

    # O 추출 및 그리기
    for item in obj["curve"]:
        if len(item["pts"]) == 3:
            x_round = calc_score(round_partial((item["x0"] + item["x1"]) / 2, RESOLUTION))
            y_round = round_partial(height - item["y0"], RESOLUTION)
            if y_round in failed.keys():  # 올바르게 이루어진 X 추출의 y좌표와 일치한다면 (완벽한 알고리즘은 아님)
                if y_round in passed.keys():
                    passed[y_round].append(x_round)
                else:
                    passed[y_round] = [x_round]

                canvas.create_oval(item["x0"], height - item["y0"] - 2.8615, item["x1"], height - item["y1"] + 2.8615, outline="black", width=0.3)

print(sorted(passed.keys()))
print(sorted(failed.keys()))

"""
with open("out2.txt", "w") as fout:
    for k in sorted(x_dict.keys()):
        fout.write(f"{round(k, 2)}: {sorted(x_dict[k])}\n")
"""
# 결과 추출
result = {}
all_y = set(passed.keys()) | set(failed.keys())
for item in all_y:
    result[item] = [sorted(passed[item]), sorted(failed[item])]

# 엑셀에 저장
ws = xlwings.Book(EXCEL_PATH).sheets("Sheet1")
i = 1
for k in sorted(result.keys()):
    ws.range((1, i)).value = k
    ws.range((1, i), (1, i+1)).merge()
    ws.range((2, i)).value = ["O", "X"]
    ws.range((3, i)).options(transpose=True).value = result[k][0]
    ws.range((3, i+1)).options(transpose=True).value = result[k][1]
    i += 2

ws.used_range.number_format = "0.00"

canvas.update()
canvas.postscript(file="result.ps")
# app.mainloop()
