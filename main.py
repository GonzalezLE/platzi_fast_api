#pyhon
from typing import Optional,Dict

#PYdantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body

app = FastAPI()

#model

class Person(BaseModel):
    first_name : str
    last_name :str
    age :int
    hair_color :Optional[str] = None
    is_married :Optional[bool] = None

# path operation decoretor
@app.get('/')
def home():
    return {"Hello":"world"}

# Request and Response Body
@app.post('person/new')
def create_person(person: Person = Body(...)):
    return person