#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel AIM727."""

from ctypes import Structure, c_uint8, c_uint32
from enum import IntEnum


class AIM727_FILTER(IntEnum):
    """Определение параметра "Частота фильтра" в конфигурации модуля AIM727."""

    HZ50 = 0        # 50 Гц
    HZ500 = 1       # 500 Гц
    HZ1000 = 2      # 1000 Гц


class AIM727_CONFIGURATION(Structure):
    """Область конфигурационных параметров модуля AIM727."""

    _pack_ = 1
    _fields_ = [
        ("filterOptions0", c_uint8),        # Частота фильтра канала 1
        ("filterOptions1", c_uint8),        # Частота фильтра канала 2
        ("filterOptions2", c_uint8),        # Частота фильтра канала 3
        ("filterOptions3", c_uint8),        # Частота фильтра канала 4
    ]


class AIM727_INPUTS(Structure):
    """Область входных каналов "Inputs" модуля AIM727."""

    _pack_ = 1
    _fields_ = [
        ("diagnostics", c_uint8),       # Значение FFh свидетельствует об отсутствии связи с модулем
        ("input0", c_uint32),           # Код АЦП на 1-м канале ввода напряжения
        ("input1", c_uint32),           # Код АЦП на 2-м канале ввода напряжения
        ("input2", c_uint32),           # Код АЦП на 3-м канале ввода напряжения
        ("input3", c_uint32),           # Код АЦП на 4-м канале ввода напряжения
    ]


class AIM727(Structure):
    """Структура, представляющая модуль AIM727."""

    _pack_ = 1
    _fields_ = [
        ("Inputs", AIM727_INPUTS),                  # Область входных параметров Inputs модуля
        ("Configuration", AIM727_CONFIGURATION),    # Область конфигурационных параметров модуля
    ]
