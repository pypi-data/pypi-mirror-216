from fastapi import APIRouter,Depends, HTTPException
from starlette.responses import RedirectResponse
from validador_colab.loop import first_block
import asyncio
import datetime

router = APIRouter(
    prefix="/daily_conf",
    tags=["daily_conf"],
    responses={404: {"status": "404", "description": "Not found"}},
)

fut = None
tasks = []


async def calculate_daily_conf(fut, industry_id: int = None, date_start: str = None, date_end: str = None):
    count_produtos_certos, count_produtos_errados = await first_block(industry_id, date_start, date_end)
    fut.set_result((count_produtos_certos, count_produtos_errados))


@router.get("/calculate/{industry_id}")
async def calculate(industry_id: int, date_start: str = None, date_end: str = None):
    global fut
    loop = asyncio.get_event_loop()
    fut = loop.create_future()
    loop.create_task(calculate_daily_conf(fut, industry_id, date_start, date_end))
    return {"status": "calculating"}


@router.get("/{industry_id}")
async def get_daily_conf(industry_id: int, date_start: str = None, date_end: str = None):

    if date_start is None or date_end is None:
        date_start = datetime.datetime.now().strftime("%Y-%m-%d")
        date_end = datetime.datetime.now().strftime("%Y-%m-%d")

    global fut

    if fut:
        await fut
    else:
        return RedirectResponse(url=f'/daily_conf/calculate/{industry_id}?date_start={date_start}&date_end={date_end}')
    count_produtos_certos, count_produtos_errados = fut.result()

    passing_conditions = True

    if count_produtos_certos == 0:
        passing_conditions = False
    if count_produtos_errados > 0:
        passing_conditions = False

    fut = None

    if not passing_conditions:
        return {"data": {"condition": "fail"}}
    else:
        return {"data": {"condition": "pass"}}



