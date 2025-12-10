import math
from task_package.zad import compute_series_sum,compute_control_value

def main() -> None:
    """Основная функция для вычисления и сравнения результатов."""
    x = math.pi
    epsilon = 1e-7

    # Вычисляем сумму ряда
    S = compute_series_sum(x, epsilon)

    # Вычисляем контрольное значение
    y = compute_control_value(x)

    # Выводим результаты
    print(f"Вычисленная сумма ряда S: {S:.10f}")
    print(f"Контрольное значение y: {y:.10f}")
    print(f"Разница |S - y|: {abs(S - y):.10e}")

    # Проверяем точность
    if abs(S - y) < epsilon:
        print(f"Точность достигнута: разница меньше {epsilon}")
    else:
        print(f"Точность не достигнута: разница больше {epsilon}")


if __name__ == "__main__":
    main()
