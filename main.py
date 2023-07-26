from fastapi import FastAPI, Depends
import numpy as np
from pydantic import BaseModel
from typing import Optional
from base import minimize_TLj
import sys
import aioredis

app = FastAPI()


async def get_redis_pool():
    pool = await aioredis.from_url("redis://localhost", minsize=5, maxsize=10)
    try:
        yield pool
    finally:
        pool.close()
        await pool.wait_closed()


class Item(BaseModel):
    name: str
    sensor: str = None
    description: Optional[str] = None


class PersonSensor(BaseModel):
    person_id: str
    heart_sensor: dict = None
    temperature_sensor: dict = None
    blood_pressure_sensor: dict = None


@app.get("/")
async def root():
    A = [2000, 100, 1500]  # List of values for x
    load_of_each_server = [10, 15, 20]
    capacity_of_each_server = [10, 15, 40]
    min_TLj, min_combination = minimize_TLj(A, load_of_each_server, capacity_of_each_server)
    return {"message": min_TLj, "min_com": min_combination}
    # return {"message": "Hello World"}


@app.get("/calculate/")
async def calculate(item: PersonSensor):
    import json

    redis = aioredis.from_url("redis://localhost")

    A = [2000, 100, 1500]  # List of values for x
    total_size = sys.getsizeof(item) / 10

    load_of_each_server = await redis.get("load_of_each_server")
    if load_of_each_server is None:
        load_of_each_server = [10, 15, 20]
    else:
        load_of_each_server=json.loads(load_of_each_server)


    capacity_of_each_server = [50, 150, 100]
    # await redis.set("my-key", "value")
    # value = await redis.get("my-key")
    # print(value)

    await redis.set(item.person_id, total_size)
    value = await redis.get(item.person_id)
    min_TLj, min_combination = minimize_TLj(A, load_of_each_server, capacity_of_each_server)
    min_pos = np.array(list(min_combination)).argmax()
    print(min_pos)
    load_of_each_server[min_pos] += total_size
    # load_of_each_server = [10, 15, 20]

    ss = json.dumps(load_of_each_server)
    await redis.set("load_of_each_server", ss, ex=30)
    print({"message": load_of_each_server, "min_com": min_combination})
    return {"message": min_TLj, "min_com": min_combination}
