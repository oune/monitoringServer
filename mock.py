from uvicorn import Config, Server
from fastapi import FastAPI
from time import ctime, time

import random
import socketio
import asyncio
import datetime

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = FastAPI()

data_len = 10


async def sensor_loop_vib():
    print('vib loop start')
    while True:
        now_time = ctime(time())
        message = {'time': now_time,
                   'machine2_left': [random.random() for i in range(0, data_len)],
                   'machine2_right': [random.random() for i in range(0, data_len)],
                   'machine1_left': [random.random() for i in range(0, data_len)],
                   'machine1_right': [random.random() for i in range(0, data_len)]
                   }

        await sio.sleep(1)
        await sio.emit('vib', message)


async def sensor_loop_temp():
    print('temp loop start')
    while True:
        now_time = ctime(time())
        message = {'time': now_time,
                   'machine2': [random.random() * 30 + 20 for i in range(0, data_len)],
                   'machine1': [random.random() * 30 + 20 for i in range(0, data_len)]}

        await sio.sleep(1)
        await sio.emit('temp', message)


async def sensor_loop_model1():
    print('model1 loop start')
    while True:
        message = {
            'name': 'machine1',
            'score': random.random(),
            'remain_time': 355 + random.random(),
            'anomaly': False
        }

        await sio.sleep(4)
        await sio.emit('model', message)


async def sensor_loop_model2():
    print('model2 loop start')
    while True:
        message = {
            'name': 'machine2',
            'score': random.random(),
            'remain_time': 355 + random.random(),
            'anomaly': False
        }

        await sio.sleep(4)
        await sio.emit('model', message)


@app.get("/month/{date}")
def get_stat_month(date: datetime.date):
    return {'date': date}


@app.get("/{date}")
def get_stat_day(date: datetime.date):
    return {'date': date}


if __name__ == "__main__":
    socket_app = socketio.ASGIApp(sio, app)

    main_loop = asyncio.get_event_loop()

    config = Config(app=socket_app,
                    host='127.0.0.1',
                    port=8000,
                    loop=main_loop)
    server = Server(config)

    sensor_task_vib = sio.start_background_task(sensor_loop_vib)
    sensor_task_temp = sio.start_background_task(sensor_loop_temp)
    sensor_task_model1 = sio.start_background_task(sensor_loop_model1)
    sensor_task_model2 = sio.start_background_task(sensor_loop_model2)

    main_loop.run_until_complete(server.serve())
    main_loop.run_until_complete(sensor_task_vib)
    main_loop.run_until_complete(sensor_task_temp)
    main_loop.run_until_complete(sensor_task_model1)
    main_loop.run_until_complete(sensor_task_model2)
