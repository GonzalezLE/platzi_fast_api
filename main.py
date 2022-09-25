#pyhon

from typing import Optional,Dict
from enum import Enum

#PYdantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import Body,Query,Path

app = FastAPI()

#model
class HairColor(Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    blonde = 'blonde'
    red = 'red'
    

class Location(BaseModel):
    city : str
    state : str
    country : str

class Person(BaseModel):
    first_name : str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    last_name :str= Field(
        ...,
        min_length=1,
        max_length=50
        )
    age :int = Field(
        ...,
        gt=0,
        le=115
        )
    hair_color :Optional[HairColor] = Field(default=None)
    is_married :Optional[bool] = Field(default=None)

# path operation decoretor
@app.get('/')
def home():
    return {"Hello":"world"}

# Request and Response Body
@app.post('person/new')
def create_person(person: Person = Body(...)):
    return person



@app.get('/person/detail')
def show_person(
    name : Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title='Person Name',
        description= "this is the person name, It's between 1 and 50 characters"
        ),
    age : str = Query(
        ...,
        title='Person Age',
        description = 'This is a person age, it is required'
        )
):
    return { name:age}



# validaciones Path parameters
@app.get('/person/detail/{person_id}')
def show_person(
    person_id: int = Path(...,gt=0)
):
    return {person_id: 'It exists'}



# validaciones: request body 
@app.put('/person/{person_id}')
def update_person(
    person_id: int = Path(
        ...,
        title='person id',
        description='This is the person is',
        gt=0
    ),
    person:Person = Body(...),
    location:Location = Body(...)
):
    result = person.dict()
    result.update(location.dict())
    
    return result
    
    
    