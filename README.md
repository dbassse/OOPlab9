# 🐍 Управление процессами в Python. 
![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)
![Type Checking](https://img.shields.io/badge/types-mypy-blue.svg)
![Testing](https://img.shields.io/badge/tests-pytest-green.svg)

## 👨‍💻 Автор

**Давид Даниелян**

---

📊 Проект для вычисления суммы бесконечного ряда с заданной точностью с использованием многопроцессности на Python.

## Описание

Вычисление суммы ряда:
$\[
S = \sum_{n=1}^{\infty} \frac{\cos nx}{n} = \cos x + \frac{\cos 2x}{2} + \ldots
\]$
с точностью \(\varepsilon = 10^{-7}\) и сравнение с контрольным значением функции:
$\[
y = -\ln\left(2\sin\frac{x}{2}\right)
\]$

### Требования
- Python 3.8+
- Зависимости: стандартная библиотека Python (multiprocessing, math, typing)



