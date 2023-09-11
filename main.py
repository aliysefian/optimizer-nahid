from fastapi import FastAPI, Depends, HTTPException
import numpy as np
from pydantic import BaseModel
from typing import Optional
from base import minimize_TLj
import sys
import aioredis
from fastapi.encoders import jsonable_encoder
import json
import queue

from utils import compare_lists

pq = queue.PriorityQueue()

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
    time: str = None
    pariority: int = None


# @app.get("/")
# async def root():
#     A = [2000, 100, 1500]  # List of values for x
#     load_of_each_server = [10, 15, 20]
#     capacity_of_each_server = [10, 15, 40]
#     min_TLj, min_combination = minimize_TLj(A, load_of_each_server, capacity_of_each_server)
#     return {"message": min_TLj, "min_com": min_combination}
#     # return {"message": "Hello World"}


@app.get("/calculate/")
async def calculate(item: PersonSensor):
    redis = aioredis.from_url("redis://localhost")
    A = [2000, 100, 1500]  # List of values for x

    total_size = sys.getsizeof(item) / 10

    load_of_each_server = await redis.get("load_of_each_server")
    if load_of_each_server is None:
        load_of_each_server = [0, 0, 0]
    else:
        load_of_each_server = json.loads(load_of_each_server)
    capacity_of_each_server = [150, 150, 200]
    is_queue_call = compare_lists(capacity_of_each_server, load_of_each_server)
    proccess_data = None
    if is_queue_call:
        print("queue call")
        data_exceed = json.dumps(jsonable_encoder(item))
        await enqueue_item(data_exceed, item.pariority)
        return {"message": 0, "min_com": -1, "data": jsonable_encoder(item)}
    else:

        all_queue = await get_all_queue_length()

        if 3 in all_queue.keys() and all_queue[3] > 0:
            proccess_data = await dequeue_item("3")
        elif 2 in all_queue.keys() and all_queue[2] > 0:
            proccess_data = await dequeue_item("2")
        elif 1 in all_queue.keys() and all_queue[1] > 0:
            proccess_data = await dequeue_item("1")
        if proccess_data is not None:
            print("queue start")
            data_exceed = json.dumps(jsonable_encoder(item))
            await enqueue_item(data_exceed, item.pariority)
            total_size = sys.getsizeof(proccess_data) / 10
            proccess_data = json.loads(proccess_data)

    # await redis.set(item.person_id, total_size)
    # value = await redis.get(item.person_id)
    min_TLj, min_combination, cost = minimize_TLj(A, load_of_each_server, capacity_of_each_server)

    min_pos = np.array(list(min_combination)).argmax()
    # print(min_pos)
    load_of_each_server[min_pos] += total_size

    load_server = json.dumps(load_of_each_server)

    await redis.set("load_of_each_server", load_server, ex=15)
    # pq.put

    print({"message": load_of_each_server, "min_com": min_combination})
    if proccess_data is None:
        proccess_data = jsonable_encoder(item)
    else:
        # proccess_data=json.dumps(proccess_data)
        proccess_data = proccess_data
    return {"message": min_TLj, "min_com": str(min_pos), "data": proccess_data}


async def enqueue_item(item: str, priority: int):
    redis = aioredis.from_url("redis://localhost")

    queue_length = await redis.lpush(f"queue_{priority}", item)
    return {"message": f"Item '{item}' enqueued. Queue length: {queue_length}"}


# Dequeue an item from the queue
async def dequeue_item(priority):
    redis = aioredis.from_url("redis://localhost")
    item = await redis.rpop(f"queue_{priority}")
    if item is None:
        return None
    return item


async def get_queue_length(pariorty):
    redis = aioredis.from_url("redis://localhost")
    queue_length = await redis.llen(f"queue_{pariorty}")
    return queue_length


async def get_all_queue_length():
    redis = aioredis.from_url("redis://localhost")
    all_qu = {}
    for item in range(1, 4):
        queue_length = await redis.llen(f"queue_{item}")

        all_qu[item] = queue_length
    return all_qu
