def solve_part3():
    print("Часть 3. Двоичный счетчик вычитающего типа на 8 внутренних состояний (Т-триггеры)")
    print("-" * 50)
    print("Таблица истинности:")
    print("v q3* q2* q1* | q3 q2 q1 | h3 h2 h1")
    print("-" * 50)

    sdnf_h3, sdnf_h2, sdnf_h1 = [], [], []

    # Перебор всех комбинаций входа v и текущего состояния q
    for v in (0, 1):
        for q in range(8):
            q3_star, q2_star, q1_star = (q >> 2) & 1, (q >> 1) & 1, q & 1
            
            # Для вычитающего счетчика при v=1 считаем вниз
            q_next = q if v == 0 else (q - 1) % 8
            q3, q2, q1 = (q_next >> 2) & 1, (q_next >> 1) & 1, q_next & 1
            
            # Функция возбуждения Т-триггера (изменилось ли состояние)
            h3, h2, h1 = q3_star ^ q3, q2_star ^ q2, q1_star ^ q1

            print(f"{v}  {q3_star}   {q2_star}   {q1_star}  |  {q3}  {q2}  {q1}  |  {h3}  {h2}  {h1}")

            # Сборка СДНФ
            term = f"{'v' if v else '~v'}*{'q3' if q3_star else '~q3'}*{'q2' if q2_star else '~q2'}*{'q1' if q1_star else '~q1'}"
            if h3: sdnf_h3.append(term)
            if h2: sdnf_h2.append(term)
            if h1: sdnf_h1.append(term)

    print("-" * 50)
    print("СДНФ функций возбуждения:")
    print(f"h3 = {' + '.join(sdnf_h3)}")
    print(f"h2 = {' + '.join(sdnf_h2)}")
    print(f"h1 = {' + '.join(sdnf_h1)}")

    print("-" * 50)
    print("Минимизированные функции возбуждения:")
    print("h3 = ~q2 * ~q1 * v")
    print("h2 = ~q1 * v")
    print("h1 = v")

if __name__ == "__main__":
    solve_part3()