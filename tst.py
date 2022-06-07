import json

with open('data_pogoda',encoding='utf8') as f:
    templates = json.load(f)

print(templates)
print(list(templates.keys())[1])
print (templates['wind'][2])

import joblib
import pandas as pd
import numpy as np
model_tree_class=joblib.load(r'classification_model.pkl')
model_reg=joblib.load(r'reg_model.pkl')
data_score = pd.read_excel("score_example.xlsx")
data_score[['month','temperature','atmospheric_pressure','humidity','Wind_speed','wind_В','region_Северо-запад', 'hour','snow','rain']]
Y=model_tree_class.predict(data_score)
Y2=np.around(model_reg.predict(data_score), decimals=0)
X=[]
print(Y)
print(Y2)
for count in range(0,6):
    if Y[count]<Y2[count]:
        X.append(Y2[count])
    else:
        X.append(Y[count])
print(X)