# Лабораторная работа № 1 — Реализация массива и основных операций с ним

Дисциплина «Алгоритмы и структуры данных».

Статический и динамический массивы, реализованные с нуля на `ctypes.py_object`,
линейный и бинарный поиск, замеры времени и графики.

## Структура проекта

```
dsa-lab-01/
├── src/
│   ├── static_array.py        🥉 Бронза: StaticArray (get, set, append, len, str)
│   ├── dynamic_array.py       🥈 Серебро: DynamicArray (append, get, insert,
│   │                              remove, find, binary_search, resize/shrink)
│   └── dynamic_array_gold.py  🥇 Золото: DynamicArrayGold + эксперимент
│                                 с коэффициентом роста
├── benchmarks/
│   └── benchmark.py           Замеры append и insert(0), графики
├── tests/
│   └── test_arrays.py         Тесты для самопроверки (assert)
├── results/                   Графики и CSV с результатами замеров
└── REPORT.md                  Отчёт: таблица сложности, замеры, анализ
```

## Требования

- Python 3.8+
- `matplotlib` (только для графиков)

```bash
pip install matplotlib
```

## Запуск

```bash
# Тесты для самопроверки
python tests/test_arrays.py

# Демонстрация работы (бронза / серебро)
python src/static_array.py
python src/dynamic_array.py

# Золото: сравнение коэффициентов роста 2.0 и 1.5 -> results/growth_factors.png
python src/dynamic_array_gold.py

# Замеры append и insert(0) -> results/append_insert.png, results/timings.csv
python benchmarks/benchmark.py
```

## Кратко о сложности

| Операция | Static Array | Dynamic Array | list (Python) |
|---|---|---|---|
| Доступ по индексу | O(1) | O(1) | O(1) |
| Вставка в конец | O(1)\* | O(1) амортиз. | O(1) амортиз. |
| Вставка / удаление в начале и середине | O(n) | O(n) | O(n) |
| Линейный поиск | O(n) | O(n) | O(n) |
| Бинарный поиск | O(log n) | O(log n) | O(log n) |

\* При наличии свободного места, иначе `OverflowError`.

Подробный разбор результатов и графики — в [REPORT.md](REPORT.md).
