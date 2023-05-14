def classify_flower_color(flower_colors):
    color_classes = {
        '빨강': [],
        '파랑': [],
        '초록': [],
        '노랑': [],
        '흰색': []
    }

    for color in flower_colors:
        if '빨강' in color:
            color_classes['빨강'].append(color)
        elif '파랑' in color:
            color_classes['파랑'].append(color)
        elif '초록' in color:
            color_classes['초록'].append(color)
        elif '노랑' in color:
            color_classes['노랑'].append(color)
        elif '흰색' in color:
            color_classes['흰색'].append(color)
        else:
            # 다른 색상에 해당하는 경우 여기에 처리 로직을 추가할 수 있습니다.
            pass

    return color_classes

# 테스트를 위한 리스트
flowers = ['빨강장미', '파랑국화', '노랑튤립', '흰색카네이션', '초록장미', '보라꽃']

# 꽃 색상으로 분류
classified_colors = classify_flower_color(flowers)

# 분류 결과 출력
for color, flower_list in classified_colors.items():
    print(color + ':', flower_list)