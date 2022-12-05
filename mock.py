from uvicorn import Config, Server
from fastapi import FastAPI
from time import ctime, time

import socketio
import asyncio
import datetime

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = FastAPI()


async def sensor_loop_vib():
    while True:
        now_time = ctime(time())
        print('vib')
        message = {
            'time': now_time  # TODO 내용추가
        }

        await sio.sleep(1)
        await sio.emit('vib', message)


async def sensor_loop_temp():
    while True:
        now_time = ctime(time())
        print('temp')
        message = {
            'time': now_time  # TODO 내용추가
        }

        await sio.sleep(1)
        await sio.emit('temp', message)


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

    main_loop.run_until_complete(server.serve())
    main_loop.run_until_complete(sensor_task_vib)
    main_loop.run_until_complete(sensor_task_temp)
