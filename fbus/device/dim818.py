#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel DIM818."""

from ctypes import Structure, c_uint8, c_uint16, c_uint32


class DIM818_PWM_DUTY_CODE(Structure):
    """Структура описания длительности полуволн ШИМ."""

    _pack_ = 1
    _fields_ = [
        ("leadingHalfDutyCode", c_uint16),      # Длительность первой полуволны ШИМ
        ("trailingHalfDutyCode", c_uint16),     # Длительность второй полуволны ШИМ
    ]


class DIM818_CONFIGURATION(Structure):
    """Область конфигурационных параметров модуля DIM818."""

    _pack_ = 1
    _fields_ = [
        ("initialStates", c_uint32),    # Начальные состояния выходных каналов
        ("safeStates", c_uint32),       # Безопасные состояния выходных каналов
        ("enablePWM", c_uint16),        # Режим ШИМ на каналах
    ]


class DIM818_INPUTS(Structure):
    """Область входных каналов "Inputs" модуля DIM818."""

    _pack_ = 1
    _fields_ = [
        ("diagnostics", c_uint8),           # Значение FFh свидетельствует об отсутствии связи с модулем по внутренней шине
        ("outputsDiagnostics", c_uint32),   # Смежные пары битовых полей содержат статусы диагностики каналов
        ("outputsState", c_uint16),         # Биты данного канала отражают последние состояния выходов, переданные модулю
        ("timestamp", c_uint32),            # Значение счетчика миллисекунд от запуска контроллера
    ]


class DIM818_OUTPUTS(Structure):
    """Область выходных каналов "Outputs" модуля DIM818."""

    _pack_ = 1
    _fields_ = [
        ("outputsControl", c_uint16),                   # Канал управления выходами модуля
        ("PWMDutyCode", DIM818_PWM_DUTY_CODE * 16),     # Длительности полуволн ШИМ для каналов с 1 до 16
    ]


class DIM818(Structure):
    """Структура, представляющая модуль DIM818."""

    _pack_ = 1
    _fields_ = [
        ("Inputs", DIM818_INPUTS),                  # Область входных параметров Inputs модуля
        ("Outputs", DIM818_OUTPUTS),                # Область выходных параметров Outputs модуля
        ("Configuration", DIM818_CONFIGURATION),    # Область конфигурационных параметров модуля
    ]
