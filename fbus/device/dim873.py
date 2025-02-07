#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel DIM873."""

from ctypes import Structure, c_uint8, c_uint16, c_uint32


class DIM873_CONFIGURATION(Structure):
    """Область конфигурационных параметров модуля DIM873."""

    _pack_ = 1
    _fields_ = [
        ("initialStates", c_uint32),    # Начальные состояния выходных каналов
        ("SafeStates", c_uint32),       # Безопасные состояния выходных каналов
    ]


class DIM873_INPUTS(Structure):
    """Область входных каналов "Inputs" модуля DIM873."""

    _pack_ = 1
    _fields_ = [
        ("diagnostics", c_uint8),       # Значение FFh свидетельствует об отсутствии связи с модулем по внутренней шине
        ("outputsState", c_uint16),     # Биты данного канала отражают текущее состояние соответствующих каналов релейной коммутации
        ("timestamp", c_uint32),        # Значение счетчика миллисекунд от запуска контроллера
    ]


class DIM873_OUTPUTS(Structure):
    """Область выходных каналов "Outputs" модуля DIM873."""

    _pack_ = 1
    _fields_ = [
        ("OutputsControl", c_uint16),       # Биты данного канала предназначены для управления каналами релейной коммутации модуля
    ]


class DIM873(Structure):
    """Структура, представляющая модуль DIM873."""

    _pack_ = 1
    _fields_ = [
        ("Inputs", DIM873_INPUTS),                  # Область входных параметров Inputs модуля
        ("Outputs", DIM873_OUTPUTS),                # Область выходных параметров Outputs модуля
        ("Configuration", DIM873_CONFIGURATION),    # Область конфигурационных параметров модуля
    ]
