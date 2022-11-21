import datetime
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/day")
async def read_day(day: datetime.date):
    return {"day": day}


@app.get("/month")
async def read_item(start: datetime.date, end: datetime.date):
    return {'month': str(start) + str(end)}
