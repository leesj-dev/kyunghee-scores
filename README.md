# kyunghee-scores
이 자료는 2023학년도 경희대학교 입학전형 내신 통계자료 PDF를 `pdfplumber`로 파싱하여 전체 학생의 내신에 대한 합/불 여부를 출력하는 코드입니다.
원본 PDF에서 추출한 O, X 좌표값들을 `tkinter` 패키지를 이용하여 원본과 '거의' 동일함을 검증하였으며, 추가 동일성 검증 및 좌표값을 .csv 형태로 저장하는 기능은 추후 보완 예정입니다.

* `2023학년도 경희대학교 입학전형 통계자료.pdf` : 원본 PDF
* `original.pdf`: 위 자료에서의 10번째 페이지만 따로 추출한 PDF
* `main.py` : 실행 코드
* `result.ps` : 실행 결과
* `result.pdf` : Adobe Illustrator에서 PostScript 파일(`result.ps`)을 PDF로 변환