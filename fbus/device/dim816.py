#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel DIM816."""

from ctypes import Structure, c_uint8, c_uint16, c_uint32


class DIM816_CONFIGURATION(Structure):
    """Область конфигурационных параметров модуля DIM816."""

    _pack_ = 1
    _fields_ = [
        ("onDelay", c_uint8 * 4),       # Программные задержки включения каналов
        ("offDelay", c_uint8 * 4),      # Программные задержки выключения каналов
        ("countingModes", c_uint8),     # Режимы работы счетчиков
    ]


class DIM816_INPUTS(Structure):
    """Область входных каналов "Inputs" модуля DIM816."""

    _pack_ = 1
    _fields_ = [
        ("diagnostics", c_uint8),       # Значение FFh свидетельствует об отсутствии связи с модулем по внутренней шине
        ("inputsState", c_uint8),       # Биты данного канала отражают текущее состояние соответствующих входных каналов
        ("timestamp", c_uint32),        # Значение счетчика миллисекунд от запуска контроллера
        ("lastCommand", c_uint16),      # Последнее значение счетчика команды сброса "Counter0–15"
        ("counter", c_uint16 * 4),      # Циклические счетчики фронтов на входах модуля
    ]


class DIM816_OUTPUTS(Structure):
    """Область выходных каналов "Outputs" модуля DIM816."""

    _pack_ = 1
    _fields_ = [
        ("resetCommand", c_uint8),          # Битовая маска сброса счетчиков
        ("commandCounter", c_uint16),       # Счетчик команды сброса
    ]


class DIM816(Structure):
    """Структура, представляющая модуль DIM816."""

    _pack_ = 1
    _fields_ = [
        ("Inputs", DIM816_INPUTS),                  # Область входных параметров Inputs модуля
        ("Outputs", DIM816_OUTPUTS),                # Область выходных параметров Outputs модуля
        ("Configuration", DIM816_CONFIGURATION),    # Область конфигурационных параметров модуля
    ]
