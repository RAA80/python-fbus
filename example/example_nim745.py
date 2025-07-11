#! /usr/bin/env python3

"""Пример использования библиотеки (NIM745)."""

from fbus.client import FBUS
from fbus.protocol import FBUS_ADAPTER

if __name__ == "__main__":
    bus = FBUS()

    print(f"fbusGetVersion {bus.fbusGetVersion()}")
    print(f"fbusInitialize {bus.fbusInitialize()}")
    print(f"fbusOpen {bus.fbusOpen(adapter=FBUS_ADAPTER.TCP, port=1)}")

    adapter = bus.fbusGetAdapterInfo()
    print(f"fbusGetAdapterInfo: {adapter}")
    print(f"    type: {adapter.type}")
    print(f"    nim745: {adapter.nim745}")
    print(f"        prodcode: {adapter.nim745.prodcode}")
    print(f"        sernum: {(adapter.nim745.sernum & 0x00FFFFFF) / 10000}")
    print(f"        fw: {adapter.nim745.fw[0]}.{adapter.nim745.fw[1]}")
    print(f"        mac: {tuple(adapter.nim745.mac)}")

    print(f"fbusClose {bus.fbusClose()}")
    print(f"fbusDeInitialize {bus.fbusDeInitialize()}")
