from keras.models import load_model
from numpy import where

model = load_model("model")

def getSuicidal(df, threshold=0.999):
    features = df.title.values
    predictions = model.predict(features)
    isSuicidal = list(map(lambda x: "suicidal" if x > threshold else "non-suicidal", list(predictions)))

    indices = where(predictions > threshold)[0]
    df["isSuicidal"] = isSuicidal


    return df, df.url[indices].values
