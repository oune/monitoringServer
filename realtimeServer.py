from uvicorn import Config, Server
from sensor import Sensor
from sys import exit
from configparser import ConfigParser
from fastapi import FastAPI

import socketio
import nidaqmx
import asyncio
import datetime

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')


def config_load(config: ConfigParser):
    sampling_rate = int(config['sensor']['rate'])
    sensor_buffer_size = sampling_rate * 2

    vib_device = config['vib']['device']
    vib_channel_name = vib_device + "/" + config['vib']['channels']

    temp_device = config['temp']['device']
    temp_channel_name = temp_device + "/" + config['temp']['channels']

    return sampling_rate, sensor_buffer_size, vib_channel_name, temp_channel_name


def init_sensor(sampling_rate: int, sensor_buffer_size: int, vib_channel_name: str, temp_channel_name: str):
    vib = Sensor.vib(vib_channel_name, sampling_rate, sensor_buffer_size)
    temp = Sensor.temp(temp_channel_name, sampling_rate, sensor_buffer_size)
    return vib, temp


def try_sensor_load(config: ConfigParser):
    rate, buffer_size, vib_channel, temp_channel = config_load(config)
    vib, temp = init_sensor(rate, buffer_size, vib_channel, temp_channel)
    return vib, temp


def sensor_load(config: ConfigParser):
    try:
        return try_sensor_load(config)
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
        await sensor_temp.read(sio, 'temp')

app = FastAPI()


@app.get("/month/{date}")
def get_stat_month(date: datetime.date):
    return {'date': date}


@app.get("/{date}")
def get_stat_day(date: datetime.date):
    return {'date': date}


if __name__ == "__main__":
    conf = ConfigParser()
    conf.read('config.ini')
    sensor_vib, sensor_temp = sensor_load(conf)
    socket_app = socketio.ASGIApp(sio, app)
    sensor_task_vib = sio.start_background_task(sensor_loop_vib)
    sensor_task_temp = sio.start_background_task(sensor_loop_temp)
    main_loop = asyncio.get_event_loop()

    socket_config = Config(app=socket_app,
                           host=conf['server']['ip'],
                           port=int(conf['server']['port']),
                           loop=main_loop)
    socket_server = Server(socket_config)

    main_loop.run_until_complete(socket_server.serve())
    main_loop.run_until_complete(sensor_task_vib)
    main_loop.run_until_complete(sensor_task_temp)
