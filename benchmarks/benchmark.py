"""
Замеры времени операций append и insert(0, value) и построение графиков.
Сравниваются собственный DynamicArray и встроенный list (Python).

Запуск из корня проекта:  python benchmarks/benchmark.py
Результаты: results/append_insert.png, results/timings.csv
"""

import os
import sys
import time

import matplotlib

# Неинтерактивный бэкенд – график сохраняется в файл
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from dynamic_array import DynamicArray

# Размеры, для которых замеряем время (слайд 12)
SIZES = [10_000, 100_000, 1_000_000]

# Каждое измерение повторяем несколько раз и берём среднее значение
REPEATS = 3

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")


def time_append(DS, n):
    """
    Замеряет время n добавлений в конец.
    Суммарно O(n) -> амортизированная O(1) на одну операцию.
    """
    ds = DS()
    start = time.perf_counter()
    for i in range(n):
        ds.append(i)
    return time.perf_counter() - start


def time_insert_front(DS, n):
    """
    Замеряет время ОДНОЙ вставки в начало массива из n элементов.
    Требует сдвига всех элементов -> O(n) на операцию.
    """
    ds = DS()
    for i in range(n):
        ds.append(i)
    start = time.perf_counter()
    ds.insert(0, -1)
    return time.perf_counter() - start


def average(func, DS, n, repeats=REPEATS):
    """Повторяет измерение repeats раз и возвращает среднее значение."""
    total = 0.0
    for _ in range(repeats):
        total += func(DS, n)
    return total / repeats


def run():
    structures = [("DynamicArray", DynamicArray), ("list (Python)", list)]

    # Словари вида {"DynamicArray": [t1, t2, t3], ...}
    append_times = {name: [] for name, _ in structures}
    insert_times = {name: [] for name, _ in structures}

    print("Запуск замеров. Это может занять до нескольких минут...\n")
    for n in SIZES:
        for name, DS in structures:
            t_app = average(time_append, DS, n)
            t_ins = average(time_insert_front, DS, n)
            append_times[name].append(t_app)
            insert_times[name].append(t_ins)
            print(f"n = {n:>9} | {name:<14} | append: {t_app:.6f} c | insert(0): {t_ins:.8f} c")
        print()

    os.makedirs(RESULTS_DIR, exist_ok=True)
    save_csv(append_times, insert_times)
    plot(append_times, insert_times)
    print_table(append_times, insert_times)


def save_csv(append_times, insert_times):
    """Сохраняет численные результаты в CSV для отчёта."""
    path = os.path.join(RESULTS_DIR, "timings.csv")
    with open(path, "w", encoding="utf-8") as f:
        f.write("operation,structure,n,time_sec\n")
        for op, data in (("append", append_times), ("insert_front", insert_times)):
            for name, times in data.items():
                for n, t in zip(SIZES, times):
                    f.write(f"{op},{name},{n},{t:.9f}\n")
    print(f"Данные сохранены: {path}")


def plot(append_times, insert_times):
    """Строит два графика в логарифмическом масштабе (как на слайде 13)."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for ax, data, title in (
        (axes[0], append_times, "append (в конец)"),
        (axes[1], insert_times, "insert(0, value) (в начало)"),
    ):
        for marker, (name, times) in zip(("o-", "s-"), data.items()):
            ax.plot(SIZES, times, marker, label=name)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("Количество элементов (n)")
        ax.set_ylabel("Время, с")
        ax.set_title(title)
        ax.legend()
        ax.grid(True, which="both", linestyle="--", alpha=0.4)

    fig.suptitle("Обе структуры показывают O(n) при вставке в начало")
    fig.tight_layout()

    path = os.path.join(RESULTS_DIR, "append_insert.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"График сохранён: {path}")


def print_table(append_times, insert_times):
    """Печатает итоговую таблицу с отношением времени DynamicArray / list."""
    print("\n=== Итоговая таблица ===")
    for op, data in (("append (весь цикл)", append_times), ("insert(0) (одна операция)", insert_times)):
        print(f"\n{op}")
        print(f"{'n':>9} | {'DynamicArray, с':>16} | {'list, с':>14} | {'во сколько раз медленнее':>25}")
        print("-" * 76)
        for i, n in enumerate(SIZES):
            own = data["DynamicArray"][i]
            builtin = data["list (Python)"][i]
            ratio = own / builtin if builtin else float("inf")
            print(f"{n:>9} | {own:>16.6f} | {builtin:>14.6f} | {ratio:>25.1f}")


if __name__ == "__main__":
    run()
