
# Consignment-Pricing-Prediction-Using-MLOps-DVC

<div style="text-align: center">
  <img src="https://github.com/praj2408/Consignment-Pricing-using-MLOps-DVC/blob/main/notebook/3554469_8b80_9.jpg" alt="">
</div>

## Project Overview
The Consignment-Price Prediction project aims to develop a machine-learning model that can accurately predict the price of consignment items based on various features and variables. Consignment is a business model in which an individual or business agrees to sell someone else's items on their behalf, typically taking a commission on the final sale price.

This project aims to create a predictive model to help consignment store owners and sellers better understand how to price their items, leading to increased sales and profits. To accomplish this, the project will involve collecting and analyzing data on various features that could impact the sale price of consignment items, such as the item's condition, brand, and rarity, as well as market trends and buyer behaviour.

Once the data is collected, the project will involve cleaning and preprocessing the data, selecting appropriate features, and training and testing various machine learning algorithms to determine which model performs the best. The project will also involve evaluating the accuracy and effectiveness of the final model, and potentially deploying it in a web application or other tool that consignment store owners and sellers can use.

Overall, the Consignment-Price Prediction project has the potential to provide significant value to the consignment industry by helping sellers and store owners make more informed pricing decisions, leading to increased sales and revenue.

## Website
...

## File Structure 
    .
    ├── app_exception           # Custom exception
    ├── application_logging     # custom logger
    ├── data_given              # Given Data
    ├── data                    # raw / processed/ transformed data
    ├── saved_models            # regression model
    ├── report                  # model parameter and pipeline reports.
    ├── notebook                # jupyter notebooks
    ├── src                     # Source files for project implementation
    ├── webapp                  # ml web application
    ├── dvc.yaml                # data version control pipeline.
    ├── app.py                  # Flask backend
    ├── param.yaml              # parameters
    ├── requirements.txt
    └── README.md

## Dataset
The dataset is provided by iNeuron.ai: 
[supply-chain-shipment-pricing-data](https://www.kaggle.com/datasets/divyeshardeshana/supply-chain-shipment-pricing-data)

## MLOps Level 1: ML Pipeline Automation Architecture
The goal of level 1 is to perform continuous training of the model by automating the ML pipeline; this lets you achieve continuous delivery of model prediction service. To automate the process of using new data to retrain models in production, you need to introduce automated data and model validation steps to the pipeline, as well as pipeline triggers and metadata management.

The following figure is a schematic representation of an automated ML pipeline for CT.
![](https://github.com/praj2408/ETE-Protect/blob/main/images/ML%20pipeline%20automation.jpg)

## MLOps Level 2: CI/CD pipeline automation
For a rapid and reliable update of the pipelines in production, you need a robust automated CI/CD system. This automated CI/CD system lets your data scientists rapidly explore new ideas around feature engineering, model architecture, and hyperparameters. They can implement these ideas and automatically build, test, and deploy the new pipeline components to the target environment.

The following diagram shows the implementation of the ML pipeline using CI/CD, which has the characteristics of the automated ML pipelines setup plus the automated CI/CD routines.
![](https://github.com/praj2408/ETE-Protect/blob/main/images/cicd%20pipeline%20automation.jpg)

## Model information
Experiments:

         Model Name              R2 score 
      1. Linear Regression         92.35        
      2. Lasso Regression          91.41
      3. DecisionTree Regression   95.71
      
## Results and analysis

After training the model, we achieved an R-squared value of 0.95 (95% accuracy) on the test data, indicating a high level of predictive power.
## Installation
To run the code, first clone this repository and navigate to the project directory:
```
git clone https://github.com/your-username/repository_name.git
```
Create a virtual environment
```
conda create -p venv python==3.9 -y
conda activate venv/
```
To run this project, you will need Python packages present in the requirements file
```
pip install -r requirements.txt
```

Then, run the `app.py` file to start the Flask web application:
```
python app.py
```
### Tox Commands
Tox aims to automate and standardize testing in Python. It is part of a larger vision of easing the packaging, testing and release process of Python
```bash
[tox]
   envlist=py37
   [testenv]
   deps=pytest
   command=pytest -v
```
### For Rebuilding
``` tox -r ```

### Pytest
```pytest -v```
Used for testing purposes. You can use pip install pytest and pip install tox

### Setup
```pip install -e```

### Package building
``` python setup.py sdist bdist_wheel```

### Hands-on commands for testing
```dvc repro```
```dvc metrics show```

Use logging libraries to make logs

### Testing
while testing your file names must contain the word "test" in it. For ex: xyztest.py or configtest.py

After writing the code, run pytest -v and see all test cases done

### Web Deployment
Streamlit is used to build a website<br>
all the codes are given in app.py

## Contributions
If you have any questions or suggestions regarding the project, please feel free to contact the project maintainer at [gmail](https://mail.google.com/mail/?view=cm&tf=0&to=prajwalgbdr03@gmail.com)

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Run the Project
- Clone the project
- pip install -r requirements.txt
- python app.py Enjoy the project in a local host
