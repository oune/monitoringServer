# monitoringServer
## 기능
- ni 패키지에서 실시간 데이터 csv 형태로 저장
- 1시간 마다 평균 데이터 통계 저장
- http 통계데이터 조회 api 제공
- socket.io 실시간 데이터, 모델 결과 제공

## directory
```
monitoringServer
├─ .gitignore
├─ clock.py  //시간 관련모듈, 시간 출력, 요일변경확인, 시간변경 확인
├─ csvwriter.py // raw 데이터 저장 모듈, csv 포맷으로 저장
├─ dataController.py // 데이터를 처리
├─ db.py // 통계자료용으로 데이터 저장, 조회
├─ mock.py // 목업서버
├─ model.py // 인공지능 모델
├─ realtimeServer.py // http, sokect.io 서버
├─ realtimeServer.spec
├─ resource
│  ├─ config.ini // 프로젝트 설정파일
│  └─ init_data_path.data // 모델 이상치 계산용
├─ sensor.py // 데이터 수집 모듈
└─ tests // 테스트코드
```

## config.ini
```
[server]
ip = 서버 호스트 아이피
port = 서버 호스트 포트번호
sampling_rate = 실시간 전송 데이터 개

[database]
machine1 = 통계저장 db 경로, 확장자 .db
machine2 = 

[sensor]
rate = 센서 데이터 수집 주기, 해당 샘플링 레이트로 데이터가 저장됨

[temp]
device = 온도 수집 ni 장치 이름
channels = 데이터 획득 채널

[vib]
device = 진동 수집 ni 장치 이름
channels = 데이터 획득 채널

[model]
rate = 모델에서 사용하는 샘플링레이트
batch_size = 모델에서 사용하는 배치크기
score_model = 고장진단 모델 가중치 경로
time_model = 수명 예지모델 가중치 경로
calc_init = 고장진단 스코어 계산기 데이터 경로

[csv]
directory = raw csv 데이터 저장 경로
```

## api
socket.io 실시간 데이터
```
http:/hostip/
```
특정 날자의 통계 데이터 획득
```
http:/hostip/{date}
http:/hostip/2012-1-14
```
특정 구간의 통계 데이터 획득
```
http:/hostip/month/{start}/{end}
http:/hostip/month/2012-1-14/2022-12-20
```

## 빌드
```
pyinstaller realtimeServer.spec
```
