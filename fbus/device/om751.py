#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel OM751."""

from ctypes import Structure, c_uint8


class OM751_INPUTS(Structure):
    """Область входных каналов "Inputs" модуля OM751."""

    _pack_ = 1
    _fields_ = [
        ("diagnostics", c_uint8),       # Значение FFh свидетельствует об отсутствии связи с модулем по внутренней шине
        ("inputStates", c_uint8),       # Битовая маска статусных каналов
    ]


class OM751(Structure):
    """Структура, представляющая модуль OM751."""

    _pack_ = 1
    _fields_ = [
        ("Inputs", OM751_INPUTS),       # Область входных параметров Inputs модуля
     ]
