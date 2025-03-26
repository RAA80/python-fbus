#! /usr/bin/env python3

"""Пример использования библиотеки (NIM745 + DIM718)."""

from time import sleep

from fbus.client import FBUS
from fbus.device.dim718 import DIM718_CONFIGURATION, DIM718_INPUTS, DIM718_OUTPUTS
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

    spec_par = DIM718_CONFIGURATION()
    spec_par.initialOutputStates = 0b00000000
    spec_par.outputSafeStates = 0b00000000
    spec_par.mode = 0b0000
    print(f"fbusSetNodeSpecificParameters {bus.fbusSetNodeSpecificParameters(net_id=0, src=spec_par)}")

    spec_par = bus.fbusGetNodeSpecificParameters(net_id=0, dest=DIM718_CONFIGURATION)
    print(f"fbusGetNodeSpecificParameters {spec_par}")
    print(f"    initialOutputStates: {spec_par.initialOutputStates}")
    print(f"    outputSafeStates: {spec_par.outputSafeStates}")
    print(f"    mode: {spec_par.mode}")

    print(f"fbusWriteConfig {bus.fbusWriteConfig(net_id=0)}")

    # Посылаем данные
    outputs = DIM718_OUTPUTS()
    outputs.digitalOutputs = 0b11111111
    outputs.firstHalfDuty_PWM0 = 0
    outputs.secondHalfDuty_PWM0 = 0
    outputs.firstHalfDuty_PWM1 = 0
    outputs.secondHalfDuty_PWM1 = 0
    outputs.firstHalfDuty_PWM2 = 0
    outputs.secondHalfDuty_PWM2 = 0
    outputs.firstHalfDuty_PWM3 = 0
    outputs.secondHalfDuty_PWM3 = 0
    print(f"fbusWriteOutputs {bus.fbusWriteOutputs(net_id=0, src=outputs)}")

    sleep(0.2)

    # Читаем ответные данные
    inputs = bus.fbusReadInputs(net_id=0, dest=DIM718_INPUTS)
    print(f"fbusReadInputs {inputs}")
    print(f"    diagnostics: {inputs.diagnostics:08b}")
    print(f"    channelsStates: {inputs.channelsStates:08b}")
    print(f"    firstHalfDutyState_PWM0: {inputs.firstHalfDutyState_PWM0}")
    print(f"    secondHalfDutyState_PWM0: {inputs.secondHalfDutyState_PWM0}")
    print(f"    firstHalfDutyState_PWM1: {inputs.firstHalfDutyState_PWM1}")
    print(f"    secondHalfDutyState_PWM1: {inputs.secondHalfDutyState_PWM1}")
    print(f"    firstHalfDutyState_PWM2: {inputs.firstHalfDutyState_PWM2}")
    print(f"    secondHalfDutyState_PWM2: {inputs.secondHalfDutyState_PWM2}")
    print(f"    firstHalfDutyState_PWM3: {inputs.firstHalfDutyState_PWM3}")
    print(f"    secondHalfDutyState_PWM3: {inputs.secondHalfDutyState_PWM3}")

    # print(f"fbusBuildGroups {bus.fbusBuildGroups()}")
    # print(f"fbusDeleteGroup {bus.fbusDeleteGroup(group_id=FBUS_GROUP_ID_MIN + 0)}")
    # print(f"fbusReadConfig {bus.fbusReadConfig(net_id=0)}")
    # print(f"fbusSaveConfig {bus.fbusSaveConfig(net_id=0)}")
    # print(f"fbusDeleteAllGroups {bus.fbusDeleteAllGroups()}")
    # print(f"fbusSendSync {bus.fbusSendSync(sync_id=0)}")
    # print(f"fbusReset {bus.fbusReset(net_id=0)}")

    print(f"fbusClose {bus.fbusClose()}")
    print(f"fbusDeInitialize {bus.fbusDeInitialize()}")
