from flask import Flask, render_template, request, jsonify
import os
import yaml
import joblib
import pandas as pd
import numpy as np
from application_logging import logging




params_path = 'params.yaml'
webapp_root = 'webapp'


static_dir = os.path.join(webapp_root, 'static')
template_dir = os.path.join(webapp_root, 'templates')



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# def read_params(config_path):
#     with open(config_path) as yaml_file:
#         config = yaml.safe_load(yaml_file)
#     return config


# def predict(data):
#     try:
#         config = read_params(params_path)
#         model_dir_path = config['webapp_model_dir']
#         model = joblib.load(model_dir_path)
#         prediction = model.predict(data)
#         return prediction
    
#     except Exception as e:
#         logging.info('Error is detected', str(e))
    
    
# logging.info('predective model demonstration')
        




# def api_response(request):
#     try:
#         data = np.array([list(request.json.values())])
#         response = predict(data)
#         response = {"response": response}
#         return jsonify(response)

#     except Exception as e:
#         print(e)
#         error = {"error": "something went wrong"}
#         return error





# @app.route("/predictdata", methods=["GET", "POST"])
# def predict_datapoint():
#     if request.method == 'GET':
#         return render_template("home.html")
#     else:
#         if request.form:
                
#             po_so = int(request.form.get("po_so")),
#             asn_dn = int(request.form.get("asn_dn")),
#             country = int(request.form.get("country")),
#             fulfill_via = int(request.form.get("fulfill_via")),
#             vendor_inco_term = int(request.form.get("vendor_inco_term")),
#             sub_classification = int(request.form.get("sub_classification")),
#             unit_of_measure = int(request.form.get("unit_of_measure_(per_pack)")),
#             line_item_quantity = int(request.form.get("line_item_quantity")),
#             pack_price = int(request.form.get("pack_price")),
#             unit_price = int(request.form.get("unit_price")),
#             first_line_designation = int(request.form.get("first_line_designation")),
#             freight_cost = int(request.form.get("freight_cost_(usd)")),
#             shipment_mode = int(request.form.get("shipment_mode")),
#             line_item_insurance = int(request.form.get("line_item_insurance_(usd)")),
#             days_to_process = int(request.form.get("days_to_process")),

                
#             consignment_data = [po_so, asn_dn,country, fulfill_via, vendor_inco_term, sub_classification, unit_of_measure, line_item_quantity, pack_price,
#                                     unit_price, first_line_designation, freight_cost, shipment_mode, line_item_insurance, days_to_process]
            
#             input_val = np.array(consignment_data)
            
#             response = predict(input_val)
            
#             response = {"response": response}
            
#             return render_template("home.html", response_int=input_val,response=str(response))
    




if __name__ == "__main__":
    app.run()
    
    
    