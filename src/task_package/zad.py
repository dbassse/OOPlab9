import math
from multiprocessing import Pool, cpu_count
from typing import List, Tuple


def compute_term(args: Tuple[int, float]) -> float:
    """Вычисляет отдельный член ряда."""
    n, x = args
    return math.cos(n * x) / n


def compute_partial_sum(start_end: Tuple[int, int, float]) -> float:
    """Вычисляет частичную сумму ряда для заданного диапазона."""
    start, end, x = start_end
    partial_sum = 0.0
    for n in range(start, end + 1):
        partial_sum += math.cos(n * x) / n
    return partial_sum


def compute_series_sum(x: float = math.pi, epsilon: float = 1e-7) -> float:
    """
    Вычисляет сумму ряда S = Σ(cos(n*x)/n) с точностью epsilon.

    Args:
        x: Значение аргумента
        epsilon: Точность вычисления

    Returns:
        Сумма ряда S
    """
    # Определяем максимальное количество членов ряда для достижения точности
    n = 1
    max_n = 0
    while True:
        term = abs(math.cos(n * x) / n)
        if term < epsilon:
            max_n = n
            break
        n += 1
        if n > 10000000:  # Защита от бесконечного цикла
            max_n = n
            break

    # Создаем диапазоны для параллельных вычислений
    num_processes = min(cpu_count(), 4)  # Используем до 4 процессов
    chunk_size = max_n // num_processes

    ranges: List[Tuple[int, int, float]] = []
    for i in range(num_processes):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size if i < num_processes - 1 else max_n
        ranges.append((start, end, x))

    # Параллельное вычисление частичных сумм
    with Pool(processes=num_processes) as pool:
        partial_sums: List[float] = pool.map(compute_partial_sum, ranges)

    # Суммируем все частичные суммы
    total_sum = sum(partial_sums)
    return total_sum


def compute_control_value(x: float = math.pi) -> float:
    """
    Вычисляет контрольное значение y.

    Args:
        x: Значение аргумента

    Returns:
        Контрольное значение y
    """
    if 2 * math.sin(x / 2) > 0:
        return -math.log(2 * math.sin(x / 2))
    else:
        # Для избежания ошибок при неположительных значениях логарифма
        return float("nan")


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
