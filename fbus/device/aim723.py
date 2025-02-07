#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel AIM723."""

from ctypes import Structure, c_uint8, c_uint32
from enum import IntEnum


class AIM723_FILTER(IntEnum):
    """Определение параметра "Частота фильтра" в конфигурации модуля AIM723."""

    HZ50 = 0        # 50 Гц
    HZ1000 = 2      # 1000 Гц
    HZ100 = 4       # 100 Гц
    HZ25 = 5        # 25 Гц


class AIM723_CONFIGURATION(Structure):
    """Область конфигурационных параметров модуля AIM723."""

    _pack_ = 1
    _fields_ = [
        ("filterOptions0", c_uint8),       # Частота фильтра канала 1
        ("filterOptions1", c_uint8),       # Частота фильтра канала 2
        ("filterOptions2", c_uint8),       # Частота фильтра канала 3
        ("filterOptions3", c_uint8),       # Частота фильтра канала 4
    ]


class AIM723_INPUTS(Structure):
    """Область входных каналов "Inputs" модуля AIM723."""

    _pack_ = 1
    _fields_ = [
        ("diagnostics", c_uint8),   # Значение FFh свидетельствует об отсутствии связи с модулем
        ("input0", c_uint32),       # Код АЦП на 1-м канале измерения тока
        ("input1", c_uint32),       # Код АЦП на 2-м канале измерения тока
        ("input2", c_uint32),       # Код АЦП на 3-м канале измерения тока
        ("input3", c_uint32),       # Код АЦП на 4-м канале измерения тока
    ]


class AIM723(Structure):
    """Структура, представляющая модуль AIM723."""

    _pack_ = 1
    _fields_ = [
        ("Inputs", AIM723_INPUTS),                  # Область входных параметров Inputs модуля
        ("Configuration", AIM723_CONFIGURATION),    # Область конфигурационных параметров модуля
    ]
