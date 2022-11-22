from fastapi import FastAPI
import datetime

app = FastAPI()


@app.get("/")
async def read():
    return {'hellow': 'test'}


@app.get("/day")
async def read_day(day: datetime.date):
    return {"day": day}


@app.get("/month")
async def read_item(start: datetime.date, end: datetime.date):
    return {'month': str(start) + str(end)}
