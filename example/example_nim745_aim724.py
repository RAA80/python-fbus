#! /usr/bin/env python3

"""Пример использования библиотеки (NIM745 + AIM724)."""

import contextlib
from time import sleep

from fbus.client import FBUS
from fbus.device.aim724 import (AIM724_CJC_MODE, AIM724_CONFIGURATION, AIM724_INPUTS,
                                AIM724_RANGE, AIM724_SCAN_RATE)
from fbus.protocol import FBUS_ADAPTER, FBUS_UNDEFINED_SYNC_ID

if __name__ == "__main__":
    bus = FBUS()

    print(f"fbusGetVersion {bus.fbusGetVersion()}")
    print(f"fbusInitialize {bus.fbusInitialize()}")
    print(f"fbusOpen {bus.fbusOpen(adapter=FBUS_ADAPTER.TCP, port=1)}")
    print(f"fbusRescan {bus.fbusRescan()}")
    print(f"fbusGetNodesCount {bus.fbusGetNodesCount()}")

    descr = bus.fbusGetNodeDescription(net_id=0)    # 0 - первый подключенный модуль
    print(f"fbusGetNodeDescription {descr}")
    print(f"    Type: {descr.Type}")
    print(f"    TypeName: {descr.TypeName}")
    print(f"    ProductionCode: {descr.ProductionCode}")
    print(f"    SerialNumber: {(descr.SerialNumber & 0x00FFFFFF) / 10000}")
    print(f"    fbusVer: {descr.fbusVer[0]}.{descr.fbusVer[1]}")
    print(f"    fwVer: {descr.fwVer[0]}.{descr.fwVer[1]}")
    print(f"    SpecificRoSize: {descr.SpecificRoSize}")
    print(f"    SpecificRwSize: {descr.SpecificRwSize}")
    print(f"    InputsSize: {descr.InputsSize}")
    print(f"    OutputsSize: {descr.OutputsSize}")

    com_par = bus.fbusGetNodeCommonParameters(net_id=0)
    print(f"fbusGetNodeCommonParameters {com_par}")
    print(f"    ConfigurationID: {com_par.ConfigurationID}")
    print(f"    HostWatchdogInterval: {com_par.HostWatchdogInterval}")
    print(f"    OutputSync: {com_par.OutputSync}")
    print(f"    InputSync: {com_par.InputSync}")
    print(f"    GroupConf: {com_par.GroupConf}")
    print(f"        GroupID: {com_par.GroupConf.GroupID}")
    print(f"        OutputPacketDataOffset: {com_par.GroupConf.OutputPacketDataOffset}")
    print(f"        OutputModuleDataLength: {com_par.GroupConf.OutputModuleDataLength}")
    print(f"        OutputModuleDataOffset: {com_par.GroupConf.OutputModuleDataOffset}")
    print(f"        OutputPacketCRCOffset: {com_par.GroupConf.OutputPacketCRCOffset}")
    print(f"        InputPacketDataOffset: {com_par.GroupConf.InputPacketDataOffset}")
    print(f"        InputModuleDataLength: {com_par.GroupConf.InputModuleDataLength}")
    print(f"        InputModuleDataOffset: {com_par.GroupConf.InputModuleDataOffset}")
    print(f"        InputPacketCRCOffset: {com_par.GroupConf.InputPacketCRCOffset}")

    com_par.OutputSync = FBUS_UNDEFINED_SYNC_ID
    com_par.InputSync = FBUS_UNDEFINED_SYNC_ID
    print(f"fbusSetNodeCommonParameters {bus.fbusSetNodeCommonParameters(net_id=0, src=com_par)}")

    spec_par = AIM724_CONFIGURATION()
    spec_par.scanRate = AIM724_SCAN_RATE.MS200
    spec_par.cjc_mode = AIM724_CJC_MODE.INTERNAL_SENSOR
    spec_par.inputRange = AIM724_RANGE.TC_K
    print(f"fbusSetNodeSpecificParameters {bus.fbusSetNodeSpecificParameters(net_id=0, src=spec_par)}")

    spec_par = bus.fbusGetNodeSpecificParameters(net_id=0, dest=AIM724_CONFIGURATION)
    print(f"fbusGetNodeSpecificParameters {spec_par}")
    print(f"    scanRate: {spec_par.scanRate}")
    print(f"    cjc_mode: {spec_par.cjc_mode}")
    print(f"    inputRange: {spec_par.inputRange}")

    print(f"fbusWriteConfig {bus.fbusWriteConfig(net_id=0)}")

    with contextlib.suppress(KeyboardInterrupt):
        while True:
            sleep(1.0)
            # Читаем ответные данные
            inputs = bus.fbusReadInputs(net_id=0, dest=AIM724_INPUTS)
            #print(f"fbusReadInputs {inputs}")
            print(f"    diagnostics: {inputs.diagnostics:08b}, channel0: {inputs.channel0}")
            #print(f"    channel0: {inputs.channel0}")
            #print(f"    channel1: {inputs.channel1}")
            #print(f"    cjcInput: {inputs.cjcInput}")

    print(f"fbusClose {bus.fbusClose()}")
    print(f"fbusDeInitialize {bus.fbusDeInitialize()}")
