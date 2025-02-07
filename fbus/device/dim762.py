#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel DIM762."""

from ctypes import Structure, c_uint8, c_uint16
from enum import IntEnum


class DIM762_DEBOUNCE(IntEnum):
    """Определение параметра "Устранение дребезга контактов" в конфигурации модуля DIM762."""

    NODEBOUNCE = 0          # антидребезг не используется
    DEBOUNCE_200US = 1      # время устранения дребезга около 200 мкс
    DEBOUNCE_3MS = 2        # время устранения дребезга около 3 мс


class DIM762_EDGE_SETTINGS(IntEnum):
    """Определение параметра "Конфигурация счетчика" в конфигурации модуля DIM762."""

    RISINGEDGE = 0          # Передний фронт
    FALLINGEDGE = 1         # Задний фронт


class DIM762_COUNTER_DIRECTION(IntEnum):
    """Определение параметра "Направление счета" в конфигурации модуля DIM762."""

    UPWARDCOUNT = 0         # Счет с суммированием
    DOWNWARDCOUNT = 1       # Счет с вычитанием


class DIM762_COUNTER_MODE(IntEnum):
    """Тип поведения счетчика при достижении предельного значения."""

    CONTINUOUSUPDATE = 0    # Прекращение счета
    CYCLICUPDATE = 1        # Циклический счетчик


class DIM762_COUNTER_INPUT_SETTINGS(Structure):
    """Конфигурация счетчика."""

    _pack_ = 1
    _fields_ = [
        ("edge", c_uint8),              # Выбор активного фронта сигнала
        ("direction", c_uint8),         # Направление счета
        ("countingMode", c_uint8),      # Тип поведения счетчика при достижении предельного значения
        ("presetValue", c_uint16),      # Предустановленное значение
    ]


class DIM762_CONFIGURATION(Structure):
    """Область конфигурационных параметров модуля DIM762."""

    _pack_ = 1
    _fields_ = [
        ("debounce", c_uint8),                                      # Устранение дребезга контактов
        ("enableCounting", c_uint8),                                # Режим счетчика
        ("countingParameters", DIM762_COUNTER_INPUT_SETTINGS * 2),  # Конфигурация счетчика 1..2
    ]


class DIM762_INPUTS(Structure):
    """Область входных каналов "Inputs" модуля DIM762."""

    _pack_ = 1
    _fields_ = [
        ("diagnostics", c_uint8),       # Значение FFh свидетельствует об отсутствии связи с модулем по внутренней шине
        ("inputStates", c_uint8),       # Биты данного канала отражают текущее состояние соответствующих физических каналов
        ("counter0", c_uint16),         # Значения суммирующих счетчиков на первом канале
        ("counter1", c_uint16),         # Значения суммирующих счетчиков на втором канале
        ("countersState", c_uint8),     # Зарезервировано/Не используется в текущей версии прошивки модуля
    ]


class DIM762(Structure):
    """Структура, представляющая модуль DIM762."""

    _pack_ = 1
    _fields_ = [
        ("Inputs", DIM762_INPUTS),                  # Область входных параметров Inputs модуля
        ("Configuration", DIM762_CONFIGURATION),    # Область конфигурационных параметров модуля
    ]
