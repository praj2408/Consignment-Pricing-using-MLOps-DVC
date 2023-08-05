import joblib
import numpy as np
import pandas as pd


a = [0,15,0,1,4,25,98,3675.0,37.5,1.5,1,180.0,0,5.88,-290]



model = joblib.load('prediction_service/model/model_rf.pkl')


input_val = np.array(a)



output = model.predict([input_val])


print(output)