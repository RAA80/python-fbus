#! /usr/bin/env python3

"""Реализация класса клиента для работы с приборами Fastwel по шине FBUS.
Fastwel FBUS SDK Версия 2.4.
"""

from __future__ import annotations

import os
from ctypes import (CDLL, CFUNCTYPE, POINTER, Structure, byref, c_int, c_size_t,
                    c_uint, c_uint8, c_uint32, c_void_p, cdll, sizeof)
from functools import partial
from platform import architecture
from typing import TYPE_CHECKING, Callable

from fbus.protocol import (FBUS_ADAPTER, FBUS_ADAPTER_INFO, FBUS_RESULT,
                           FIO_MODULE_COMMON_CONF, FIO_MODULE_DESC)

if TYPE_CHECKING:
    from _ctypes import _CData, _PyCFuncPtrType


def _load_lib(arch: str, name: str) -> CDLL:
    return cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), "libs", arch, name))


arch = {"posix": {"32bit": ("linux32", "libfbus.so"),
                  "64bit": ("linux64", "libfbus.so")},
        "nt":    {"32bit": ("win32", "fbuslibw.dll")},
       }[os.name][architecture()[0]]
_lib = _load_lib(*arch)


class FBusError(Exception):
    pass


class FBusDevice(c_void_p):
    """Основной интерфейс для работы с устройствами."""

    _functions_ = {
        "fbusGetVersion": CFUNCTYPE(c_uint, POINTER(c_int), POINTER(c_int)),
        "fbusInitialize": CFUNCTYPE(c_uint),
        "fbusDeInitialize": CFUNCTYPE(c_uint),
        "fbusOpen": CFUNCTYPE(c_uint, c_size_t, POINTER(c_size_t)),
        "fbusClose": CFUNCTYPE(c_uint, c_size_t),
        "fbusRescan": CFUNCTYPE(c_uint, c_size_t, POINTER(c_size_t)),
        "fbusGetNodesCount": CFUNCTYPE(c_uint, c_size_t, POINTER(c_size_t)),
        "fbusGetNodeDescription": CFUNCTYPE(c_uint, c_size_t, c_uint8, POINTER(FIO_MODULE_DESC), c_size_t),
        "fbusReset": CFUNCTYPE(c_uint, c_size_t, c_uint8),
        "fbusSendSync": CFUNCTYPE(c_uint, c_size_t, c_uint8),
        "fbusGetNodeCommonParameters": CFUNCTYPE(c_uint, c_size_t, c_uint8, POINTER(FIO_MODULE_COMMON_CONF), c_size_t),
        "fbusSetNodeCommonParameters": CFUNCTYPE(c_uint, c_size_t, c_uint8, POINTER(FIO_MODULE_COMMON_CONF), c_size_t),
        "fbusGetNodeSpecificParameters": CFUNCTYPE(c_uint, c_size_t, c_uint8, c_void_p, c_size_t, c_size_t),
        "fbusSetNodeSpecificParameters": CFUNCTYPE(c_uint, c_size_t, c_uint8, c_void_p, c_size_t, c_size_t),
        "fbusDeleteGroup": CFUNCTYPE(c_uint, c_size_t, c_uint8),
        "fbusDeleteAllGroups": CFUNCTYPE(c_uint, c_size_t),
        "fbusAssignNodeToGroup": CFUNCTYPE(c_uint, c_size_t, c_uint8, c_uint8, c_size_t, c_size_t, c_size_t, c_size_t),
        "fbusBuildGroups": CFUNCTYPE(c_uint, c_size_t),
        "fbusReadConfig": CFUNCTYPE(c_uint, c_size_t, c_uint8),
        "fbusWriteConfig": CFUNCTYPE(c_uint, c_size_t, c_uint8),
        "fbusSaveConfig": CFUNCTYPE(c_uint, c_size_t, c_uint8),
        "fbusReadInputs": CFUNCTYPE(c_uint, c_size_t, c_uint8, c_void_p, c_size_t, c_size_t),
        "fbusWriteOutputs": CFUNCTYPE(c_uint, c_size_t, c_uint8, c_void_p, c_size_t, c_size_t),
        "fbusProcessGroup": CFUNCTYPE(c_uint, c_size_t, c_uint8),
        "fbusGroupSetNodeOutputs": CFUNCTYPE(c_uint, c_size_t, c_uint8, c_uint8, c_size_t, c_size_t, c_void_p),
        "fbusGroupGetNodeInputs": CFUNCTYPE(c_uint, c_size_t, c_uint8, c_uint8, c_size_t, c_size_t, c_void_p),
        "fbusModuleGetCalibrationData": CFUNCTYPE(c_uint, c_size_t, c_uint8, c_size_t, c_size_t, c_void_p),
        "fbusModuleSetCalibrationData": CFUNCTYPE(c_uint, c_size_t, c_uint8, c_size_t, c_size_t, c_void_p),
        "fbusModuleEnterCalibrationMode": CFUNCTYPE(c_uint, c_size_t, c_uint8),
        "fbusModuleLeaveCalibrationMode": CFUNCTYPE(c_uint, c_size_t, c_uint8),
        "fbusModuleSaveCalibrationData": CFUNCTYPE(c_uint, c_size_t, c_uint8, c_uint32),
        "fbusModuleLoadCalibrationData": CFUNCTYPE(c_uint, c_size_t, c_uint8, c_uint32),
        "fbusGetAdapterInfo": CFUNCTYPE(c_uint, c_size_t, c_void_p, c_size_t),
    }

    def __call__(self, prototype: _PyCFuncPtrType, *arguments: tuple[_CData, ...]) -> bool:
        if result := prototype((self.name, _lib))(*arguments):
            msg = f"{self.name} error {result} ({FBUS_RESULT(result).name})"
            raise FBusError(msg)

        return True

    def __getattr__(self, name: str) -> Callable[..., bool]:    # type: ignore
        self.name = name
        return partial(self.__call__, self._functions_[name])


class FBUS:
    """Класс клиента для работы с приборами Fastwel по шине FBUS."""

    def __init__(self) -> None:
        """Инициализация класса клиента с указанными параметрами."""

        self._fbus = FBusDevice()
        self._hnet = c_size_t()

    def fbusGetVersion(self) -> str:
        """Функция возвращает номер версии ПО FBUS API."""

        major = c_int()
        minor = c_int()

        self._fbus.fbusGetVersion(byref(major), byref(minor))
        return f"{major.value}.{minor.value}"

# Функции инициализации сервиса

    def fbusInitialize(self) -> bool:
        """Инициализировать внутренние структуры сервиса FBUS."""

        return self._fbus.fbusInitialize()

    def fbusDeInitialize(self) -> bool:
        """Завершить работу с сервисом FBUS."""

        return self._fbus.fbusDeInitialize()

# Функции управления сетью

    def fbusOpen(self, adapter: FBUS_ADAPTER, port: int) -> bool:
        """Открыть сеть и получить ее системный идентификатор."""

        if port not in range(1, 101):
            msg = "Invalid port number"
            raise FBusError(msg)

        net_number = {FBUS_ADAPTER.LOCAL: 100 + port - 1 if port > 1 else 0,
                      FBUS_ADAPTER.TCP: port,
                     }[adapter]

        return self._fbus.fbusOpen(c_size_t(net_number), byref(self._hnet))

    def fbusClose(self) -> bool:
        """Закрыть открытую сеть."""

        return self._fbus.fbusClose(self._hnet)

    def fbusRescan(self) -> int:
        """Сканирование сети, назначение обнаруженным модулям идентификаторов и
        считывание текущей конфигурации из модулей.
        """

        nodes = c_size_t()

        self._fbus.fbusRescan(self._hnet, byref(nodes))
        return nodes.value

    def fbusGetNodesCount(self) -> int:
        """Получить количество узлов в сети."""

        nodes = c_size_t()

        self._fbus.fbusGetNodesCount(self._hnet, byref(nodes))
        return nodes.value

    def fbusGetNodeDescription(self, net_id: int) -> FIO_MODULE_DESC:
        """Получить описание модуля."""

        descr = FIO_MODULE_DESC()

        self._fbus.fbusGetNodeDescription(self._hnet, c_uint8(net_id), byref(descr),
                                          sizeof(descr))
        return descr

    def fbusReset(self, net_id: int) -> bool:
        """Сброс одного или всех модулей сети."""

        return self._fbus.fbusReset(self._hnet, c_uint8(net_id))

    def fbusSendSync(self, sync_id: int) -> bool:
        """Послать синхронизирующий пакет."""

        return self._fbus.fbusSendSync(self._hnet, c_uint8(sync_id))

# Функции конфигурирования

    def fbusGetNodeCommonParameters(self, net_id: int) -> FIO_MODULE_COMMON_CONF:
        """Получить значения общих изменяемых параметров модуля из конфигурации
        сети.
        """

        conf = FIO_MODULE_COMMON_CONF()

        self._fbus.fbusGetNodeCommonParameters(self._hnet, c_uint8(net_id),
                                               byref(conf), sizeof(conf))
        return conf

    def fbusSetNodeCommonParameters(self, net_id: int,
                                          src: FIO_MODULE_COMMON_CONF) -> bool:
        """Установить значения общих изменяемых параметров модуля в конфигурации
        сети.
        """

        return self._fbus.fbusSetNodeCommonParameters(self._hnet, c_uint8(net_id),
                                                      byref(src), sizeof(src))

    def fbusGetNodeSpecificParameters(self, net_id: int,
                                            dest: type[Structure]) -> Structure:
        """Получить значения специфических изменяемых параметров модуля из
        конфигурации сети.
        """

        config = dest()
        self._fbus.fbusGetNodeSpecificParameters(self._hnet, c_uint8(net_id),
                                                 byref(config), 0, sizeof(config))
        return config

    def fbusSetNodeSpecificParameters(self, net_id: int, src: Structure) -> bool:
        """Установить значения специфических изменяемых параметров модуля в
        конфигурации сети.
        """

        return self._fbus.fbusSetNodeSpecificParameters(self._hnet, c_uint8(net_id),
                                                        byref(src), 0, sizeof(src))

    def fbusDeleteGroup(self, group_id: int) -> bool:
        """Удалить группу из конфигурации сети."""

        return self._fbus.fbusDeleteGroup(self._hnet, c_uint8(group_id))

    def fbusDeleteAllGroups(self) -> bool:
        """Удалить все группы из конфигурации сети."""

        return self._fbus.fbusDeleteAllGroups(self._hnet)

    def fbusAssignNodeToGroup(self, node_id: int, group_id: int,
                                    input_offset: int, input_length: int,
                                    output_offset: int, output_length: int) -> bool:
        """Присоединить модуль к группе в конфигурации сети."""

        return self._fbus.fbusAssignNodeToGroup(self._hnet, c_uint8(node_id),
                    c_uint8(group_id), c_size_t(input_offset), c_size_t(input_length),
                    c_size_t(output_offset), c_size_t(output_length))

    def fbusBuildGroups(self) -> bool:
        """Инициализировать параметры группового обмена всех модулей в
        конфигурации сети.
        """

        return self._fbus.fbusBuildGroups(self._hnet)

    def fbusReadConfig(self, net_id: int) -> bool:
        """Прочитать значения конфигурационных параметров из модуля (модулей) в
        конфигурацию сети.
        """

        return self._fbus.fbusReadConfig(self._hnet, c_uint8(net_id))

    def fbusWriteConfig(self, net_id: int) -> bool:
        """Записать значения конфигурационных параметров из конфигурации сети в
        модуль (модули).
        """

        return self._fbus.fbusWriteConfig(self._hnet, c_uint8(net_id))

    def fbusSaveConfig(self, net_id: int) -> bool:
        """Сохранить конфигурацию в энергонезависимой памяти модуля (модулей)."""

        return self._fbus.fbusSaveConfig(self._hnet, c_uint8(net_id))

# Функции индивидуальных запросов

    def fbusReadInputs(self, net_id: int, dest: type[Structure]) -> Structure:
        """Чтение области входных данных из модуля."""

        inputs = dest()
        self._fbus.fbusReadInputs(self._hnet, c_uint8(net_id), byref(inputs),
                                  0, sizeof(inputs))
        return inputs

    def fbusWriteOutputs(self, net_id: int, src: Structure) -> bool:
        """Запись в область выходных данных модуля."""

        return self._fbus.fbusWriteOutputs(self._hnet, c_uint8(net_id), byref(src),
                                           0, sizeof(src))

# Функции группового обмена

    def fbusProcessGroup(self, group_id: int) -> bool:
        """Выполнить групповой обмен с модулями."""

        return self._fbus.fbusProcessGroup(self._hnet, c_uint8(group_id))

    def fbusGroupSetNodeOutputs(self, group_id: int, node_id: int,
                                      src: Structure) -> bool:
        """Записать данные выходов модуля в выходной буфер группы."""

        return self._fbus.fbusGroup_setNodeOutputs(self._hnet, c_uint8(group_id),
                                    c_uint8(node_id), 0, sizeof(src), byref(src))

    def fbusGroupGetNodeInputs(self, group_id: int, node_id: int,
                                     dest: type[Structure]) -> Structure:
        """Прочитать данные входов модуля из входного буфера группы."""

        inputs = dest()
        self._fbus.fbusGroup_getNodeInputs(self._hnet, c_uint8(group_id),
                                c_uint8(node_id), 0, sizeof(inputs), byref(inputs))
        return inputs

# Функции калибровки

    def fbusModuleGetCalibrationData(self, net_id: int, offset: int,
                                           length: int, dest: Structure) -> bool:
        """."""

        return self._fbus.fbusModuleGetCalibrationData(self._hnet, c_uint8(net_id),
                                    c_size_t(offset), c_size_t(length), byref(dest))

    def fbusModuleSetCalibrationData(self, net_id: int, offset: int,
                                           length: int, src: Structure) -> bool:
        """."""

        return self._fbus.fbusModuleSetCalibrationData(self._hnet, c_uint8(net_id),
                                    c_size_t(offset), c_size_t(length), byref(src))

    def fbusModuleEnterCalibrationMode(self, net_id: int) -> bool:
        """."""

        return self._fbus.fbusModuleEnterCalibrationMode(self._hnet, c_uint8(net_id))

    def fbusModuleLeaveCalibrationMode(self, net_id: int) -> bool:
        """."""

        return self._fbus.fbusModuleLeaveCalibrationMode(self._hnet, c_uint8(net_id))

    def fbusModuleSaveCalibrationData(self, net_id: int, section_code: int) -> bool:
        """."""

        return self._fbus.fbusModuleSaveCalibrationData(self._hnet, c_uint8(net_id),
                                                        c_uint32(section_code))

    def fbusModuleLoadCalibrationData(self, net_id: int, section_code: int) -> bool:
        """."""

        return self._fbus.fbusModuleLoadCalibrationData(self._hnet, c_uint8(net_id),
                                                        c_uint32(section_code))

# Функции -------

    def fbusGetAdapterInfo(self) -> FBUS_ADAPTER_INFO:
        """Информация об удаленном адаптере."""

        dest = FBUS_ADAPTER_INFO()

        self._fbus.fbusGetAdapterInfo(self._hnet, byref(dest), sizeof(dest))
        return dest


__all__ = ["FBUS"]
