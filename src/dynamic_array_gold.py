"""
Модуль: dynamic_array_gold.py
Золотой уровень лабораторной работы №1.
Динамический массив с настраиваемым коэффициентом роста (growth factor)
и эксперимент по сравнению factor = 2.0 и factor = 1.5.
"""

import os
import time

import matplotlib

# Используем неинтерактивный бэкенд, чтобы график сохранялся в файл
# даже при запуске из терминала без графической оболочки
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Наследуемся от серебряного уровня – весь базовый функционал уже реализован там
from dynamic_array import DynamicArray

# Папка для сохранения графиков (путь не зависит от текущей директории запуска)
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")


class DynamicArrayGold(DynamicArray):
    """Золотой уровень – массив с настраиваемым коэффициентом роста."""

    # ------------------------------------------------------------------
    # КОНСТРУКТОР – добавляем к базовому массиву коэффициент роста
    # ------------------------------------------------------------------
    def __init__(self, growth_factor=2.0):
        """
        :param growth_factor: во сколько раз увеличивается ёмкость при расширении
                              2.0 – как в Python list / C++ std::vector
                              1.5 – "экономный" вариант (меньше пустой памяти)
        """
        # Вызываем конструктор родителя: _size = 0, _capacity = 1, _array создан
        super().__init__()

        # Сохраняем коэффициент роста как атрибут объекта
        self._growth_factor = growth_factor

    # ------------------------------------------------------------------
    # _resize – переопределяем: новая ёмкость считается по коэффициенту
    # ------------------------------------------------------------------
    def _resize(self, new_capacity=None):
        """
        Если ёмкость не указана явно – вычисляем её как _capacity * growth_factor.
        "+ 1" гарантирует рост даже при малых ёмкостях и дробных коэффициентах
        (например, int(1 * 1.5) = 1 – массив бы не вырос и append зациклился).
        """
        if new_capacity is None:
            new_capacity = int(self._capacity * self._growth_factor) + 1

        # Само копирование элементов делает родительский метод
        super()._resize(new_capacity)

    # ------------------------------------------------------------------
    # append – переопределяем, чтобы он использовал этот _resize
    # ------------------------------------------------------------------
    def append(self, value):
        """
        Добавляет элемент в конец. При заполнении расширяет массив
        в _growth_factor раз (а не строго в 2 раза, как в серебре).
        """
        if self._size == self._capacity:
            self._resize()   # без аргумента, использует коэффициент

        self._array[self._size] = value
        self._size += 1


# -------------------- ЭКСПЕРИМЕНТ --------------------
def compare_growth_factors():
    """
    Замеряет время заполнения массива для factor = 2.0 и factor = 1.5,
    строит график и печатает таблицу результатов.
    """
    sizes = [1000, 5000, 10000, 50000, 100000]
    times_2x = []
    times_1_5x = []

    print("Запуск эксперимента. Подождите...")
    for n in sizes:
        # factor 2.0
        arr2 = DynamicArrayGold(2.0)
        start = time.perf_counter()
        for i in range(n):
            arr2.append(i)
        times_2x.append(time.perf_counter() - start)

        # factor 1.5
        arr15 = DynamicArrayGold(1.5)
        start = time.perf_counter()
        for i in range(n):
            arr15.append(i)
        times_1_5x.append(time.perf_counter() - start)

    # График
    plt.figure(figsize=(10, 5))
    plt.plot(sizes, times_2x, 'o-', label='factor = 2.0')
    plt.plot(sizes, times_1_5x, 's-', label='factor = 1.5')
    plt.xlabel('Количество добавлений (n)')
    plt.ylabel('Время (сек)')
    plt.title('Сравнение коэффициентов роста')
    plt.legend()
    plt.grid(True)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    path = os.path.join(RESULTS_DIR, "growth_factors.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    print(f"График сохранён: {path}")

    # Вывод таблицы
    print("\n=== Результаты ===")
    print(f"{'n':>8} | {'factor 2.0':>12} | {'factor 1.5':>12} | {'разница, %':>10}")
    print("-" * 55)
    for i, n in enumerate(sizes):
        diff = (times_2x[i] - times_1_5x[i]) / times_1_5x[i] * 100
        print(f"{n:>8} | {times_2x[i]:>12.6f} | {times_1_5x[i]:>12.6f} | {diff:>10.2f}")

    return sizes, times_2x, times_1_5x


# -------------------- ЗАПУСК --------------------
if __name__ == "__main__":
    # Быстрая проверка
    arr = DynamicArrayGold(1.5)
    for i in range(10):
        arr.append(i)
    print("Массив:", arr)
    print("Размер:", len(arr), "Ёмкость:", arr._capacity)

    # Запуск эксперимента
    compare_growth_factors()
