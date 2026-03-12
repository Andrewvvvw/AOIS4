import sys
from src.models import BinaryNumber
from src.converters.to_binary import to_direct, to_reverse, to_additional
from src.converters.to_decimal import direct_to_decimal, additional_to_decimal, fixed_point_to_decimal
from src.arithmetic.addition import add_binary
from src.arithmetic.subtraction import negate
from src.arithmetic.multiplication import multiply_binary
from src.arithmetic.division import divide_binary
from src.ieee754.converters import float_to_ieee754, ieee754_to_float
from src.ieee754.addition_subtraction import add_ieee754, subtract_ieee754
from src.ieee754.multiplication import multiply_ieee754
from src.ieee754.division import divide_ieee754
from src.gray_bcd.converters import decimal_to_gray_bcd, gray_bcd_to_decimal
from src.gray_bcd.addition import add_gray_bcd
from src.config import BCD_DECAD_SIZE, MANTISSA_START

def format_bin(bn: BinaryNumber) -> str:
    return "".join(map(str, bn.bits))


def format_ieee(bn: BinaryNumber) -> str:
    b = format_bin(bn)
    return f"{b[0]} {b[1:MANTISSA_START]} {b[MANTISSA_START:]}"


def format_bcd(bn: BinaryNumber) -> str:
    b = format_bin(bn)
    return " ".join(b[i:i + BCD_DECAD_SIZE] for i in range(0, len(b), BCD_DECAD_SIZE))


def get_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: Введите целое число.")


def get_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: Введите число с плавающей точкой.")


def print_menu():
    print("1. Конвертация целого числа (Прямой, Обратный, Дополнительный)")
    print("2. Сложение в дополнительном коде")
    print("3. Вычитание в дополнительном коде")
    print("4. Умножение в прямом коде")
    print("5. Деление в прямом коде")
    print("6. Арифметика с плавающей точкой (IEEE-754-2008)")
    print("7. Сложение в двоично-десятичном коде (Gray BCD)")
    print("0. Выход")


def main():
    while True:
        print_menu()
        choice = input("Выберите операцию (0-7): ").strip()

        try:
            if choice == '0':
                print("Завершение работы.")
                sys.exit(0)

            elif choice == '1':
                val = get_int("Введите целое десятичное число: ")
                d = to_direct(val)
                r = to_reverse(val)
                a = to_additional(val)
                print(f"\nДесятичное:      {val}")
                print(f"Прямой код:      {format_bin(d)}")
                print(f"Обратный код:    {format_bin(r)}")
                print(f"Дополнительный:  {format_bin(a)}")
                print(f"Проверка (10):   {additional_to_decimal(a)}")

            elif choice == '2':
                v1 = get_int("Введите первое слагаемое: ")
                v2 = get_int("Введите второе слагаемое: ")
                a, b = to_additional(v1), to_additional(v2)
                res = add_binary(a, b)
                print(f"\n[{format_bin(a)}] ({v1})")
                print(f"+")
                print(f"[{format_bin(b)}] ({v2})\n")
                print(f"[{format_bin(res)}] -> {additional_to_decimal(res)} (10-й формат)")

            elif choice == '3':
                v1 = get_int("Введите уменьшаемое: ")
                v2 = get_int("Введите вычитаемое: ")
                a = to_additional(v1)
                b = to_additional(v2)

                neg_b = negate(b)
                res = add_binary(a, neg_b)

                print(f"\nУменьшаемое (A):      {format_bin(a)} ({v1})")
                print(f"Вычитаемое (B):       {format_bin(b)} ({v2})")
                print(f"Отрицание B (-B):     {format_bin(neg_b)} (Инверсия + 1)")
                print(f"Сложение A + (-B):    {format_bin(res)}")
                print(f"Результат (10):       {additional_to_decimal(res)}")

            elif choice == '4':
                v1 = get_int("Введите первый множитель: ")
                v2 = get_int("Введите второй множитель: ")
                a, b = to_direct(v1), to_direct(v2)
                res = multiply_binary(a, b)
                print(f"\nМножимое:      {format_bin(a)} ({v1})")
                print(f"Множитель:     {format_bin(b)} ({v2})")
                print(f"Произведение:  {format_bin(res)}")
                print(f"Результат(10): {direct_to_decimal(res)}")

            elif choice == '5':
                v1 = get_int("Введите делимое: ")
                v2 = get_int("Введите делитель: ")
                if v2 == 0:
                    print("Ошибка: Деление на ноль запрещено.")
                    continue
                a, b = to_direct(v1), to_direct(v2)
                res = divide_binary(a, b)
                print(f"\nДелимое:       {format_bin(a)} ({v1})")
                print(f"Делитель:      {format_bin(b)} ({v2})")
                print(f"Частное (bin): {format_bin(res)} ")
                print(f"Результат(10): {fixed_point_to_decimal(res)}")

            elif choice == '6':
                f1 = get_float("Введите первое число (float): ")
                f2 = get_float("Введите второе число (float): ")
                a = float_to_ieee754(f1)
                b = float_to_ieee754(f2)

                print("\nФормат: [Знак] [Экспонента (8 бит)] [Мантисса (23 бита)]")
                print(f"A: {format_ieee(a)} ({ieee754_to_float(a)})")
                print(f"B: {format_ieee(b)} ({ieee754_to_float(b)})")

                op = input("Выберите операцию (+, -, *, /): ").strip()
                if op == '+':
                    res = add_ieee754(a, b)
                elif op == '-':
                    res = subtract_ieee754(a, b)
                elif op == '*':
                    res = multiply_ieee754(a, b)
                elif op == '/':
                    if f2 == 0.0:
                        print("Ошибка: Деление на ноль в IEEE-754.")
                        continue
                    res = divide_ieee754(a, b)
                else:
                    print("Неизвестная операция.")
                    continue

                print(f"\nРезультат(IEEE): {format_ieee(res)}")
                print(f"Результат(10):   {ieee754_to_float(res)}")

            elif choice == '7':
                v1 = get_int("Введите первое неотрицательное число (макс 8 цифр): ")
                v2 = get_int("Введите второе неотрицательное число (макс 8 цифр): ")
                if v1 < 0 or v2 < 0:
                    print(
                        "Внимание:"
                        " Gray BCD работает только с беззнаковыми числами."
                    )
                    continue

                a = decimal_to_gray_bcd(v1)
                b = decimal_to_gray_bcd(v2)
                res = add_gray_bcd(a, b)

                print(f"\nGray BCD (A):  {format_bcd(a)} ({v1})")
                print(f"Gray BCD (B):  {format_bcd(b)} ({v2})")
                print(f"Сумма (BCD):   {format_bcd(res)}")
                print(f"Результат(10): {gray_bcd_to_decimal(res)}")

            else:
                print("Неверный выбор. Введите число от 0 до 7.")

        except Exception as e:
            print(f"\n[КРИТИЧЕСКАЯ ОШИБКА]: {str(e)}")


if __name__ == "__main__":
    main()
