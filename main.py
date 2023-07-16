from fastapi import FastAPI

from base import minimize_TLj

app = FastAPI()


@app.get("/")
async def root():
    A = [2000, 100, 1500]  # List of values for x
    load_of_each_server = [10, 15, 20]
    capacity_of_each_server = [10, 15, 40]
    min_TLj, min_combination = minimize_TLj(A, load_of_each_server, capacity_of_each_server)
    return {"message": min_TLj,"min_com":min_combination}
    # return {"message": "Hello World"}
