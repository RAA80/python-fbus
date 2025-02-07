#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel AIM724."""

from ctypes import Structure, c_float, c_uint8
from enum import IntEnum


class AIM724_SCAN_RATE(IntEnum):
    """Определение параметра "Период опроса" в конфигурации модуля AIM724."""

    MS200 = 0       # 200 мс


class AIM724_CJC_MODE(IntEnum):
    """Определение параметра "Компенсация холодного спая" в конфигурации модуля AIM724."""

    EXTERNAL_SOURCE = 1     # Внешний термометр
    DISABLED = 2            # Не используется
    INTERNAL_SENSOR = 3     # Встроенный термометр


class AIM724_RANGE(IntEnum):
    """Определение параметра "Входной диапазон" в конфигурации модуля AIM724."""

    TC_J = 0            # TC типа J
    TC_K = 1            # TC типа K
    TC_N = 2            # TC типа N
    TC_T = 3            # TC типа T
    TC_E = 4            # TC типа E
    TC_R = 5            # TC типа R
    TC_S = 6            # TC типа S
    TC_B = 7            # TC типа B
    MV_DIFF20 = 8       # -20...+20 мВ
    MV_DIFF50 = 9       # -50...+50 мВ
    MV_DIFF100 = 10     # -100...+100 мВ
    MV_DIFF200 = 11     # -200...+200 мВ
    TC_L = 17           # TC типа L


class AIM724_CONFIGURATION(Structure):
    """Область конфигурационных параметров модуля AIM724."""

    _pack_ = 1
    _fields_ = [
        ("scanRate", c_uint8),          # Период опроса
        ("cjc_mode", c_uint8),          # Компенсация холодного спая
        ("inputRange", c_uint8),        # Входной диапазон
    ]


class AIM724_INPUTS(Structure):
    """Область входных каналов "Inputs" модуля AIM724."""

    _pack_ = 1
    _fields_ = [
        ("diagnostics", c_uint8),       # Значение FFh свидетельствует об отсутствии связи с модулем
        ("channel0", c_float),          # Значение в выбранном диапазоне на первом канале в единицах физической величины
        ("channel1", c_float),          # Значение в выбранном диапазоне на втором канале в единицах физической величины
        ("cjcInput", c_float),          # Значение температуры холодного спая, измеренное встроенным датчиком
    ]


class AIM724_OUTPUTS(Structure):
    """Область выходных каналов "Outputs" модуля AIM724."""

    _pack_ = 1
    _fields_ = [
        ("cjcExternalSource", c_float),     # Значение температуры холодного спая, передаваемое в модуль приложением
    ]


class AIM724(Structure):
    """Структура, представляющая модуль AIM724."""

    _pack_ = 1
    _fields_ = [
        ("Inputs", AIM724_INPUTS),                  # Область входных параметров Inputs модуля
        ("Outputs", AIM724_OUTPUTS),                # Область выходных параметров Outputs модуля
        ("Configuration", AIM724_CONFIGURATION),    # Область конфигурационных параметров модуля
    ]
