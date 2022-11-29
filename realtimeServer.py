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
    temp_sampling_rate = int(config['temp']['sampling_rate'])
    vib_sampling_rate = int(config['vib']['sampling_rate'])

    sensor_temp = Sensor.of(config['temp']['device'],
                            config['temp']['channels'],
                            temp_sampling_rate,
                            temp_sampling_rate * 2,
                            DataType.TEMP)
    sensor_vib = Sensor.of(config['vib']['device'],
                           config['vib']['channels'],
                           vib_sampling_rate,
                           vib_sampling_rate * 4,
                           DataType.VIB)

except nidaqmx.errors.DaqError:
    print('잘못된 설정값이 입력 되었습니다. config.ini 파일을 올바르게 수정해 주세요.')
    exit()

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')


async def try_read(server: AsyncServer, sensor: Sensor, sampling_rate: int, event_name: str):
    now_time = ctime(time())
    data = await sensor.read(sampling_rate)

    await server.sleep(1)
    await server.emit(event_name, {'time': now_time, 'data': data})


async def read(server: AsyncServer, sensor: Sensor, sampling_rate: int, event_name: str):
    try:
        await try_read(server, sensor, sampling_rate, event_name)
    except Exception as e:
        print(e)
        await server.sleep(1)
        await server.emit('error', '!')


async def sensor_loop_temp():
    while True:
        await read(sio, sensor_temp, temp_sampling_rate, 'temp')


async def sensor_loop_vib():
    while True:
        await read(sio, sensor_vib, vib_sampling_rate, 'vib')


socket_app = socketio.ASGIApp(sio)
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
    main_loop.run_until_complete(sensor_task_vib)
    main_loop.run_until_complete(sensor_task_temp)
