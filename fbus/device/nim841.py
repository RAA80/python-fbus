#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel NIM841."""

from ctypes import Structure, c_uint8, c_uint16
from enum import IntEnum


class NIM841_UART_BAUDRATE(IntEnum):
    """Скорость обмена."""

    BPS300 = 0
    BPS1200 = 1
    BPS2400 = 2
    BPS4800 = 3
    BPS9600 = 4
    BPS14400 = 5
    BPS19200 = 6
    BPS38400 = 7
    BPS57600 = 8
    BPS115200 = 9


class NIM841_UART_DATABITS(IntEnum):
    """Количество бит данных."""

    BITS8 = 0
    BITS7 = 1


class NIM841_UART_STOPBITS(IntEnum):
    """Количество стоповых бит."""

    BIT1 = 0
    BIT2 = 1


class NIM841_UART_PARITY(IntEnum):
    """Четность."""

    NONE = 0
    EVEN = 1
    ODD = 2


class NIM841_UART_MODE(IntEnum):
    """Тип интерфейса модуля NIM841."""

    RS485 = 0
    RS422 = 1


class NIM841_CONFIGURATION(Structure):
    """Области конфигурационных параметров модулей NIM841."""

    _pack_ = 1
    _fields_ = [
        ("Mode", c_uint8),          # Зарезервировано! Должно быть равным 0
        ("Baudrate", c_uint8),      # Скорость обмена
        ("Databits", c_uint8),      # Количество бит данных
        ("Stopbits", c_uint8),      # Количество стоповых бит
        ("Parity", c_uint8),        # Четность
    ]


class NIM841_INPUTS(Structure):
    """Области входных каналов "Inputs" модулей NIM841."""

    _pack_ = 1
    _fields_ = [
        ("Diagnostics", c_uint8),       # Диагностический виртуальный канал модуля
        ("Status", c_uint16),           # Битовая маска статусных признаков модуля
        ("FIFOLength", c_uint16),       # Количество байт в буфере приема модуля
        ("rx_Control", c_uint8),        # Канал статуса управления передачей данных из приемного буфера
        ("rx_Length", c_uint8),         # Количество байт данных передаваемых модулем из внутреннего буфера приема в текущем цикле обмена по FBUS
        ("rx_Data", c_uint8 * 32),      # Окно для передачи данных из внутреннего буфера приема модуля
    ]


class NIM841_OUTPUTS(Structure):
    """Области выходных каналов "Outputs" модулей NIM841."""

    _pack_ = 1
    _fields_ = [
        ("Control", c_uint16),          # Битовая маска команд управления
        ("tx_Control", c_uint8),        # Канал управления записью данных в буфер передачи
        ("tx_Length", c_uint8),         # Количество байт, передаваемых модулю в массиве tx_Data для записи в FIFO передачи
        ("tx_Data", c_uint8 * 32),      # Данные для записи в FIFO передачи
    ]


class NIM841(Structure):
    """Структура, представляющая модуль NIM841."""

    _pack_ = 1
    _fields_ = [
        ("Inputs", NIM841_INPUTS),                  # Область входных параметров Inputs модуля
        ("Outputs", NIM841_OUTPUTS),                # Область выходных параметров Outputs модуля
        ("Configuration", NIM841_CONFIGURATION),    # Область конфигурационных параметров модуля
    ]
