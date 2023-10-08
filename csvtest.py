import csv

data = [
    ["문제번호", "문제", "선택지1", "선택지2", "선택지3", "선택지4", "정답"],
    [1, "다음 중 소수인 숫자는?", 10, 17, 25, 31, "b"],
    [2, "다음 식을 계산하시오: (6 + 4) × (8 - 2)", 24, 48, -24, -48, "a"],
    [3, "다음 등식에서 x의 값은?", "x + (15 - x)/3 = x + (x -5)/5", -5, -3, -1, "d"],
    [
        4,
        "직사각형 ABCD에서 AB = BC = CD = DA = x일 때 AC = y의 관계식은?",
        "y=2x",
        "y=4x",
        "y=x/2",
        "y=x/4",
        "c",
    ],
    # ... 나머지 문제들 추가
    [50, "다음 중 최대공약수(GCD)를 구하시오: 12와 18의 GCD는?", 6, 9, 12, "b"],
]

filename = "math_problems.csv"

with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)

print(f"CSV 파일 '{filename}'이 생성되었습니다.")
