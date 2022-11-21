import configparser

config = configparser.ConfigParser()


def write(file_name: str):
    config['model'] = {}
    config['model']['device'] = 'cDAQ1Mod1'
    config['model']['channels'] = 'ai0:3'
    config['model']['sampling_rate'] = '51200'
    config['model']['samples_per_channel'] = '51200'
    config['model']['type'] = 'vib'
    config['model']['ip'] = '127.0.0.1'
    config['model']['port'] = '8000'

    with open(file_name, 'w') as configfile:
        config.write(configfile)


def load(file_name: str):
    config.read(file_name)
    device_name = config['model']['device']
    device_channel_name = config['model']['channels']
    sampling_rate = int(config['model']['sampling_rate'])
    samples_per_channel = int(config['model']['samples_per_channel'])
    type = config['model']['type']
    ip = config['model']['ip']
    port = int(config['model']['port'])

    return device_name, device_channel_name, sampling_rate, samples_per_channel, type, ip, port


if __name__ == '__main__':
    import sys
    write(sys.argv[1])
