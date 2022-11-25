from uvicorn import Config, Server
from time import ctime, time
from sensor import Sensor
from sys import exit
from scipy import signal

import configparser
import socketio
import nidaqmx
import asyncio

config = configparser.ConfigParser()
config.read('config.ini')

samplingRate = int(config['sensor']['sampling_rate'])
buffer_size = samplingRate * 8

try:
    sensor_temp = Sensor.of(config['temp']['device'],
                            config['temp']['channels'],
                            samplingRate,
                            buffer_size,
                            config['temp']['datatype'])
    sensor_vib = Sensor.of(config['vib']['device'],
                           config['vib']['channels'],
                           samplingRate,
                           buffer_size,
                           config['vib']['datatype'])

except nidaqmx.errors.DaqError:
    print('잘못된 설정값이 입력 되었습니다. config.ini 파일을 올바르게 수정해 주세요.')
    exit()

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

print(samplingRate)

async def sensor_loop():
    while True:
        now_time = ctime(time())
        temp_data = await sensor_temp.read(samplingRate)
        vib_data = await sensor_vib.read(samplingRate)

        # 리샘플링
        # temp_data = [signal.resample(dataList, numberOfSamples) for dataList in temp_data]
        # vib_data = [signal.resample(dataList, numberOfSamples) for dataList in vib_data]

        print(len(temp_data[0]))
        print(len(vib_data[0]))

        await sio.sleep(1)
        for idx in range(0, len(temp_data)):
            await sio.emit('temp', {'sensor_id': idx, 'time': now_time, 'data': temp_data})
            await sio.sleep(1)

        for idx in range(0, len(temp_data)):
            await sio.emit('vib', {'sensor_id': idx, 'time': now_time, 'data': vib_data})
            await sio.sleep(1)

        # TODO 모델 결과 전송 부분 구현
        # wait sio.emit('model', {'time': now_time, 'mse': output_mse.item(),  'result': model_result})
        # await sio.sleep(1)


sensor_task = sio.start_background_task(sensor_loop)
socket_app = socketio.ASGIApp(sio)

if __name__ == "__main__":
    main_loop = asyncio.get_event_loop()

    socket_config = Config(app=socket_app,
                           host=config['server']['ip'],
                           port=int(config['server']['port']),
                           loop=main_loop)
    socket_server = Server(socket_config)
    # main_loop.run_until_complete(socket_server.serve())
    main_loop.run_until_complete(sensor_task)
