# kyunghee-scores
2023학년도 경희대학교 입학전형 내신 통계자료 PDF를 `pdfplumber`로 파싱하여 전체 학생의 내신에 대한 합/불 여부를 출력합니다.
현재 개발 중이며, 구현된 기능 및 구현 예정 기능은 다음과 같습니다.
- [x] 원본 PDF에서 합/불 좌표값 추출
- [x] `tkinter` 패키지를 이용하여 그림을 재생성하여 원본과의 동일성 검증 (완벽히 증명되진 않음)
- [x] 스프레드시트에 합/불 좌표값 저장
- [ ] 학과명 추출 및 스프레드시트에 저장
- [ ] 합격자 평균 등급으로 평균 내신 동일성 검증
- [ ] 총 합격자 수 (모집 인원 + 충원 인원)이 O 개수와 일치하는지 검증

## 파일 설명
* `2023학년도 경희대학교 입학전형 통계자료.pdf` : 원본 PDF
* `original.pdf`: 위 자료에서의 10번째 페이지만 따로 추출한 PDF
* `main.py` : 실행 코드
* `graph.ps` : 실행 결과
* `graph.pdf` : Adobe Illustrator에서 PostScript 파일(`graph.ps`)을 PDF로 변환

## 좌표 → 내신 변환 방법
온도계 보정 식 $T = \dfrac{T_{b}(t - t_0)}{t_{100} - t_0}$과 동일한 원리를 사용하였습니다.
존재할 수 있는 최고 내신 1.00에 대응하는 x좌표 값을 $B_H$, 최저 내신 9.00에 대응하는 y좌표 값을 $B_L$, 우리가 내신을 구하고 싶어하는 한 자료의 좌표를 $B_x$라고 두면, $B_x$의 내신 $x$는 $\dfrac{B_L - B_x}{B_L - B_H} = \dfrac{9.00 - x}{9.00 - 1.00}$의 비례관계를 통해 구할 수 있습니다. 정리하면 $x=9-8\times\dfrac{B_L-B_x}{B_L-B_H}$이고, 이를 코드로 나타내면
```python
def calc_score (x):
    return 9 - round(8 * (BOUND_LOW - x) / (BOUND_LOW - BOUND_HIGH), 2)
```
입니다.

## 해결해야 하는 이슈
1. PDF을 파싱하다 보면 오브젝트들의 좌표값들이 정확하게 일관적 규칙을 가지고 배치되어 있지 않고 < 0.03pt의 오차를 가지고 있는 것을 확인할 수 있습니다. 이러한 오차 때문에 threshold 설정이 상당히 중요하고, PDF의 각 페이지마다 알맞는 threshold가 다르기에 단순히 round 처리를 통해 바운더리를 나누는 것이 아니라 K-means clustering 등의 알고리즘을 적용해야 할 필요성을 느끼고 있습니다.

2. X자의 경우 `pdfplumber`로 완벽하게 파싱에 성공하였으나 O표의 경우 약간의 문제가 있습니다. 가장 윗줄을 $1$번째 줄, 가장 아랫줄을 $m$번째 줄이라 하면, 원본 PDF에서 $n$번째 줄에 존재하던 O표는 파싱한 결과를 `tkinter`로 나타낸 결과(이하 변형본)의 $n$번째 줄에도 존재하지만 그 O표 위로 $(n - 1)$개, 그 아래로 $(m - n)$개 존재하며, 그 O표들 사이에 간격은 *이슈 1*에서도 지적하였듯이 일정하지 않습니다. 일단 이것을 해결한 방법은 바로 '원본과 변형본에 동시에 존재하는 O표는 변형본에서 제대로 된 위치에 있다'는 원리를 바탕으로 '원본에 있는 X표의 y좌표로부터 *허용 가능한 오차범위* 내에 있는 O표만 남겨두는' 방식을 택하였습니다. (*이슈 1*에서 설명하였듯이 정확하게 y좌표가 같다는 보장이 없습니다.) 문제는 '변형본에만 존재하는 O는 $n$번째 줄이 아닌 줄의 정위치에 존재하지 않는다는 보장은 없다'는 데에 있기에, 이러한 방법의 무결성을 검증하지 못하였습니다.