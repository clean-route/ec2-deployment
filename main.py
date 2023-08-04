# Bring in lightweight dependencies

from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle

app = FastAPI()

class ScoringItem(BaseModel):
    ITEMP: float
    IRH: float
    IWS: float
    IWD: float
    IPM: float
    FTEMP: float
    FRH: float
    FWS: float
    FWD: float
    

@app.post('/')
async def scoring_endpoint(item: ScoringItem):
    with open('./models/dtu-300min-1723_july_predict.pkl', 'rb') as f:
        model = pickle.load(f)
    print(item)
    min_max = {
        "ITEMP":(0.05, 44.97),
        "IRH": (0.2, 100),
        "IWS":(0.01, 46.91),
        "IWD":(0.01, 360),
        "IPM": (64.11, 525),
        "FTEMP": (0.01, 44.99),
        "FRH": (0.2, 100),
        "FWS": (0.01, 47.71),
        "FWD":(0.01, 360),
    }
    
    item.ITEMP = (item.ITEMP - min_max["ITEMP"][0]) / (min_max["ITEMP"][1] - min_max["ITEMP"][0])
    item.IRH = (item.IRH - min_max["IRH"][0]) / (min_max["IRH"][1] - min_max["IRH"][0])
    item.IWS = (item.IWS - min_max["IWS"][0]) / (min_max["IWS"][1] - min_max["IWS"][0])
    item.IWD = (item.IWD - min_max["IWD"][0]) / (min_max["IWD"][1] - min_max["IWD"][0])
    item.IPM = (item.IPM - min_max["IPM"][0]) / (min_max["IPM"][1] - min_max["IPM"][0])
    item.FTEMP = (item.FTEMP - min_max["FTEMP"][0]) / (min_max["FTEMP"][1] - min_max["FTEMP"][0])
    item.FRH = (item.FRH - min_max["FRH"][0]) / (min_max["FRH"][1] - min_max["FRH"][0])
    item.FWS = (item.FWS - min_max["FWS"][0]) / (min_max["FWS"][1] - min_max["FWS"][0])
    item.FWD = (item.FWD - min_max["FWD"][0]) / (min_max["FWD"][1] - min_max["FWD"][0])
        
    df = pd.DataFrame([item.model_dump().values()], columns=item.model_dump().keys())
    
    print(df)
    yhat = model.predict(df)[0]
    print("Prediction: {}".format(yhat))
    return {"prediction": yhat}


