#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel AIM792."""

from ctypes import Structure, c_uint8, c_uint16
from enum import IntEnum


class AIM792_RANGE(IntEnum):
    """Определение параметра "Диапазон канала" в конфигурации модуля AIM792."""

    V0_5 = 0        # 0...5 В
    V0_10 = 1       # 0...10 В
    VDIFF5 = 2      # -5...+5 В
    VDIFF10 = 3     # -10...+10 В


class AIM792_CONFIGURATION(Structure):
    """Область конфигурационных параметров модуля AIM792."""

    _pack_ = 1
    _fields_ = [
        ("inputRange", c_uint8),            # Резерв! Не используется
        ("scanRate", c_uint8),              # Период опроса (мс)
        ("filterDepth", c_uint8),           # Глубина фильтра
        ("lowLimit", c_uint16 * 8),         # Нижний предел канала (1...8)
        ("highLimit", c_uint16 * 8),        # Верхний предел канала (1...8)
        ("channelRanges", c_uint8 * 8),     # Диапазон канала (1...8)
    ]


class AIM792_INPUTS(Structure):
    """Область входных каналов "Inputs" модуля AIM792."""

    _pack_ = 1
    _fields_ = [
        ("diagnostics", c_uint8),       # Значение FFh свидетельствует об отсутствии связи с модулем по внутренней шине
        ("channelRanges", c_uint16),    # Коды текущих выбранных диапазонов для каналов измерения напряжения
        ("channelsStatus", c_uint16),   # Статус каналов измерения напряжения
        ("values", c_uint16 * 8),       # Код АЦП на каждом канале измерения напряжения
    ]


class AIM792(Structure):
    """Структура, представляющая модуль AIM792."""

    _pack_ = 1
    _fields_ = [
        ("Inputs", AIM792_INPUTS),                  # Область входных параметров Inputs модуля
        ("Configuration", AIM792_CONFIGURATION),    # Область конфигурационных параметров модуля
    ]
