from uvicorn import Config, Server
from time import ctime, time
from sensor import Sensor, DataType
from sys import exit
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
                           vib_sampling_rate * 2,
                           DataType.VIB)

except nidaqmx.errors.DaqError:
    print('잘못된 설정값이 입력 되었습니다. config.ini 파일을 올바르게 수정해 주세요.')
    exit()

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')


async def sensor_loop_temp():
    while True:
        now_time = ctime(time())
        data = await sensor_temp.read(temp_sampling_rate)

        await sio.sleep(1)
        await sio.emit('temp', {'time': now_time, 'data': len(data[0])})


async def sensor_loop_vib():
    while True:
        now_time = ctime(time())
        data = await sensor_vib.read(vib_sampling_rate)

        await sio.sleep(1)
        await sio.emit('vib', {'time': now_time, 'data': len(data[0])})

sensor_task_vib = sio.start_background_task(sensor_loop_vib)
sensor_task_temp = sio.start_background_task(sensor_loop_temp)
socket_app = socketio.ASGIApp(sio)

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
