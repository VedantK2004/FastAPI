
from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse
from typing import Annotated, Optional
import json 

app = FastAPI()

class Patient(BaseModel): 

    id: Annotated[str, Field(..., description="Unique identifier for the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Name of the patient", examples=["John Doe"])]
    city: Annotated[str, Field(..., description="City where the patient resides", examples=["New York"])]
    age: Annotated[int, Field(..., ge=0, lt=120, description="Age of the patient in years", examples=[30])]
    height: Annotated[float, Field(..., gt=0, description="Height of th e patient in meters",)]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kilograms", examples=[60.2])]
 
    @computed_field
    @property
    def bmi(self) -> float:
        """Calculate Body Mass Index (BMI)"""
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        """Determine the health verdict based on BMI"""
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"
        
class PatientUpdate(BaseModel):

    name: Annotated[Optional[str], Field(description=None)]
    city: Annotated[Optional[str], Field(description=None)]
    gender: Annotated[Optional[str], Field(description=None)]
    age: Annotated[Optional[int], Field(ge=0, lt=120, description=None)]
    height: Annotated[Optional[float], Field(gt=0, description=None)]
    weight: Annotated[Optional[float], Field(gt=0, description=None)]

 
def load_data():
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
    data = load_data()
    return data 

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="ID of the patient to view", example ="P001")):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="Field to sort on the basis of height, weight or bmi"), order: str = Query("asc", description="Order of sorting, either 'asc' or 'desc'")):

    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail="Invalid sort field. Choose from height, weight, or bmi.")
    
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Choose either 'asc' or 'desc'.")
    
    data = load_data()
    sorted_data = sorted(data.values(), key=lambda x:  x.get(sort_by, 0), reverse=False if order == "asc" else True)

    return sorted_data

def save_data(data):
    with open("patients.json", 'w') as file:
        json.dump(data, file, indent=4)

@app.post("/create")
def create_patient(patient: Patient):

    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists.")
    
    data[patient.id] = patient.model_dump(exclude={"id"})

    save_data(data)
    
    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})

@app.put("/update/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    existing_patient = data[patient_id]
    
    updated_patient = existing_patient.copy()
    updated_patient.update(patient_update.model_dump(exclude_unset=True))

    data[patient_id] = updated_patient

    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})