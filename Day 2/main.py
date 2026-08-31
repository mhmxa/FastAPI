from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
        return data

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
    