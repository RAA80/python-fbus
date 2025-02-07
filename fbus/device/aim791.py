#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel AIM791."""

from ctypes import Structure, c_uint8, c_uint16
from enum import IntEnum


class AIM791_RANGE(IntEnum):
    """Определение параметра "Диапазон канала" в конфигурации модуля AIM791."""

    MA0_5 = 0           # 0...5 mA
    MA0_20 = 1          # 0...20 мА
    MA4_20 = 2          # 4...20 мА


class AIM791_CONFIGURATION(Structure):
    """Область конфигурационных параметров модуля AIM791."""

    _pack_ = 1
    _fields_ = [
        ("inputRange", c_uint8),            # Резерв! Не используется
        ("scanRate", c_uint8),              # Период опроса (мс)
        ("filterDepth", c_uint8),           # Глубина фильтра
        ("lowLimit", c_uint16 * 8),         # Нижний предел канала (1...8)
        ("highLimit", c_uint16 * 8),        # Верхний предел канала (1...8)
        ("channelRanges", c_uint8 * 8),     # Диапазон канала (1...8)
    ]


class AIM791_INPUTS(Structure):
    """Область входных каналов "Inputs" модуля AIM791."""

    _pack_ = 1
    _fields_ = [
        ("diagnostics", c_uint8),       # Значение FFh свидетельствует об отсутствии связи с модулем по внутренней шине
        ("channelRanges", c_uint16),    # Коды текущих выбранных диапазонов для каналов измерения тока
        ("channelsStatus", c_uint16),   # Статус каналов измерения тока
        ("values", c_uint16 * 8),       # Код АЦП на каждом канале измерения тока
    ]


class AIM791(Structure):
    """Структура, представляющая модуль AIM791."""

    _pack_ = 1
    _fields_ = [
        ("Inputs", AIM791_INPUTS),                  # Область входных параметров Inputs модуля
        ("Configuration", AIM791_CONFIGURATION),    # Область конфигурационных параметров модуля
    ]
