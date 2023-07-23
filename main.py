from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from base import minimize_TLj

app = FastAPI()

# Create a Pydantic model to define the structure of the request body
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
    return {"message": min_TLj,"min_com":min_combination}
    # return {"message": "Hello World"}

@app.get("/calculate/")
async def calculate(item: PersonSensor):
    A = [2000, 100, 1500]  # List of values for x
    load_of_each_server = [10, 15, 20]
    capacity_of_each_server = [10, 15, 40]
    min_TLj, min_combination = minimize_TLj(A, load_of_each_server, capacity_of_each_server)
    return {"message": min_TLj,"min_com":min_combination}