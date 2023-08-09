from flask import Flask, render_template, request, jsonify
import os
import yaml
import joblib
import pandas as pd
import numpy as np
from application_logging import logging




app = Flask(__name__)



@app.route('/')
def home():
    return "hello world"









if __name__ == "__main__":
    app.run()