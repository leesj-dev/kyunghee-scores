import os
import pdfplumber
from tkinter import *
from pprint import pprint
import math

app = Tk()
app.title("Lines")
app.geometry("1191x842")
width = 1190.55
height = 841.89
canvas = Canvas(app, width=width, height=height, bg="white")
canvas.pack()
path = os.path.join(os.path.dirname(__file__), "2023학년도 경희대학교 입학전형 통계자료.pdf")
x_dict = {}
y_set = set()

def round_partial (value, resolution):
    return round(round(value / resolution) * resolution, -math.floor(math.log(resolution, 10)))

with pdfplumber.open(path) as pdf:
    page = pdf.pages[9]
    obj = page.objects
    # width, height 확인용
    # print(page.width, page.height)

    # object 구조 파악용
    # with open("out.txt", "w") as fout:
        # pprint(obj, fout)

    # X 추출 및 그리기
    for item in obj["line"]:
        if item["stroking_color"] == (1, 0, 0):  # red color
            canvas.create_line(item["x0"], height - item["y0"], item["x1"], height - item["y1"], fill="red", width=0.3)
            canvas.create_line(item["x0"], height - item["y1"], item["x1"], height - item["y0"], fill="red", width=0.3)
            y_set.add(round_partial(height - (item["y0"] + item["y1"]) / 2, 0.005))

    # O 추출 및 그리기
    for item in obj["curve"]:
        if len(item["pts"]) == 3:
            y_round = round_partial(height - item["y0"], 0.005)
            """
            if item["x0"] in x_dict.keys():
                x_dict[item["x0"]].add(y_round)
            else:
                x_dict[item["x0"]] = {y_round}
            """
            if y_round in y_set:  # 완벽한 알고리즘이라고 할 수는 없음
                canvas.create_oval(item["x0"], height - item["y0"] - 2.8615, item["x1"], height - item["y1"] + 2.8615, outline="black", width=0.3)

print(sorted(y_set))

# x좌표 별 y좌표 결과 추출
"""
with open("out1.txt", "w") as fout:
    for k in sorted(x_dict.keys()):
        fout.write(f"{round(k, 2)}: {sorted(x_dict[k])}\n")
    # pprint(x_dict, fout)
"""

canvas.update()
canvas.postscript(file="result.ps")
app.mainloop()
