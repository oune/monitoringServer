import configparser


class Serializable:
    def __init__(self, name, filename, config):
        self._name: str = name
        self._filename = filename
        self._config = config

    def save(self):
        self._config[self._name] = {}

        for (key, value) in self.__dict__.items():
            if not str(key).startswith('_'):
                self._config[key] = value

        with open(self._filename, 'w') as configfile:
            self._config.write(configfile)


class Sensor(Serializable):
    def __init__(self, name, filename, config, device, channels, sampling_rate, samples_per_channel, model_type):
        super().__init__(name, filename, config)
        self.device = device
        self.channels = channels
        self.sampling_rate = sampling_rate
        self.samples_per_channel = samples_per_channel
        self.model_type = model_type


class Server(Serializable):
    def __init__(self, name, filename, config, host_ip: str, port: int, database: str):
        super().__init__(name, filename, config)
        self.host_ip: str = host_ip
        self.port: int = port
        self.database: str = database


class Config:
    def __init__(self, filename: str, config, temp: Sensor, vib: Sensor, server: Server):
        self.filename = filename
        self.temp: Sensor = temp
        self.vib: Sensor = vib
        self.server: Server = server


if __name__ == '__main__':
    configparser = configparser.ConfigParser()
    config_file_name = 'config_t.ini'
    sensor_temp = Sensor('temp', config_file_name, configparser, 'Dev0mod1', 'ai0:3', 10, 20, 'temp')
    sensor_vib = Sensor('vib', config_file_name, configparser, 'Dev0mod1', 'ai0:3', 10, 20, 'vib')
    server_config = Server('server', config_file_name, configparser, )

    print(sensor_temp.__dict__)
    print(sensor_vib.__dict__)
