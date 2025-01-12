from pymongo.mongo_client import MongoClient
import pandas as pd
import json

#url
uri="mongodb+srv://hello:B3opk4zLjprFqU2O@cluster0.pta0p.mongodb.net/?retryWrites=true&w=majority"

#create new cilent and connect server
client=MongoClient(uri)

DATABASE_NAME="pwskiils"
COLLECTION_NAME="waferfault"

df=pd.read_csv("/Users/mac/Desktop/sensorproject/notebooks/wafer_23012020_041211.csv")

df.head()

df=df.drop("Unnamed: 0", axis=1)

json_record = list(json.loads(df.T.to_json()).values())

client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)
