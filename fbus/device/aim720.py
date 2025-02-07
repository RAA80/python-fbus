#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel AIM720."""

from ctypes import Structure, c_uint8, c_uint16
from enum import IntEnum


class AIM720_RANGE(IntEnum):
    """Определение параметра "Входной диапазон" в конфигурации модуля AIM720."""

    V0_5 = 0        # 0...5В
    V0_10 = 1       # 0...10В
    VM5_5 = 2       # -5...5В
    VM10_10 = 3     # -10...10В


class AIM720_CONFIGURATION(Structure):
    """Область конфигурационных параметров модуля AIM720."""

    _pack_ = 1
    _fields_ = [
        ("inputsRange", c_uint8),       # Входной диапазон
        ("scanPeriod", c_uint16),       # Период опроса (от 0 до 65535)
        ("filterDepth", c_uint8),       # Глубина фильтра (от 0 до 10)
    ]


class AIM720_INPUTS(Structure):
    """Область входных каналов "Inputs" модуля AIM720."""

    _pack_ = 1
    _fields_ = [
        ("diagnostics", c_uint8),           # При равенстве 0 значения остальных каналов достоверны. Значение FFh свидетельствует об отсутствии связи с модулем
        ("voltageInput0", c_uint16),        # Код АЦП на 1-м канале ввода напряжения. Действительны первые 12 разрядов
        ("voltageInput1", c_uint16),        # Код АЦП на 2-м канале ввода напряжения. Действительны первые 12 разрядов
        ("voltageInput2", c_uint16),        # Код АЦП на 3-м канале ввода напряжения. Действительны первые 12 разрядов
        ("currentInput0", c_uint16),        # Код АЦП на 1-м канале ввода тока. Действительны первые 12 разрядов
        ("currentInput1", c_uint16),        # Код АЦП на 2-м канале ввода тока. Действительны первые 12 разрядов
        ("currentInput2", c_uint16),        # Код АЦП на 3-м канале ввода тока. Действительны первые 12 разрядов
        ("zeroReference", c_uint16),        # Код АЦП на канале АЦП, который подключен к аналоговой «земле»
        ("halfScaleReference", c_uint16),   # Код АЦП, соответствующий опорному напряжению АЦП (около 2,5 В)
    ]


class AIM720(Structure):
    """Структура, представляющая модуль AIM720."""

    _pack_ = 1
    _fields_ = [
        ("Inputs", AIM720_INPUTS),                  # Область входных параметров Inputs модуля
        ("Configuration", AIM720_CONFIGURATION),    # Область конфигурационных параметров модуля
    ]
