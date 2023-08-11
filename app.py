import streamlit as st
import yaml
import pandas as pd
import numpy as np
import joblib
import os



params_path = 'params.yaml'
webapp_root = 'webapp'

model_dir = "D:/Projects/Consignment/prediction_service/model/model_rf.pkl"
model = joblib.load(model_dir)


with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Prediction Service", 
         "")
    ) 





st.title("Consignment Pricing Prediction")

poso_ = st.selectbox(label="PO/SO Number", options=('SCMS', 'SO'))
if poso_ == "SCMS":
    poso = 0
else:
    poso = 1
    
asn_dn_ =st.selectbox(label="ASN/DN Number", options=('Advanced Shipping Notice', 'Delivery Notice'))
if asn_dn_ == "Advanced Shipping Notice":
    asn_dn = 0
elif asn_dn_ == "Delivery Notice":
    asn_dn = 1

country_ = st.selectbox(label="Country", options=('South Africa', 'Nigeria','Côte d Ivoire','Uganda','Vietnam','Zambia','Haiti','Mozambique','Zimbabwe',
                                                  'Tanzania','Tanzania','Rwanda','Congo, DRC','Guyana','Ethiopia','South Sudan','Kenya','Burundi','Namibia',
                                                  'Cameroon','Dominican Republic','Ghana','Sudan','Botswana','Swaziland','Pakistan','Benin','Malawi','Mali',
                                                  'Guatemala','Libya','Angola','Liberia','Sierra Leone','Togo','Senegal','Kyrgyzstan','Burkina Faso','Lesotho',
                                                  'Afghanistan', 'Guinea', 'Belize'))
if country_=="South Africa":
    country = 1402
elif country_=="Nigeria":
    country = 1076
elif country_=="Côte d'Ivoire":
    country = 1027
elif country_=="Uganda":
    country = 737
elif country_=="Vietnam":
    country = 673
elif country_=="Zambia":
    country = 615
elif country_=="Haiti":
    country = 600
elif country_=="Mozambique":
    country = 565
elif country_=="Zimbabwe":
    country = 525
elif country_=="Tanzania":
    country = 487
elif country_=="Rwanda":
    country = 403
elif country_=="Congo, DRC":
    country = 326
elif country_=="Guyana":
    country = 237
elif country_=="Ethiopia":
    country = 172
elif country_=="South Sudan":
    country = 164
elif country_=="Kenya":
    country = 108
elif country_=="Burundi":
    country = 97
elif country_=="Namibia":
    country = 94
elif country_=="Cameroon":
    country = 67
elif country_=="Dominican Republic":
    country = 51
elif country_=="Ghana":
    country = 48
elif country_=="Sudan":
    ountry = 46
elif country_=="Botswana":
    country = 44
elif country_=="Swaziland":
    country = 34
elif country_=="Pakistan":
    country = 15
elif country_=="Benin":
    country = 13
elif country_=="Malawi":
    country = 12
elif country_=="Mali":
    country = 12
elif country_=="Guatemala":
    country = 12
elif country_=="Libya":
    country = 8
elif country_=="Angola":
    country = 7
elif country_=="Liberia":
    country = 6
elif country_=="Sierra Leone":
    country = 4
elif country_=="Togo":
    country = 3
elif country_=="Senegal":
    country = 3
elif country_=="Kyrgyzstan":
    country = 2
elif country_=="Burkina Faso":
    country = 2
elif country_=="Lesotho":
    country = 2
elif country_=="Afghanistan":
    country = 1
elif country_=="Guinea":
    country = 1
elif country_=="Belize":
    country = 1


           
fulfill_via_ =st.selectbox(label="Fulfill Via", options=('Direct Drop', 'From RDC'))
if fulfill_via_=="Direct Drop":
    fulfill_via = 0
elif fulfill_via_=="From RDC":
    fulfill_via = 1
    
    
vender_INCO_term_ = st.selectbox(label="Vender INCO Term", options=('N/A - From RDC', 'EXW', 'DDP','FCA','CIP','Others'))
if vender_INCO_term_ == 'N/A - From RDC':
    vender_INCO_term = 4
elif vender_INCO_term_ == 'EXW':
    vender_INCO_term = 2
elif vender_INCO_term_ == 'DDP':
    vender_INCO_term = 1
elif vender_INCO_term_ == 'FCA':
    vender_INCO_term = 3
elif vender_INCO_term_ == 'CIP':
    vender_INCO_term = 0
elif vender_INCO_term_ == 'Others':
    vender_INCO_term = 5
    
    
sub_classification_ = st.selectbox(label="Sub Classification", options=('Adult', 'Pediatric', 'HIV test','HIV test-Ancillary', 'Malaria', 'ACT'))
if sub_classification_ == 'Adult':
    sub_classification = 1
elif sub_classification_ == 'Pediatric':
    sub_classification = 5
elif sub_classification_ == 'HIV test':
    sub_classification = 2
elif sub_classification_ == 'HIV test-Ancillary':
    sub_classification = 3
elif sub_classification_ == 'Malaria':
    sub_classification = 4
elif sub_classification_ == 'ACT':
    sub_classification = 0


first_line_designation_ = st.selectbox(label="First Line Designation", options=('Yes', 'No'))
if first_line_designation_ == 'Yes':
    first_line_designation = 1
else: first_line_designation = 0

shipment_mode_ = st.selectbox(label="Shipment Mode", options=('Air', 'Truck', 'Air Charter', 'Ocean'))
if shipment_mode_ == 'Air':
    shipment_mode = 0
if shipment_mode_ == 'Truck':
    shipment_mode = 3
if shipment_mode_ == 'Air Charter':
    shipment_mode = 1
if shipment_mode_ == 'Ocean':
    shipment_mode = 2


unit_of_measure_ = st.number_input(label="Unit of Measure (Per Pack)")

line_item_quantity = st.number_input(label="Line Item Quantity")


line_item_insurance_ = st.number_input(label="Line Item Insurance (USD)")

pack_price = st.number_input(label="Pack Price")

unit_price = st.number_input(label="Unit Price")

freight_cost_ = freight_cost_ = st.number_input(label="Freight Cost (USD)")

days_to_process = st.number_input(label="Days to Process")


# a = [0,0,38,0,5,5,240,1000,6.2,0.03,1,4521.5,0,47.04,-930]

data = [poso, asn_dn, country, fulfill_via, vender_INCO_term, sub_classification, first_line_designation,
        shipment_mode, unit_of_measure_, line_item_quantity, line_item_insurance_, pack_price, unit_price,
        freight_cost_, days_to_process]


input_val = np.array(data)

# st.write(poso, asn_dn, country, fulfill_via, vender_INCO_term, sub_classification, first_line_designation,
#         shipment_mode, unit_of_measure_, line_item_quantity, line_item_insurance_, pack_price, unit_price,
#         freight_cost_, days_to_process)

output = model.predict([input_val])


print(output)

st.write(output)