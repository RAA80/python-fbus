#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel DIM813."""

from ctypes import Structure, c_uint8, c_uint32


class DIM813_CONFIGURATION(Structure):
    """Область конфигурационных параметров модуля DIM813."""

    _pack_ = 1
    _fields_ = [
        ("InitialStates", c_uint8),     # Начальные состояния выходных каналов
        ("SafeStates", c_uint8),        # Безопасные состояния выходных каналов
    ]


class DIM813_INPUTS(Structure):
    """Область входных каналов "Inputs" модуля DIM813."""

    _pack_ = 1
    _fields_ = [
        ("diagnostics", c_uint8),       # Значение FFh свидетельствует об отсутствии связи с модулем по внутренней шине
        ("outputsState", c_uint8),      # Первые четыре бита данного канала отражают текущее состояние соответствующих каналов релейной коммутации
        ("timestamp", c_uint32),        # Значение счетчика миллисекунд от запуска контроллера
    ]


class DIM813_OUTPUTS(Structure):
    """Область выходных каналов "Outputs" модуля DIM813."""

    _pack_ = 1
    _fields_ = [
        ("outputsControl", c_uint8),        # Первые четыре бита данного канала предназначены для управления каналами релейной коммутации модуля
    ]


class DIM813(Structure):
    """Структура, представляющая модуль DIM813."""

    _pack_ = 1
    _fields_ = [
        ("Inputs", DIM813_INPUTS),                  # Область входных параметров Inputs модуля
        ("Outputs", DIM813_OUTPUTS),                # Область выходных параметров Outputs модуля
        ("Configuration", DIM813_CONFIGURATION),    # Область конфигурационных параметров модуля
    ]
