#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel DIM715."""

from ctypes import Structure, c_uint8


class DIM715_INPUTS(Structure):
    """Область входных каналов "Inputs" модуля DIM715."""

    _pack_ = 1
    _fields_ = [
        ("diagnostics", c_uint8),       # Значение FFh свидетельствует об отсутствии связи с модулем по внутренней шине
        ("inputStates", c_uint8),       # Первые два бита данного канала отражают текущее состояние соответствующих входных каналов
    ]


class DIM715(Structure):
    """Структура, представляющая модуль DIM715."""

    _pack_ = 1
    _fields_ = [
        ("Inputs", DIM715_INPUTS),      # Область входных параметров Inputs модуля
     ]
