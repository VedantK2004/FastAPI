
from pydantic import BaseModel, Field

class Patients(BaseModel):
    
    name: str
    age: int

def insert_patient(name, age):

    print(name)
    print(age)

    print("Inserting patient into database")

patient_info = {"name": "John Doe", "age": 30}