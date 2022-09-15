from fastapi import FastAPI


app = FastAPI()

# path operation decoretor
@app.get('/')
def home():
    return {"Hello":"world"}

