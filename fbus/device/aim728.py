#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel AIM728."""

from ctypes import Structure, c_uint8, c_uint32
from enum import IntEnum


class AIM728_FILTER(IntEnum):
    """Определение параметра "Частота фильтра" в конфигурации модуля AIM728."""

    HZ50 = 0        # 50 Гц
    HZ500 = 1       # 500 Гц
    HZ1000 = 2      # 1000 Гц


class AIM728_CONFIGURATION(Structure):
    """Область конфигурационных параметров модуля AIM728."""

    _pack_ = 1
    _fields_ = [
        ("filterOptions0", c_uint8),        # Частота фильтра канала 1
        ("filterOptions1", c_uint8),        # Частота фильтра канала 2
        ("filterOptions2", c_uint8),        # Частота фильтра канала 3
        ("filterOptions3", c_uint8),        # Частота фильтра канала 4
    ]


class AIM728_INPUTS(Structure):
    """Область входных каналов "Inputs" модуля AIM728."""

    _pack_ = 1
    _fields_ = [
        ("diagnostics", c_uint8),       # Значение FFh свидетельствует об отсутствии связи с модулем
        ("input0", c_uint32),           # Код АЦП на 1-м канале ввода напряжения
        ("input1", c_uint32),           # Код АЦП на 2-м канале ввода напряжения
        ("input2", c_uint32),           # Код АЦП на 3-м канале ввода напряжения
        ("input3", c_uint32),           # Код АЦП на 4-м канале ввода напряжения
    ]


class AIM728(Structure):
    """Структура, представляющая модуль AIM728."""

    _pack_ = 1
    _fields_ = [
        ("Inputs", AIM728_INPUTS),                  # Область входных параметров Inputs модуля
        ("Configuration", AIM728_CONFIGURATION),    # Область конфигурационных параметров модуля
    ]
