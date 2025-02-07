#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel AIM729."""

from ctypes import Structure, c_uint8, c_uint32
from enum import IntEnum


class AIM729_FILTER(IntEnum):
    """Определение параметра "Частота фильтра" в конфигурации модуля AIM729."""

    HZ50 = 0        # 50 Гц
    HZ500 = 1       # 500 Гц
    HZ1000 = 2      # 1000 Гц


class AIM729_CONFIGURATION(Structure):
    """Область конфигурационных параметров модуля AIM729."""

    _pack_ = 1
    _fields_ = [
        ("filterOptions0", c_uint8),        # Частота фильтра канала 1
        ("filterOptions1", c_uint8),        # Частота фильтра канала 2
    ]


class AIM729_INPUTS(Structure):
    """Область входных каналов "Inputs" модуля AIM729."""

    _pack_ = 1
    _fields_ = [
        ("diagnostics", c_uint8),       # Значение FFh свидетельствует об отсутствии связи с модулем
        ("input0", c_uint32),           # Код АЦП на 1-м канале ввода напряжения
        ("input1", c_uint32),           # Код АЦП на 2-м канале ввода напряжения
    ]


class AIM729(Structure):
    """Структура, представляющая модуль AIM729."""

    _pack_ = 1
    _fields_ = [
        ("Inputs", AIM729_INPUTS),                  # Область входных параметров Inputs модуля
        ("Configuration", AIM729_CONFIGURATION),    # Область конфигурационных параметров модуля
    ]
