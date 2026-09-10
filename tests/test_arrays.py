"""
Тесты для самопроверки (assert-тесты из раздаточных материалов).
Запуск из корня проекта:  python tests/test_arrays.py
"""

import os
import sys

# Добавляем папку src в пути поиска модулей, чтобы импорты работали
# при запуске файла из корня проекта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from static_array import StaticArray
from dynamic_array import DynamicArray
from dynamic_array_gold import DynamicArrayGold


def test_static_array():
    """Бронза: get, set, append, len, str + обработка ошибок."""
    arr = StaticArray(5)
    assert len(arr) == 0

    for i in range(5):
        arr.append(i * 10)
    assert len(arr) == 5
    assert arr.get(2) == 20
    assert str(arr) == "[0, 10, 20, 30, 40]"

    arr.set(2, 999)
    assert arr.get(2) == 999

    # Выход за границы
    try:
        arr.get(10)
        assert False, "ожидался IndexError"
    except IndexError:
        pass

    # Переполнение
    try:
        arr.append(100)
        assert False, "ожидался OverflowError"
    except OverflowError:
        pass

    # Некорректная ёмкость
    try:
        StaticArray(0)
        assert False, "ожидался ValueError"
    except ValueError:
        pass

    print("StaticArray: тесты пройдены")


def test_dynamic_array():
    """Серебро: тест из раздаточных материалов."""
    da = DynamicArray()
    for i in range(100):
        da.append(i)
    assert len(da) == 100
    assert da.get(50) == 50
    da.insert(10, 999)
    assert da.get(10) == 999
    da.remove(10)
    assert da.get(10) == 10
    assert da.find(50) == 50
    # Для бинарного поиска массив отсортирован
    assert da.binary_search(50) == 50
    print("DynamicArray: тесты пройдены")


def test_dynamic_array_extra():
    """Серебро: поиск отсутствующего элемента, вставка в конец, сжатие."""
    da = DynamicArray()
    assert da.find(1) is None
    assert da.binary_search(1) is None

    for i in range(10):
        da.append(i)

    # Вставка в конец (index == len)
    da.insert(len(da), -1)
    assert da.get(10) == -1
    assert len(da) == 11
    da.remove(10)

    assert da.find(100) is None
    assert da.binary_search(100) is None

    # Проверка автоматического сжатия (shrink)
    big = DynamicArray()
    for i in range(100):
        big.append(i)
    assert big._capacity == 128
    for _ in range(80):
        big.remove(0)
    assert len(big) == 20
    assert big._capacity < 128

    print("DynamicArray (доп. проверки): тесты пройдены")


def test_dynamic_array_gold():
    """Золото: массив растёт при любом коэффициенте, данные не теряются."""
    for factor in (2.0, 1.5):
        arr = DynamicArrayGold(factor)
        for i in range(1000):
            arr.append(i)
        assert len(arr) == 1000
        assert arr.get(0) == 0
        assert arr.get(999) == 999
        assert arr._capacity >= 1000

    print("DynamicArrayGold: тесты пройдены")


if __name__ == "__main__":
    test_static_array()
    test_dynamic_array()
    test_dynamic_array_extra()
    test_dynamic_array_gold()
    print("Все тесты пройдены!")
