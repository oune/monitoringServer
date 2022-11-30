from uvicorn import Config, Server
from time import ctime, time
from sensor import Sensor, DataType
from sys import exit
from socketio.asyncio_server import AsyncServer
from scipy import signal

import configparser
import socketio
import nidaqmx
import asyncio

config = configparser.ConfigParser()
config.read('config.ini')

try:
    rate = int(config['sensor']['rate'])
    buffer_size = rate * 2

    vib_device = config['vib']['device']
    vib_channel = vib_device + "/" + config['vib']['channels']

    temp_device = config['temp']['device']
    temp_channel = temp_device + "/" + config['temp']['channels']

    sensor_vib = Sensor.vib(vib_channel, rate, buffer_size)
    sensor_vib.set_sample_count(rate)
    sensor_temp = Sensor.temp(temp_channel, rate, buffer_size)
    sensor_temp.set_sample_count(rate)

except nidaqmx.errors.DaqError:
    print('잘못된 설정값이 입력 되었습니다. config.ini 파일을 올바르게 수정해 주세요.')
    exit()

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')


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

socket_app = socketio.ASGIApp(sio)
# sensor_task = sio.start_background_task(sensor_loop)
sensor_task_vib = sio.start_background_task(sensor_loop_vib)
sensor_task_temp = sio.start_background_task(sensor_loop_temp)

if __name__ == "__main__":
    main_loop = asyncio.get_event_loop()

    socket_config = Config(app=socket_app,
                           host=config['server']['ip'],
                           port=int(config['server']['port']),
                           loop=main_loop)
    socket_server = Server(socket_config)

    main_loop.run_until_complete(socket_server.serve())
    # main_loop.run_until_complete(sensor_task)
    main_loop.run_until_complete(sensor_task_vib)
    main_loop.run_until_complete(sensor_task_temp)
