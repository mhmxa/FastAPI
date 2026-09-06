import pickle
import pandas as pd

with open("model/model.pkl","rb") as f:
    model=pickle.load(f)

def predict_premium(input: dict):
    input_df = pd.DataFrame([input])
    output = model.predict(input_df)[0]
    return output
