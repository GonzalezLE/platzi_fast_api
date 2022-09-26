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
    city : str = Field(
        ...,
        min_length=1,
        max_length=50,
        example = 'puebla'    
        )
    state : str = Field(
        ...,
        min_length=1,
        max_length=50,
        example = 'puebla'    
        )
    country : str = Field(
        ...,
        min_length=1,
        max_length=50,
        example = 'Mexico'
        )

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
    
    class Config:
        schema_extra={
            'example':{
                "first_name": "Luis Enrique",
                "last_name": "Gonzalez Arellano",
                "age": 25,
                "hair_color": "black",
                "is_married": False
            }
        }

# path operation decoretor
@app.get('/')
def home():
    return {"Hello":"world"}


def create_person_example_200():
    return Person(
        first_name = "Luis Enrique2",
        last_name = "Gonzalez Arellano2",
        age = 25,
        hair_color = "red",
        is_married = False
    )

# Request and Response Body
@app.post('/person/new',
          responses={
              200:{
                  'description' : 'This is a example for platzi studens',
                  'content':{'application/json':{'example':create_person_example_200()}}
              }
          })
def create_person(person: Person = Body(...)):
    return person



@app.get('/person/detail')
def show_person(
    name : Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title='Person Name',
        description= "this is the person name, It's between 1 and 50 characters",
        example = "Rocio" # => example
        ),
    age : str = Query(
        ...,
        title='Person Age',
        description = 'This is a person age, it is required',
        example = 25 # => example
        )
):
    return { name:age}



# validaciones Path parameters
@app.get('/person/detail/{person_id}')
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        example=123
        )
):
    return {person_id: 'It exists'}



# validaciones: request body 
@app.put('/person/{person_id}')
def update_person(
    person_id: int = Path(
        ...,
        title = 'person id',
        description = 'This is the person is',
        gt = 0 ,
        example = 123
    ),
    person:Person = Body(...),
    location:Location = Body(...)
):
    result = person.dict()
    result.update(location.dict())
    
    return result
    
    
    