import joblib
import numpy as np
import pandas as pd


a = [0,0,38,0,5,5,240,1000,6.2,0.03,1,4521.5,0,47.04,-930]



model = joblib.load('prediction_service/model/model_rf.pkl')


input_val = np.array(a)



output = model.predict([input_val])


print(output)