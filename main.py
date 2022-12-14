#pyhon

from typing import Optional,Dict
from enum import Enum

#PYdantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import SecretStr

#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body,Query,Path,Form

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


class PersonBase(BaseModel):
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
                "is_married": False,
                "password":'This.Password**'
            }
        }


class Person(PersonBase):
    password : str = Field(...,min_length=8,example = 'This.Password**')

# this model is for the response 
class PersonAut(PersonBase):
    pass


class LoginOut(BaseModel):
    username:str = Field(...,max_length=20,example='GonzalezLE')
    message: str = Field(default='Login successful :)', description='Description message')

# path operation decoretor
@app.get(
    path='/',
    status_code=status.HTTP_200_OK
    )
def home():
    return {"Hello":"world"}


def create_person_example_200():
    return Person(
        first_name = "Luis Enrique2",
        last_name = "Gonzalez Arellano2",
        age = 25,
        hair_color = "red",
        is_married = False,
        password = 'This.Password**'
    )

# Request and Response Body
@app.post(
    path= '/person/new',
    response_model = PersonAut,
    status_code=status.HTTP_201_CREATED
    )   
def create_person(person: Person = Body(...)):
    return person



@app.get(
    path= '/person/detail',
    status_code=status.HTTP_200_OK
    )
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
@app.get(
    path = '/person/detail/{person_id}',
    status_code = status.HTTP_200_OK
    )
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        example=123
        )
):
    return {person_id: 'It exists'}



# validaciones: request body 
@app.put(
    path = '/person/{person_id}',
    status_code = status.HTTP_200_OK
    )
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
    
    
@app.post(
    path='/login',
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username : str  = Form(...),password : SecretStr = Form(...)):
    return LoginOut(username=username)