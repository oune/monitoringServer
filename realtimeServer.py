from sensor import Sensor
from time import ctime, time
from sys import exit
from uvicorn import Config, Server
import nidaqmx
import socketio
import config
import asyncio

device_name, device_channel_name, sampling_rate, samples_per_channel, model_type, ip, port = config.load(
    f'config.ini')

try:
    sensor = Sensor.of(device_name,
                       device_channel_name,
                       sampling_rate,
                       samples_per_channel * 2, model_type)
except nidaqmx.errors.DaqError:
    print('잘못된 설정값이 입력 되었습니다. config.ini 파일을 올바르게 수정해 주세요.')
    exit()


async def sensor_loop():
    while True:
        datas = await sensor.read(samples_per_channel, 30.0)
        now_time = ctime(time())

        await sio.sleep(1)
        for idx in range(0, len(datas)):
            await sio.emit('data', {'sensor_id': idx, 'time': now_time})
            await sio.sleep(1)

        # 모델 결과 전송 부분
        # await sio.emit('model', {'time': now_time, 'mse': output_mse.item(),  'result': model_result})
        await sio.sleep(1)


main_loop = asyncio.get_event_loop()

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
sensor_task = sio.start_background_task(sensor_loop)

socket_app = socketio.ASGIApp(sio)
socket_config = Config(socket_app, ip, port, main_loop)
socket_server = Server(socket_config)

if __name__ == "__main__":
    main_loop.run_until_complete(socket_server.serve())
    main_loop.run_until_complete(sensor_task)
