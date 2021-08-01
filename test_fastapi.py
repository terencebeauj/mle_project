from fastapi import FastAPI

api = FastAPI()

@api.get('/')
def get_index():
    return {"data": "hello world"}
