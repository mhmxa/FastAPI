from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
        return data

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Name of the Patient", max_length=50)]
    city: Annotated[str, Field(..., description="City of the patient where he lived", max_length=50)]
    age: Annotated[int, Field(..., description="Age of the patient", gt=0, lt=100)]
    gender: Annotated[Literal["male", "female", "others"], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., description="The height of the patient in meters", gt=0)]
    weight: Annotated[float, Field(..., description="The weight of the patient in kilograms", gt=0)]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height**2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'


@app.get("/")
def home():
    return {'message': "Patient Record Management API"}

@app.get("/about")
def about():
    return {'message': "A fully functional API to manage your patient records"}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def get_by_patient_id(patient_id: str = Path(..., description="ID of the patient in the DB", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="patient not found")

@app.get("/sort")
def sorted_data(sort_by: str = Query(..., description="Sort on the basis of height, weight or bmi"), order: str = Query("asc", description="sort in asc or desc order")):
    valid_field = ["height", "weight", "bmi"]
    if sort_by not in valid_field:
        raise HTTPException(status_code=400, detail=f"invalid field, select from {valid_field}")
    
    valid_order = ["asc", "desc"]
    if order not in valid_order:
        raise HTTPException(status_code=400, detail=f"invalid field, select from {valid_order}")

    data = load_data()

    sort_order = True if order == "desc" else False
    sorted_data = sorted(data.values(), key= lambda x: x.get(sort_by, 0), reverse=sort_order)
    return sorted_data    

@app.post("/create")
def create_patient(patient: Patient):
    data  = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    data[patient.id] = patient.model_dump(exclude= ["id"])

    save_data(data)

    return JSONResponse(status_code=201, content={'message': "Patient created successfully"})