#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel DIM712."""

from ctypes import Structure, c_uint8


class DIM712_CONFIGURATION(Structure):
    """Область конфигурационных параметров модуля DIM712."""

    _pack_ = 1
    _fields_ = [
        ("initialOutputStates", c_uint8),       # Начальные состояния каналов
        ("outputSafeStates", c_uint8),          # Безопасные состояния каналов
    ]


class DIM712_INPUTS(Structure):
    """Область входных каналов "Inputs" модуля DIM712."""

    _pack_ = 1
    _fields_ = [
        ("diagnostics", c_uint8),       # Значение FFh свидетельствует об отсутствии связи с модулем по внутренней шине
        ("inputStates", c_uint8),       # Первые два бита данного канала отражают текущее состояние соответствующих каналов релейной коммутации
    ]


class DIM712_OUTPUTS(Structure):
    """Область выходных каналов "Outputs" модуля DIM712."""

    _pack_ = 1
    _fields_ = [
        ("outputsControl", c_uint8),    # Первые два бита данного канала предназначены для управления каналами релейной коммутации модуля
    ]


class DIM712(Structure):
    """Структура, представляющая модуль DIM712."""

    _pack_ = 1
    _fields_ = [
        ("Inputs", DIM712_INPUTS),                  # Область входных параметров Inputs модуля
        ("Outputs", DIM712_OUTPUTS),                # Область выходных параметров Outputs модуля
        ("Configuration", DIM712_CONFIGURATION),    # Область конфигурационных параметров модуля
    ]
