from uvicorn import Config, Server
from sensor import Sensor
from sys import exit

import configparser
import socketio
import nidaqmx
import asyncio

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')


def config_load(file_name: str):
    config = configparser.ConfigParser()
    config.read(file_name)
    sampling_rate = int(config['sensor']['rate'])
    sensor_buffer_size = sampling_rate * 2

    vib_device = config['vib']['device']
    vib_channel_name = vib_device + "/" + config['vib']['channels']

    temp_device = config['temp']['device']
    temp_channel_name = temp_device + "/" + config['temp']['channels']

    return sampling_rate, sensor_buffer_size, vib_channel_name, temp_channel_name


try:
    rate, buffer_size, vib_channel, temp_channel = config_load('config.ini')
    sensor_vib = Sensor.vib(vib_channel, rate, buffer_size)
    sensor_vib.set_sample_count(rate)
    sensor_temp = Sensor.temp(temp_channel, rate, buffer_size)
    sensor_temp.set_sample_count(rate)

except nidaqmx.errors.DaqError:
    print('잘못된 설정값이 입력 되었습니다. config.ini 파일을 올바르게 수정해 주세요.')
    exit()


async def sensor_loop():
    while True:
        await sensor_vib.read(sio, 'vib')
        await sensor_vib.read(sio, 'temp')


async def sensor_loop_vib():
    while True:
        await sensor_vib.read(sio, 'vib')


async def sensor_loop_temp():
    while True:
        await sensor_vib.read(sio, 'temp')


if __name__ == "__main__":
    socket_app = socketio.ASGIApp(sio)
    sensor_task_vib = sio.start_background_task(sensor_loop_vib)
    sensor_task_temp = sio.start_background_task(sensor_loop_temp)
    main_loop = asyncio.get_event_loop()

    socket_config = Config(app=socket_app,
                           host=config['server']['ip'],
                           port=int(config['server']['port']),
                           loop=main_loop)
    socket_server = Server(socket_config)

    main_loop.run_until_complete(socket_server.serve())
    main_loop.run_until_complete(sensor_task_vib)
    main_loop.run_until_complete(sensor_task_temp)
