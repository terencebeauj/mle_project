import pandas as pd
import numpy as np
import pickle
from fastapi import FastAPI
import tensorflow

def get_regression_datas():
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
    with open("../models/model_imbalanced_classification_lgbm.pkl", "rb") as file:
        model = pickle.load(file)

    return model


def get_regression_model():
        with open("../models/model_regression_lgbm.pkl", "rb") as file:
            model = pickle.load(file)

        return model


api = FastAPI(title="My API")

@api.get("/duration/{patient}")
def get_duration(patient):
    df = get_regression_datas()
    model = get_regression_model()
    raw = df.iloc[int(patient)]
    raw = np.array(raw).reshape(-1, df.shape[1])
    y_hat = model.predict(raw)
    y_hat = round(y_hat[0], 4)
    return {f"score": y_hat}

@api.get("/decision/{patient}")
def get_decision(patient):
    df = get_classification_datas()
    model = get_classification_model()
    raw = df.iloc[int(patient)]
    raw = np.array(raw).reshape(-1, df.shape[1])
    y_hat = model.predict(raw)
    y_hat = int(y_hat[0])
    return {f"score": y_hat}
