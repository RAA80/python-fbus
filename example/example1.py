#! /usr/bin/env python3

"""Пример использования библиотеки (NIM745 + NIM741)."""

from time import sleep

from fbus.client import FBUS
from fbus.device.nim74x import (NIM74X_CONFIGURATION, NIM74X_INPUTS, NIM74X_OUTPUTS,
                                NIM74X_UART_BAUDRATE, NIM74X_UART_DATABITS,
                                NIM74X_UART_PARITY, NIM74X_UART_STOPBITS)
from fbus.protocol import FBUS_ADAPTER, FBUS_GROUP_ID_MIN, FBUS_UNDEFINED_SYNC_ID

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

    spec_par = NIM74X_CONFIGURATION()
    spec_par.Mode = 0
    spec_par.Baudrate = NIM74X_UART_BAUDRATE.BPS115200
    spec_par.Databits = NIM74X_UART_DATABITS.BITS8
    spec_par.Stopbits = NIM74X_UART_STOPBITS.BIT1
    spec_par.Parity = NIM74X_UART_PARITY.NONE
    print(f"fbusSetNodeSpecificParameters {bus.fbusSetNodeSpecificParameters(net_id=0, src=spec_par)}")

    spec_par = bus.fbusGetNodeSpecificParameters(net_id=0, dest=NIM74X_CONFIGURATION())
    print(f"fbusGetNodeSpecificParameters {spec_par}")
    print(f"    Mode: {spec_par.Mode}")
    print(f"    Baudrate: {spec_par.Baudrate}")
    print(f"    Databits: {spec_par.Databits}")
    print(f"    Stopbits: {spec_par.Stopbits}")
    print(f"    Parity: {spec_par.Parity}")

    print(f"fbusWriteConfig {bus.fbusWriteConfig(net_id=0)}")

    # Посылаем данные в порт
    data = b"#GHHGTMOHHRTO\r"

    outputs = NIM74X_OUTPUTS()
    outputs.Control = 0b00000001
    outputs.tx_Control = 1
    outputs.tx_Length = len(data)
    outputs.tx_Data = tuple(data)
    print(f"fbusWriteOutputs {bus.fbusWriteOutputs(net_id=0, src=outputs)}")

    sleep(0.2)

    # Копируем ответные данные из FIFO приема модуля в область RxData0–31
    outputs = NIM74X_OUTPUTS()
    outputs.Control = 0b00000010
    outputs.tx_Control = 2
    outputs.tx_Length = 0
    outputs.tx_Data = ()
    print(f"fbusWriteOutputs {bus.fbusWriteOutputs(net_id=0, src=outputs)}")

    # Читаем ответные данные из RxData0–31
    inputs = bus.fbusReadInputs(net_id=0, dest=NIM74X_INPUTS())
    print(f"fbusReadInputs {inputs}")
    print(f"    Diagnostics: {inputs.Diagnostics}")
    print(f"    Status: {inputs.Status:016b}")
    print(f"    FIFOLength: {inputs.FIFOLength}")
    print(f"    rx_Control: {inputs.rx_Control}")
    print(f"    rx_Length: {inputs.rx_Length}")
    print(f"    rx_Data: {inputs.rx_Data}")
    print(f"    Ответные данные: {list(inputs.rx_Data[:inputs.rx_Length])}")

    # print(f"fbusBuildGroups {bus.fbusBuildGroups()}")
    # print(f"fbusDeleteGroup {bus.fbusDeleteGroup(group_id=FBUS_GROUP_ID_MIN + 0)}")
    # print(f"fbusReadConfig {bus.fbusReadConfig(net_id=0)}")
    # print(f"fbusSaveConfig {bus.fbusSaveConfig(net_id=0)}")
    # print(f"fbusDeleteAllGroups {bus.fbusDeleteAllGroups()}")
    # print(f"fbusSendSync {bus.fbusSendSync(sync_id=0)}")
    # print(f"fbusReset {bus.fbusReset(net_id=0)}")

    print(f"fbusClose {bus.fbusClose()}")
    print(f"fbusDeInitialize {bus.fbusDeInitialize()}")
