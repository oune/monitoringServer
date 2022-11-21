import nidaqmx
import nidaqmx.system
from nidaqmx.constants import *


class Sensor:
    def __init__(self, device):
        system = nidaqmx.system.System.local()
        self.device = system.devices[device]
        self.task = nidaqmx.Task()

    def add_vib_channel(self, channel: str):
        channel_name: str = self.device.name + "/" + channel
        self.task.ai_channels.add_ai_voltage_chan(channel_name)

    def add_temp_channel(self, channel: str):
        channel_name: str = self.device.name + "/" + channel
        self.task.ai_channels.add_ai_rtd_chan(channel_name, min_val=0.0, max_val=100.0, rtd_type=RTDType.PT_3750,
                                              resistance_config=ResistanceConfiguration.THREE_WIRE, current_excit_source=ExcitationSource.INTERNAL, current_excit_val=0.00100)

    def set_timing(self, rate: int, samples_per_channel: int):
        self.task.timing.cfg_samp_clk_timing(rate=rate,
                                             active_edge=nidaqmx.constants.Edge.RISING,
                                             sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                             samps_per_chan=samples_per_channel)

    @classmethod
    def of(clc, device: str, channel: str, rate: int, samples_per_channel: int, type: str):
        if type == 'vib':
            return Sensor.vib(device, channel,
                              rate, samples_per_channel)
        elif type == 'temp':
            return Sensor.temp(device, channel,
                               rate, samples_per_channel)

    @classmethod
    def vib(clc, device: str, channel: str, rate: int, samples_per_channel: int):
        instance = clc(device)
        instance.add_vib_channel(channel)
        instance.set_timing(rate, samples_per_channel)
        return instance

    @classmethod
    def temp(clc, device: str, channel: str, rate: int, samples_per_channel: int):
        instance = clc(device)
        instance.add_temp_channel(channel)
        instance.set_timing(rate, samples_per_channel)
        return instance

    async def read(self, samples_per_channel: int = -1, timeout: int = 10):
        return self.task.read(number_of_samples_per_channel=samples_per_channel, timeout=timeout)
