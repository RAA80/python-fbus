#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel AIM722."""

from ctypes import Structure, c_uint8, c_uint32
from enum import IntEnum


class AIM722_FILTER(IntEnum):
    """Определение параметра "Частота фильтра" в конфигурации модуля AIM722."""

    HZ50 = 0        # 50 Гц
    HZ1000 = 2      # 1000 Гц
    HZ100 = 4       # 100 Гц
    HZ25 = 5        # 25 Гц


class AIM722_CONFIGURATION(Structure):
    """Область конфигурационных параметров модуля AIM722."""

    _pack_ = 1
    _fields_ = [
        ("filterOptions0", c_uint8),       # Частота фильтра канала 1
        ("filterOptions1", c_uint8),       # Частота фильтра канала 2
    ]


class AIM722_INPUTS(Structure):
    """Область входных каналов "Inputs" модуля AIM722."""

    _pack_ = 1
    _fields_ = [
        ("diagnostics", c_uint8),   # Значение FFh свидетельствует об отсутствии связи с модулем
        ("input0", c_uint32),       # Код АЦП на 1-м канале измерения тока
        ("input1", c_uint32),       # Код АЦП на 2-м канале измерения тока
    ]


class AIM722(Structure):
    """Структура, представляющая модуль AIM722."""

    _pack_ = 1
    _fields_ = [
        ("Inputs", AIM722_INPUTS),                  # Область входных параметров Inputs модуля
        ("Configuration", AIM722_CONFIGURATION),    # Область конфигурационных параметров модуля
    ]
