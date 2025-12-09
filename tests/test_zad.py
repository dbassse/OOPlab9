# isort: skip_file
# fmt: off
import math
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from task_package.zad import (compute_control_value, compute_partial_sum,
                              compute_series_sum, compute_term, main)


# Тесты для функции compute_term
def test_compute_term_basic() -> None:
    """Тестирование базового вычисления члена ряда."""
    n, x = 1, math.pi
    expected = math.cos(n * x) / n
    result = compute_term((n, x))
    assert result == pytest.approx(expected)


def test_compute_term_multiple_cases() -> None:
    """Тестирование compute_term с разными входными данными."""
    test_cases = [
        (1, 0.0, 1.0),  # cos(0)/1 = 1
        (2, 0.0, 0.5),  # cos(0)/2 = 0.5
        (1, math.pi, -1.0),  # cos(π)/1 = -1
        (2, math.pi, 0.5),  # cos(2π)/2 = 1/2
    ]

    for n, x, expected in test_cases:
        result = compute_term((n, x))
        assert result == pytest.approx(expected, rel=1e-10)


def test_compute_term_type_check() -> None:
    """Проверка типов для функции compute_term."""
    # Тест проходит, если mypy не находит ошибок типов
    # В runtime проверяем, что функция возвращает float
    result = compute_term((1, math.pi))
    assert isinstance(result, float)


# Тесты для функции compute_partial_sum
def test_compute_partial_sum_single_term() -> None:
    """Тестирование частичной суммы с одним членом."""
    start, end, x = 1, 1, math.pi
    expected = math.cos(x) / 1
    result = compute_partial_sum((start, end, x))
    assert result == pytest.approx(expected)


def test_compute_partial_sum_range() -> None:
    """Тестирование частичной суммы с диапазоном членов."""
    start, end, x = 1, 3, 0.0
    # При x=0, cos(0)=1, поэтому сумма: 1/1 + 1/2 + 1/3
    expected = 1 / 1 + 1 / 2 + 1 / 3
    result = compute_partial_sum((start, end, x))
    assert result == pytest.approx(expected, rel=1e-10)


def test_compute_partial_sum_type_check() -> None:
    """Проверка типов для функции compute_partial_sum."""
    result = compute_partial_sum((1, 5, math.pi))
    assert isinstance(result, float)


# Тесты для функции compute_series_sum
def test_compute_series_sum_basic() -> None:
    """Базовое тестирование вычисления суммы ряда."""
    x = 0.0
    epsilon = 0.1  # Большая точность для быстрого теста

    # При x=0 ряд становится гармоническим, который расходится,
    # но мы ограничиваемся точностью epsilon
    result = compute_series_sum(x, epsilon)
    assert isinstance(result, float)
    # Проверяем, что результат конечен
    assert math.isfinite(result)


def test_compute_series_sum_pi() -> None:
    """Тестирование для x=π (основной случай)."""
    x = math.pi
    epsilon = 1e-3  # Умеренная точность для быстрого теста
    result = compute_series_sum(x, epsilon)

    # Для x=π ряд сходится к -ln(2)
    expected = -math.log(2)
    # Допускаем большую погрешность из-за небольшого epsilon
    assert result == pytest.approx(expected, abs=1e-2)


def test_compute_series_sum_custom_epsilon() -> None:
    """Тестирование с разными значениями epsilon."""
    x = math.pi / 2
    epsilon_values = [1e-1, 1e-3, 1e-5]

    for epsilon in epsilon_values:
        result = compute_series_sum(x, epsilon)
        assert isinstance(result, float)
        assert math.isfinite(result)


def test_compute_series_sum_negative_x() -> None:
    """Тестирование с отрицательным x."""
    x = -math.pi / 3
    epsilon = 1e-3
    result = compute_series_sum(x, epsilon)
    assert isinstance(result, float)
    assert math.isfinite(result)


def test_compute_series_sum_edge_cases() -> None:
    """Тестирование граничных случаев."""
    test_cases = [
        (0.0, 1e-5),  # x = 0
        (2 * math.pi, 1e-5),  # x = 2π
        (-2 * math.pi, 1e-5),  # x = -2π
        (math.pi / 4, 1e-5),  # x = π/4
    ]

    for x, epsilon in test_cases:
        result = compute_series_sum(x, epsilon)
        assert isinstance(result, float)
        assert math.isfinite(result)


def test_compute_series_sum_monotonic_convergence() -> None:
    """Проверка монотонной сходимости при уменьшении epsilon."""
    x = math.pi
    epsilons = [1e-1, 1e-2, 1e-3, 1e-4]
    results = []

    for epsilon in epsilons:
        result = compute_series_sum(x, epsilon)
        results.append(result)

    # Проверяем, что результаты стабилизируются
    # (разности между последовательными результатами уменьшаются)
    diffs = [abs(results[i] - results[i + 1]) for i in range(len(results) - 1)]
    # Последняя разность должна быть самой маленькой
    assert diffs[-1] <= diffs[0] or diffs[-1] < 1e-2


# Тесты для функции compute_control_value
def test_compute_control_value_pi() -> None:
    """Тестирование контрольного значения для x=π."""
    x = math.pi
    expected = -math.log(2 * math.sin(x / 2))
    result = compute_control_value(x)
    assert result == pytest.approx(expected, rel=1e-10)


def test_compute_control_value_positive() -> None:
    """Тестирование для x, где sin(x/2) > 0."""
    test_cases = [math.pi / 3, math.pi / 2, 2 * math.pi / 3]

    for x in test_cases:
        if 2 * math.sin(x / 2) > 0:
            expected = -math.log(2 * math.sin(x / 2))
            result = compute_control_value(x)
            assert result == pytest.approx(expected, rel=1e-10)
            assert math.isfinite(result)


def test_compute_control_value_type_check() -> None:
    """Проверка типов для функции compute_control_value."""
    result = compute_control_value(math.pi / 4)
    assert isinstance(result, float)

    # Для problem cases
    result_nan = compute_control_value(0.0)
    # Может быть NaN или inf
    assert not math.isfinite(result_nan) or math.isnan(result_nan)


# Тесты для функции main
def test_main_output(capsys: pytest.CaptureFixture[str]) -> None:
    """Тестирование вывода функции main."""
    main()
    captured = capsys.readouterr()
    output = captured.out

    # Проверяем, что вывод содержит ожидаемые строки
    assert "Вычисленная сумма ряда S:" in output
    assert "Контрольное значение y:" in output
    assert "Разница |S - y|:" in output
    assert "Точность достигнута" in output or "Точность не достигнута" in output


# Тесты на производительность и стабильность
def test_compute_series_sum_performance() -> None:
    """Тест производительности (должен выполняться быстро)."""
    import time

    x = math.pi
    epsilon = 1e-5

    start_time = time.time()
    result = compute_series_sum(x, epsilon)
    end_time = time.time()

    execution_time = end_time - start_time

    # Проверяем, что вычисление заняло разумное время (менее 5 секунд)
    assert execution_time < 5.0
    assert math.isfinite(result)


def test_compute_series_sum_parallelism() -> None:
    """Тестирование, что параллельные вычисления работают корректно."""
    x = math.pi
    epsilon = 1e-4

    # Запускаем несколько раз, чтобы убедиться в стабильности
    results = []
    for _ in range(3):
        result = compute_series_sum(x, epsilon)
        results.append(result)

    # Все результаты должны быть близки друг к другу
    for i in range(len(results) - 1):
        assert results[i] == pytest.approx(results[i + 1], rel=1e-10)


# Тесты на обработку исключений и edge cases
def test_compute_series_sum_very_small_epsilon() -> None:
    """Тестирование с очень маленьким epsilon."""
    x = math.pi
    epsilon = 1e-10  # Очень высокая точность
    result = compute_series_sum(x, epsilon)
    assert isinstance(result, float)
    # Проверяем, что не произошло переполнения или других ошибок
    assert math.isfinite(result)


def test_compute_series_sum_large_epsilon() -> None:
    """Тестирование с большим epsilon (быстрое вычисление)."""
    x = math.pi
    epsilon = 0.5  # Большая погрешность
    result = compute_series_sum(x, epsilon)
    assert isinstance(result, float)
    assert math.isfinite(result)


# Интеграционные тесты
def test_symmetry_property() -> None:
    """Тестирование свойства симметрии: S(-x) = S(x)."""
    x = math.pi / 3
    epsilon = 1e-5

    S_positive = compute_series_sum(x, epsilon)
    S_negative = compute_series_sum(-x, epsilon)

    # Из-за косинуса ряд должен быть четным: cos(-nx) = cos(nx)
    assert S_positive == pytest.approx(S_negative, rel=1e-10)


# Тесты на соответствие математическим свойствам
def test_series_known_values() -> None:
    """Тестирование известных значений ряда."""
    # При x = π/2 известное значение
    x = math.pi / 2
    epsilon = 1e-6
    S = compute_series_sum(x, epsilon)

    # Сравниваем с приближенным значением, вычисленным аналитически
    # Ряд при x=π/2: Σ cos(nπ/2)/n
    # Можно сравнить с несколькими членами
    manual_sum = 0
    for n in range(1, 1000):
        term = math.cos(n * x) / n
        if abs(term) < epsilon:
            break
        manual_sum += term

    assert S == pytest.approx(manual_sum, rel=1e-5)


# Тесты для проверки типизации mypy (косвенно)
def test_type_annotations() -> None:
    """Проверка, что функции имеют правильные аннотации типов."""
    # Если mypy проходит, эти проверки не нужны
    # Но мы можем проверить в runtime
    assert compute_term.__annotations__ != {}
    assert compute_partial_sum.__annotations__ != {}
    assert compute_series_sum.__annotations__ != {}
    assert compute_control_value.__annotations__ != {}


if __name__ == "__main__":
    # Запуск тестов напрямую, если нужно
    pytest.main([__file__, "-v"])
