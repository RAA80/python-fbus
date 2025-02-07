#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel DIM764."""

from ctypes import Structure, c_uint8, c_uint32
from enum import IntEnum

DIM764_CHANNELS_COUNT = 8   # Число физических дискретных каналов модуля DIM764-0-0


class DIM764_FILTER_OPTIONS(IntEnum):
    """Частота дискретизации фильтра, применяемого к сигналам на входных каналах."""

    MHZ50 = 0       # 50 МГц
    MHZ5 = 1        # 5 МГц
    MHZ2_5 = 2      # 2.5 МГц


class DIM764_INPUT_MODE(IntEnum):
    """Режим работы дискретного канала."""

    PERIOD = 0      # Измерение периода входного сигнала
    INTERVAL = 1    # Измерение интервала между двумя последовательными импульсами входного сигнала
    PHASE = 2       # Измерение сдвига фазы сигнала в паре ведущий-ведомый
    COUNTER = 3     # Счётчик импульсов
    DISABLED = 4    # Канал отключен


class DIM764_EDGE(IntEnum):
    """Активный фронт / либо уровень входного сигнала."""

    RISING = 0      # Передний фронт/высокий уровень
    FALLING = 1     # Задний фронт/низкий уровень


class DIM764_COUNTER(IntEnum):
    """Режим счета для ведущего канала."""

    ABSOLUTE = 0        # Режим условного счета выключен
    CONDITIONAL = 1     # Режим условного счета включен


class DIM764_CHANNEL_CFG(Structure):
    """Настройка канала модуля DIM764."""

    _pack_ = 1
    _fields_ = [
        ("inputMode", c_uint8),     # Режим работы дискретного канала
        ("paramsMask", c_uint8),    # Настройки параметров: условного счета, фильтра, входного сигнала
    ]


class DIM764_CONFIGURATION(Structure):
    """Область конфигурационных параметров модуля DIM764."""

    _pack_ = 1
    _fields_ = [
        ("version", c_uint8),                                               # Код типа прошивки FPGA. Должен быть 0
        ("subVersion", c_uint8),                                            # Код исполнения прошивки FPGA. Должен быть 0
        ("filterOption", c_uint8),                                          # Частота фильтра
        ("channelsConfig", DIM764_CHANNEL_CFG * DIM764_CHANNELS_COUNT),     # Настройки каналов 1…8 (задаются отдельно по каждому каналу)
    ]


class DIM764_INPUTS(Structure):
    """Область входных каналов "Inputs" модуля DIM764."""

    _pack_ = 1
    _fields_ = [
        ("diagnostics", c_uint8),                           # Значение FFh свидетельствует об отсутствии связи с модулем по внутренней шине
        ("controlState", c_uint8),                          # Контрольный код последнего обновления выходов модуля
        ("channelsState", c_uint8),                         # Состояние каналов
        ("values", c_uint32 * DIM764_CHANNELS_COUNT),       # Массив значений на каналах
        ("inputsState", c_uint8),                           # Состояние дискретных входов модуля
    ]


class DIM764_OUTPUTS(Structure):
    """Область выходных каналов "Outputs" модуля DIM764."""

    _pack_ = 1
    _fields_ = [
        ("control", c_uint8),           # Контрольный код обновления данных выходов
        ("resetCounters", c_uint8),     # Команда сброса счётчиков каналов
    ]


class DIM764(Structure):
    """Структура, представляющая модуль DIM764."""

    _pack_ = 1
    _fields_ = [
        ("Inputs", DIM764_INPUTS),                  # Область входных параметров Inputs модуля
        ("Outputs", DIM764_OUTPUTS),                # Область выходных параметров Outputs модуля
        ("Configuration", DIM764_CONFIGURATION),    # Область конфигурационных параметров модуля
    ]
