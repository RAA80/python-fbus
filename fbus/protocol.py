#! /usr/bin/env python3

"""Определения структур для взаимодействия с приборами Fastwel по шине FBUS.
Fastwel FBUS SDK Версия 2.4.
"""

from ctypes import Structure, c_char, c_size_t, c_uint8, c_uint16, c_uint32
from enum import IntEnum, auto

FBUS_MULTICAST_ID = 0x7E

FBUS_MAX_NODE_COUNT = 64
FBUS_MAX_NODE_ID = FBUS_MAX_NODE_COUNT - 1

FBUS_GROUP_ID_MIN = 0x80
FBUS_GROUP_ID_MAX = FBUS_GROUP_ID_MIN + FBUS_MAX_NODE_ID

FBUS_UNDEFINED_GROUP_ID = 0xFF
FBUS_UNDEFINED_SYNC_ID = 0xFF


class FBUS_ADAPTER(IntEnum):
    """Тип адаптера."""

    LOCAL = 0
    TCP = 1


class FBUS_RESULT(IntEnum):
    """Коды ошибок."""

    OK = 0                                      # Успешное выполнение
    NOERROR = OK                                # Успешное выполнение

    INVALID_STATE = auto()                      # Неверное состояние сети для вызова данной функции: закрытие активного объекта, одновременный доступ к объекту и т.п.
    NO_SYSTEM_RESOURCE = auto()                 # Недостаток системных ресурсов
    INCORRECT_PARAM = auto()                    # Неверные параметры
    OPEN_ADAPTER = auto()                       # Ошибка открытия устройства FBUS MASTER
    GROUP_UNDEFINED = auto()                    # Группа с данным идентификатором не определена
    INVALID_GROUP_CONFIG = auto()               # Ошибка в параметрах конфигурации группы
    GROUP_ALLOCATION_ERR = auto()               # Ошибка создания объекта группы
    GROUP_CONFIG_NOT_SINCHRONIZED = auto()      # Несовпадение конфигурации в памяти и в физическом модуле
    GROUP_NOT_CREATED = auto()                  # Системная ошибка при создании группы
    INVALID_GROUP_ID = auto()                   # Неверный идентификатор группы
    NODE_NOT_ASSIGNED_TO_GROUP = auto()         # Узел не входит в группу
    INVALID_EXCHANGE_REGION = auto()            # Ошибка задания параметров области обмена данными
    RPC_ERROR = auto()                          # Ошибка выполнения RPC запроса
    TIMEOUT = auto()                            # Таймаут запроса

    NET_NOT_RESCANED_OR_ZERO_MODULES = auto()

    # Hardware errors
    TRANSPORT_ERROR = auto()
    HWFRAME_ERROR = auto()
    INVALID_CONFIG = auto()

    FRAME_ERROR = auto()                        # Аппаратная ошибка транзакци
    MODULE_NOT_ANSWER = auto()                  # Модуль не отвечает
    MODULE_SAY_BAD_CRC = auto()                 # При групповой транзакции некоторый модуль обнаружил ошибку CRC
    BAD_CRC = auto()                            # Ошибка CRC
    MODULE_BUSY = auto()                        # Модуль занят
    BYTES_MORE_THEN_NEED = auto()               # Принято байтов от модуля больше, чем ожидалось
    MODULE_PENDING_ERROR = auto()               # Попытка запроса к модулю, который обрабатывает RPC-запрос

    # Unspecified
    SYSTEM_ERROR = auto()                       # Неизвестная системная ошибка

    # Break
    MAX = auto()


class FIO_MODULE_TYPE(IntEnum):
    """Коды модулей."""

    UNKNOWN = 0

    # Аналоговые модули
    AIM720 = auto()
    AIM721 = auto()
    AIM722 = auto()
    AIM723 = auto()
    AIM724 = auto()
    AIM725 = auto()
    AIM726 = auto()
    AIM727 = auto()
    AIM728 = auto()
    AIM729 = auto()
    AIM730 = auto()
    AIM731 = auto()
    AIM732 = auto()
    AIM733 = auto()

    # Цифровые модули
    DIM710 = auto()
    DIM711 = auto()
    DIM712 = auto()
    DIM713 = auto()
    DIM714 = auto()
    DIM715 = auto()
    DIM716 = auto()
    DIM717 = auto()
    DIM718 = auto()
    DIM719 = auto()
    DIM760 = auto()
    DIM761 = auto()
    DIM762 = auto()
    DIM763 = auto()
    DIM764 = auto()

    # Интерфейсные модули
    NIM741 = auto()
    NIM742 = auto()

    # Модули питания
    OM751 = auto()

    # Аналоговые модули
    AIM72503 = auto()
    AIM791 = auto()
    AIM792 = auto()

    # Цифровые модули
    DIM765 = auto()
    DIM766 = auto()

    # FIO-2
    DIM812 = auto()
    DIM813 = auto()
    DIM814 = auto()
    DIM815 = auto()
    DIM816 = auto()
    DIM817 = auto()
    DIM818 = auto()
    DIM819 = auto()
    DIM860 = auto()
    DIM862 = auto()
    DIM873 = auto()
    NIM841 = auto()


class FIO_MODULE_DESC(Structure):
    """Структура параметров описания МВВ."""

    _fields_ = [
        ("Type", c_uint32),              # Тип МВВ
        ("TypeName", c_char * 21),       # Название МВВ. Заканчивающаяся 0 ASCII строка
        ("ProductionCode", c_uint32),    # Уникальный код модели МВВ
        ("SerialNumber", c_uint32),      # Серийный номер изделия
        ("fbusVer", c_uint8 * 2),        # Версия FBUS: major, minor
        ("fwVer", c_uint8 * 2),          # Версия прошивки: major, minor
        ("SpecificRoSize", c_size_t),    # Размер области неизменяемых специфических параметров
        ("SpecificRwSize", c_size_t),    # Размер области изменяемых специфических параметров
        ("InputsSize", c_size_t),        # Размер области входных данных (текущие измерения на входах МВВ)
        ("OutputsSize", c_size_t),       # Размер области выходных данных (текущие значения для актуализации выходов МВВ)
    ]


class FIO_MODULE_GROUP_CONF(Structure):
    """Структура параметров МВВ в операциях группового обмена."""

    _fields_ = [
        ("GroupID", c_uint8),                   # Идентификатор группы. Допустимые значения в области от [0x80 - 0xBF]. Максимальное число групп 64. Значение 0xFF означает что МВВ не участвует в групповом обмене
        ("OutputPacketDataOffset", c_uint16),   # Смещение данных модуля в цепочечном пакете к модулям
        ("OutputModuleDataLength", c_uint8),    # Длина данных модуля в цепочечном пакете к модулям
        ("OutputModuleDataOffset", c_uint8),    # Смещение в области выходных данных модуля, начиная с которого модуль записывает принятую информацию
        ("OutputPacketCRCOffset", c_uint16),    # Смещение поля общего CRC в цепочечном пакете к модулям
        ("InputPacketDataOffset", c_uint16),    # Смещение данных модуля в цепочечном пакете от модулей
        ("InputModuleDataLength", c_uint8),     # Длина данных модуля в цепочечном пакете от модулей
        ("InputModuleDataOffset", c_uint8),     # Смещение в области входных данных модуля, начиная с которого модуль передает информацию
        ("InputPacketCRCOffset", c_uint16),     # Смещение поля общего CRC в цепочечном пакете от модулей
    ]


class FIO_MODULE_COMMON_CONF(Structure):
    """Структура изменяемых общих параметров МВВ."""

    _fields_ = [
        ("ConfigurationID", c_uint32),          # Идентификатор конфигурации МВВ
        ("HostWatchdogInterval", c_uint8),      # Интервал времени (сек), по истечении которого МВВ переведет свои выходы в безопасное состояние при отсутствии запросов со стороны мастера (0 - функция отключена). Использование в текущей версии FIO ограничено
        ("OutputSync", c_uint8),                # Номер синхронизирующего сообщения при получении которого МВВ актуализирует свои выходы. Значение FBUS_UNDEFINED_SYNC_ID (0xFF) означает, что МВВ актуализирует свои выходы асинхронно
        ("InputSync", c_uint8),                 # Номер синхронизирующего сообщения при получении которого МВВ актуализирует свои входы. Значение FBUS_UNDEFINED_SYNC_ID (0xFF) означает, что МВВ актуализирует свои входы асинхронно
        ("GroupConf", FIO_MODULE_GROUP_CONF),   # Параметры конфигурации группового обмена
    ]


class F_FBUS_NIM745_INFO(Structure):
    """Информация об адаптере NIM745."""

    _pack_ = 1
    _fields_ = [
        ("prodcode", c_uint32),     # Production code
        ("sernum", c_uint32),       # Serial number
        ("fw", c_uint8 * 2),        # Firmware (ver, subver)
        ("mac", c_uint8 * 6),       # MAC адрес
    ]


class FBUS_ADAPTER_INFO(Structure):
    """Информация об удаленном адаптере."""

    _fields_ = [
        ("type", c_size_t),                 # Тип устройства
        ("nim745", F_FBUS_NIM745_INFO),     # Информация об удаленном адаптере
    ]
