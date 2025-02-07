#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel DIM812."""

from ctypes import Structure, c_uint8, c_uint32


class DIM812_CONFIGURATION(Structure):
    """Область конфигурационных параметров модуля DIM812."""

    _pack_ = 1
    _fields_ = [
        ("InitialStates", c_uint8),     # Начальные состояния выходных каналов
        ("SafeStates", c_uint8),        # Безопасные состояния выходных каналов
    ]


class DIM812_INPUTS(Structure):
    """Область входных каналов "Inputs" модуля DIM812."""

    _pack_ = 1
    _fields_ = [
        ("diagnostics", c_uint8),       # Значение FFh свидетельствует об отсутствии связи с модулем по внутренней шине
        ("outputsState", c_uint8),      # Первые четыре бита данного канала отражают текущее состояние соответствующих каналов релейной коммутации
        ("timestamp", c_uint32),        # Значение счетчика миллисекунд от запуска контроллера
    ]


class DIM812_OUTPUTS(Structure):
    """Область выходных каналов "Outputs" модуля DIM812."""

    _pack_ = 1
    _fields_ = [
        ("outputsControl", c_uint8),        # Первые четыре бита данного канала предназначены для управления каналами релейной коммутации модуля
    ]


class DIM812(Structure):
    """Структура, представляющая модуль DIM812."""

    _pack_ = 1
    _fields_ = [
        ("Inputs", DIM812_INPUTS),                  # Область входных параметров Inputs модуля
        ("Outputs", DIM812_OUTPUTS),                # Область выходных параметров Outputs модуля
        ("Configuration", DIM812_CONFIGURATION),    # Область конфигурационных параметров модуля
    ]
