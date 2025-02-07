#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel AIM731."""

from ctypes import Structure, c_uint8, c_uint16
from enum import IntEnum


class AIM731_OUTPUT_RANGE(IntEnum):
    """Определение параметра "Выходной диапазон канала" в конфигурации модуля AIM731."""

    V0_10 = 0       # 0...10 В
    VDIFF10 = 1     # -10...+10 В


class AIM731_SLEW_RATE(IntEnum):
    """Определение параметра "Скорость нарастания канала" в конфигурации модуля AIM731."""

    DAC_U_SR_DISABLED = 0       # Без ограничения (Максимум)
    DAC_U_SR_0_15 = 1           # 0.15 В/с
    DAC_U_SR_0_50 = 2           # 0.5 В/с
    DAC_U_SR_1_00 = 3           # 1.0 В/с
    DAC_U_SR_2_30 = 4           # 2.3 В/с
    DAC_U_SR_4_74 = 5           # 4.7 В/с
    DAC_U_SR_9_64 = 6           # 9.6 В/с
    DAC_U_SR_19_43 = 7          # 19.4 В/с
    DAC_U_SR_39_00 = 8          # 39 В/с
    DAC_U_SR_78_18 = 9          # 78 В/с
    DAC_U_SR_156_52 = 10        # 156 В/с
    DAC_U_SR_313_19 = 11        # 313 В/с
    DAC_U_SR_626_54 = 12        # 626 В/с
    DAC_U_SR_1_25_V_MS = 13     # 1250 В/с
    DAC_U_SR_2_50_V_MS = 14     # 2500 В/с
    DAC_U_SR_5_00_V_MS = 15     # 5000 В/с
    DAC_U_SR_10_00_V_MS = 16    # 10000 В/с


class AIM731_CONFIGURATION(Structure):
    """Область конфигурационных параметров модуля AIM731."""

    _pack_ = 1
    _fields_ = [
        ("outputInitialValue0", c_uint16),      # Начальное значение канала 1
        ("outputInitialValue1", c_uint16),      # Начальное значение канала 2
        ("outputSafeValue0", c_uint16),         # Безопасное значение канала 1
        ("outputSafeValue1", c_uint16),         # Безопасное значение канала 2
        ("temperatureZonesSupport", c_uint8),   # Зарезервировано
        ("outputRange0", c_uint8),              # Выходной диапазон канала 1
        ("outputRange1", c_uint8),              # Выходной диапазон канала 2
        ("slewRateLimit0", c_uint8),            # Скорость нарастания канала 1
        ("slewRateLimit1", c_uint8),            # Скорость нарастания канала 2
    ]


class AIM731_INPUTS(Structure):
    """Область входных каналов "Inputs" модуля AIM731."""

    _pack_ = 1
    _fields_ = [
        ("diagnostics", c_uint8),       # Значение FFh свидетельствует об отсутствии связи с модулем по внутренней шине
        ("outputValue0", c_uint16),     # Текущее значение на первом канале
        ("outputValue1", c_uint16),     # Текущее значение на втором канале
    ]


class AIM731_OUTPUTS(Structure):
    """Область выходных каналов "Outputs" модуля AIM731."""

    _pack_ = 1
    _fields_ = [
        ("output0", c_uint16),      # Устанавливаемое значение на выходе первого канала
        ("output1", c_uint16),      # Устанавливаемое значение на выходе второго канала
    ]


class AIM731(Structure):
    """Структура, представляющая модуль AIM731."""

    _pack_ = 1
    _fields_ = [
        ("Inputs", AIM731_INPUTS),                  # Область входных параметров Inputs модуля
        ("Outputs", AIM731_INPUTS),                 # Область выходных параметров Outputs модуля
        ("Configuration", AIM731_CONFIGURATION),    # Область конфигурационных параметров модуля
    ]
