import pandas as pd
import numpy as np
import pickle
from fastapi import FastAPI, HTTPException

user_db = {"alice": "wonderland", "bob": "builder", "clementine": "mandarine"}

def get_regression_datas():
    """
    Get the dataframe and preprocess it for the regression model
    """
    with open("../data/final_preprocess_df.csv") as file:
        df = pd.read_csv(file, sep=",", index_col=0, encoding="utf8")

    df.drop(['dateT_E', 'dateT_S', 'decision', 'date_S_MOIS', "label",
             'date_S_JOUR', 'date_S_H', 'date_S_MN', "date", "year", "month", "day", "min", "date_S",
              "date_S_AN", "date_S_MOIS", "delta_time"],
              axis=1, inplace=True)
    df.replace({"T601": 0,
                "T602": 1,
                "M": 0,
                "F": 1,
                "FERIE": 0,
                "travail":1,
                "oui": 1,
                "non": 0},
                inplace=True)
    df.age = pd.qcut(df.age, q=5, labels=False)

    return df

def get_classification_datas():
    """
    Get the data and preprocess it for the classification model
    """
    with open("../data/final_preprocess_df.csv") as file:
        df = pd.read_csv(file, sep=",", index_col=0, encoding="utf8")

    df.drop(['dateT_E', 'dateT_S', 'delta_time', 'date_S_MOIS', "label",
         'date_S_JOUR', 'date_S_H', 'date_S_MN', "date", "year", "month", "day", "min", "date_S",
          "date_S_AN", "date_S_MOIS", "sortie_is_zero", "decision"],
          axis=1, inplace=True)
    df.replace(["Patient admis", "Patient non admis", "Patient décédé"], [0,1,2], inplace=True)
    df.age = pd.qcut(df.age, q=5, labels=False)
    df.replace({"T601": 0,
            "T602": 1,
            "M": 0,
            "F": 1,
            "FERIE": 0,
            "travail":1,
            "oui": 1,
            "non": 0},
            inplace=True)

    return df


def get_classification_model():
    """
    Get the pre-trained classification model
    """
    with open("../models/model_imbalanced_classification_lgbm.pkl", "rb") as file:
        model = pickle.load(file)

    return model


def get_regression_model():
    """
    Get the pre-trained regression model
    """
    with open("../models/model_regression_lgbm.pkl", "rb") as file:
        model = pickle.load(file)

    return model


api = FastAPI(title="My API", description="API for MLE project", version="1.0.1")

@api.get("/")
def get_endpoint():
    """
    This endpoint test if the API is working
    """
    return {"response": "API is working"}

@api.get("/duration/{patient}", name="Get the predicted duration for the choosen patient")
def get_duration(user, password, patient):
    """
    This endpoint returns the predicted time the patient will spend in the service
    """
    if user in user_db.keys():
        if password == user_db[user]:
            df = get_regression_datas()
            model = get_regression_model()
            raw = df.iloc[int(patient)]
            raw = np.array(raw).reshape(-1, df.shape[1])
            y_hat = model.predict(raw)
            y_hat = round(y_hat[0], 4)
            return {f"score": y_hat}
        else:
            raise HTTPException(status_code=404, detail="Wrong password")
    else:
        raise HTTPException(status_code=404, detail="Unknown user")

@api.get("/decision/{patient}", name="Get the predicted decision for the choosen patient")
def get_decision(user, password, patient):
    """
    This endpoint returns the predicted decision for the patient:
    - 0 for admission
    - 1 for non admission
    - 2 for decease
    """
    if user in user_db.keys():
        if password == user_db[user]:
            df = get_classification_datas()
            model = get_classification_model()
            raw = df.iloc[int(patient)]
            raw = np.array(raw).reshape(-1, df.shape[1])
            y_hat = model.predict(raw)
            y_hat = int(y_hat[0])
            return {f"score": y_hat}
        else:
            raise HTTPException(status_code=404, detail="Wrong password")
    else:
        raise HTTPException(status_code=404, detail="Unknown user")
