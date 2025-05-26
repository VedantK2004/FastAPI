
from pydantic import BaseModel, Field, EmailStr, AnyUrl
from typing import List, Dict, Optional, Annotated

class Patients(BaseModel):
    
    name: str = Field(..., min_length=1, max_length=20)  # non-empty string with length between 1 and 100
    age: int = Field(gt=0, le=120)  # greater than 0 and less than or equal to 120
    email: EmailStr
    linkedin: Optional[AnyUrl] = None
    weight: Annotated[float, Field(gt=0, title= "Patient's Weight.", description="weight of the patient.", examples =[54.3, 45.00], strict=True)] #greater than 0
    married: Annotated[bool, Field(default=None, description="Is the patient married?")]
    allergies: Optional[list[str]] = None
    contact_details: Dict[str, str] 


def insert_patient(patient: Patients):

    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.linkedin)
    print(patient.email)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)

    print("Inserting patient into database")
 
patient_info = {"name": "John Doe", "age": 30, "weight": 70.5,
                "email": "john@email.com",
                "married": True, 
                "contact_details": {"phone":"123-456-7890"}
                }

patient1 = Patients(**patient_info)
insert_patient(patient1)