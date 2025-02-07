#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel AIM733."""

from ctypes import Structure, c_uint8, c_uint32
from enum import IntEnum


class AIM733_FILTER(IntEnum):
    """Определение параметра "Частота фильтра" в конфигурации модуля AIM733."""

    HZ50 = 0        # 50 Гц
    HZ500 = 1       # 500 Гц
    HZ1000 = 2      # 1000 Гц
    HZ12_5 = 3      # 12,5 Гц


class AIM733_INPUT_RANGE(IntEnum):
    """Определение параметра "Диапазон канала" в конфигурации модуля AIM733."""

    V0_5 = 0        # 0...5 В
    V0_2D5 = 1      # 0,0...2,5 В


class AIM733_CONFIGURATION(Structure):
    """Область конфигурационных параметров модуля AIM733."""

    _pack_ = 1
    _fields_ = [
        ("filterOptions0", c_uint8),    # Частота фильтра канала 1
        ("filterOptions1", c_uint8),    # Частота фильтра канала 2
        ("filterOptions2", c_uint8),    # Частота фильтра канала 3
        ("filterOptions3", c_uint8),    # Частота фильтра канала 4
        ("range0", c_uint8),            # Диапазон канала 1
        ("range1", c_uint8),            # Диапазон канала 2
        ("range2", c_uint8),            # Диапазон канала 3
        ("range3", c_uint8),            # Диапазон канала 4
    ]


class AIM733_INPUTS(Structure):
    """Область входных каналов "Inputs" модуля AIM733."""

    _pack_ = 1
    _fields_ = [
        ("diagnostics", c_uint8),   # Значение FFh свидетельствует об отсутствии связи с модулем по внутренней шине
        ("input0", c_uint32),       # Код АЦП и диагностика 1-го канала ввода напряжения
        ("input1", c_uint32),       # Код АЦП и диагностика 2-го канала ввода напряжения
        ("input2", c_uint32),       # Код АЦП и диагностика 3-го канала ввода напряжения
        ("input3", c_uint32),       # Код АЦП и диагностика 4-го канала ввода напряжения
    ]


class AIM733(Structure):
    """Структура, представляющая модуль AIM733."""

    _pack_ = 1
    _fields_ = [
        ("Inputs", AIM733_INPUTS),                  # Область входных параметров Inputs модуля
        ("Configuration", AIM733_CONFIGURATION),    # Область конфигурационных параметров модуля
    ]
