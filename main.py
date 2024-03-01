# Bring in lightweight dependencies

from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle
from typing import List
import json 

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
    
    
# loading all the models when the server started: for quick responses
# with open('./models/60min.pkl', 'rb') as f:
#     model60 = pickle.load(f)
with open('./models/120min.pkl', 'rb') as f:
    model120 = pickle.load(f)
# with open('./models/180min.pkl', 'rb') as f:
#     model180 = pickle.load(f)
# with open('./models/240min.pkl', 'rb') as f:
#     model240 = pickle.load(f)
with open('./models/300min.pkl', 'rb') as f:
    model300 = pickle.load(f)
# with open('./models/360min.pkl', 'rb') as f:
#     model360 = pickle.load(f)

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

@app.post('/')
async def scoring_endpoint(item: List[ScoringItem]):
    print(item)
    
    # normalizing the parameters
    for i in range(len(item)):
        item[i].ITEMP = (item[i].ITEMP - min_max["ITEMP"][0]) / (min_max["ITEMP"][1] - min_max["ITEMP"][0])
        item[i].IRH = (item[i].IRH - min_max["IRH"][0]) / (min_max["IRH"][1] - min_max["IRH"][0])
        item[i].IWS = (item[i].IWS - min_max["IWS"][0]) / (min_max["IWS"][1] - min_max["IWS"][0])
        item[i].IWD = (item[i].IWD - min_max["IWD"][0]) / (min_max["IWD"][1] - min_max["IWD"][0])
        item[i].IPM = (item[i].IPM - min_max["IPM"][0]) / (min_max["IPM"][1] - min_max["IPM"][0])
        item[i].FTEMP = (item[i].FTEMP - min_max["FTEMP"][0]) / (min_max["FTEMP"][1] - min_max["FTEMP"][0])
        item[i].FRH = (item[i].FRH - min_max["FRH"][0]) / (min_max["FRH"][1] - min_max["FRH"][0])
        item[i].FWS = (item[i].FWS - min_max["FWS"][0]) / (min_max["FWS"][1] - min_max["FWS"][0])
        item[i].FWD = (item[i].FWD - min_max["FWD"][0]) / (min_max["FWD"][1] - min_max["FWD"][0])
    
    
    # loading the relevant model
    print("Delay Code: ", item[0].delayCode)       # every input feature has the same delayCode that's why!
    
    if item[0].delayCode == 1:
        # with open('./models/60min.pkl', 'rb') as f:
        #     print("Taking the 60min model")
        #     model = pickle.load(f)
        model = model120
    elif item[0].delayCode == 2:
        # with open('./models/120min.pkl', 'rb') as f:
        #     print("Taking the 120min model")
        #     model = pickle.load(f)
        model = model120
    elif item[0].delayCode == 3:
        # with open('./models/180min.pkl', 'rb') as f:
        #     print("Taking the 180min model")
        #     model = pickle.load(f)
        model = model120
    elif item[0].delayCode == 4:
        # with open('./models/240min.pkl', 'rb') as f:
        #     print("Taking the 240min model")
        #     model = pickle.load(f)
        model = model300
    elif item[0].delayCode == 5:
        # with open('./models/300min.pkl', 'rb') as f:
        #     print("Taking the 300min model")
        #     model = pickle.load(f)
        model = model300
    elif item[0].delayCode == 6:
        # with open('./models/360min.pkl', 'rb') as f:
        #     print("Taking the 360min model")
        #     model = pickle.load(f)
        model = model300
    else:
        jsonData = {
            "fpm_vec": [(item[i].IPM * (min_max['IPM'][1] - min_max['IPM'][0]) + min_max['IPM'][0]) for i in range(len(item))]
        }
        return jsonData # returning the initial concentration as the final concentration.
        
     
    # removing the unnecessary column (delayCode)   
    # df = pd.DataFrame([item.model_dump().values()], columns=item.model_dump().keys())
    
    
    # Convert the list of feature vectors into a list of dictionaries
    data_list = [it.model_dump().values() for it in item]
    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data_list, columns=ScoringItem.__annotations__.keys())
    
    print(df)
    df = df.drop("delayCode", axis=1)
    print(df)
    
    # prediction
    fpm_vec = model.predict(df)
    print("Prediction: {}".format(fpm_vec))
    
    # returning the result
    jsonData =  {
            "fpm_vec": list(fpm_vec)
        }
    print(jsonData)
    
    return jsonData
    


