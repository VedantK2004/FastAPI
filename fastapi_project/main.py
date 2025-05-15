
from fastapi import FastAPI
import json 

app = FastAPI()

def load_json():
    with open("patients.json", 'r') as file:
        data = json.load(file)
    return data

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functional Patient Management System API built with FastAPI to manage patient records."}

@app.get("/view")
def view():
    data = load_json()
    return data 