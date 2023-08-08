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
    delayCode: int
    

@app.post('/')
async def scoring_endpoint(item: ScoringItem):
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
    
    # normalizing the parameters
    item.ITEMP = (item.ITEMP - min_max["ITEMP"][0]) / (min_max["ITEMP"][1] - min_max["ITEMP"][0])
    item.IRH = (item.IRH - min_max["IRH"][0]) / (min_max["IRH"][1] - min_max["IRH"][0])
    item.IWS = (item.IWS - min_max["IWS"][0]) / (min_max["IWS"][1] - min_max["IWS"][0])
    item.IWD = (item.IWD - min_max["IWD"][0]) / (min_max["IWD"][1] - min_max["IWD"][0])
    item.IPM = (item.IPM - min_max["IPM"][0]) / (min_max["IPM"][1] - min_max["IPM"][0])
    item.FTEMP = (item.FTEMP - min_max["FTEMP"][0]) / (min_max["FTEMP"][1] - min_max["FTEMP"][0])
    item.FRH = (item.FRH - min_max["FRH"][0]) / (min_max["FRH"][1] - min_max["FRH"][0])
    item.FWS = (item.FWS - min_max["FWS"][0]) / (min_max["FWS"][1] - min_max["FWS"][0])
    item.FWD = (item.FWD - min_max["FWD"][0]) / (min_max["FWD"][1] - min_max["FWD"][0])
    
    
    # loading the relevant model
    print("Delay Code: ", item.delayCode)
    print("DelayCode Type: ", type(item.delayCode))
    if item.delayCode == 1:
        with open('./models/60min.pkl', 'rb') as f:
            print("Taking the 60min model")
            model = pickle.load(f)
    elif item.delayCode == 2:
        with open('./models/120min.pkl', 'rb') as f:
            print("Taking the 120min model")
            model = pickle.load(f)
    elif item.delayCode == 3:
        with open('./models/180min.pkl', 'rb') as f:
            print("Taking the 180min model")
            model = pickle.load(f)
    elif item.delayCode == 4:
        with open('./models/240min.pkl', 'rb') as f:
            print("Taking the 240min model")
            model = pickle.load(f)
    elif item.delayCode == 5:
        with open('./models/300min.pkl', 'rb') as f:
            print("Taking the 300min model")
            model = pickle.load(f)
    elif item.delayCode == 6:
        with open('./models/360min.pkl', 'rb') as f:
            print("Taking the 360min model")
            model = pickle.load(f)
    else:
        return {"fpm": item.IPM} # returning the initial concentration as the final concentration.
        
     
    # removing the unnecessary column (delayCode)   
    df = pd.DataFrame([item.model_dump().values()], columns=item.model_dump().keys())
    print(df)
    df = df.drop("delayCode", axis=1)
    print(df)
    
    # prediction
    yhat = model.predict(df)[0]
    print("Prediction: {}".format(yhat))
    
    # returning the result
    return {"fpm": yhat}


