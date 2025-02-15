from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import sys
from flask import jsonify
warnings.filterwarnings('ignore')
# app = Flask(__name__)
input_data_list = []

# @app.route('/symptom/predict', methods=['POST'])
for line in sys.stdin:
    input_data = line.strip()
    input_data_list.append(input_data)

def predict(form_data):
  

    # Perform your machine learning prediction using the form data
    
   form_data=np.array(form_data)
     # Example input data
   form_data= np.reshape(form_data, (1, -1))
   # print(form_data)
   data = pd.read_csv("C:\\Users\\Vasudha\\Downloads\\covid_data_2020-2021 (1).csv")
   data=data.head(60000)

#    data.shape
  
#    data.info()
#    data.isnull().sum()

   col=list(data.columns)
#    col

   data['cough'].value_counts()

   data['test_indication'].value_counts()

#    data.dtypes
   data[['test_date','corona_result','age_60_and_above','gender','test_indication']] = data[['test_date','corona_result','age_60_and_above','gender','test_indication']].astype('category')
   data['test_date'] = data['test_date'].cat.codes
   data['corona_result'] = data['corona_result'].cat.codes
   data['age_60_and_above'] = data['age_60_and_above'].cat.codes
   data['gender'] = data['gender'].cat.codes
   data['test_indication'] = data['test_indication'].cat.codes

   data
#    data.dtypes

   from statsmodels.stats.outliers_influence import variance_inflation_factor 
   col_list = []
   for col in data.columns:
    if (col !='corona_result'):
        col_list.append(col)

   X = data[col_list]
   vif_data = pd.DataFrame() 
   vif_data["feature"] = X.columns 
   vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))] 
#    print(vif_data)
   data.drop(columns=['test_indication'],axis=1,inplace=True)
#    data
#    data.columns
   col_list = []
   for col in data.columns:
    if (col !='corona_result'):
        col_list.append(col)

   X = data[col_list]
   vif_data = pd.DataFrame() 
   vif_data["feature"] = X.columns 
   vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))] 
#    print(vif_data)
   data.drop(columns=['test_date'],axis=1,inplace=True)
   data
   col_list = []
   for col in data.columns:
    if (col !='corona_result'):
        col_list.append(col)

   X = data[col_list]
   vif_data = pd.DataFrame() 
   vif_data["feature"] = X.columns 
   vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))] 
#    print(vif_data)

   x=data.drop("corona_result",axis=1)
   y=data["corona_result"]
   from sklearn.model_selection import train_test_split

   x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=1)

   from sklearn.preprocessing import StandardScaler    
   st_x= StandardScaler()    
   x_train= st_x.fit_transform(x_train.values)    
   x_test= st_x.transform(x_test.values) 

   from sklearn.linear_model import LogisticRegression  
   classifier= LogisticRegression()  
   classifier.fit(x_train, y_train)  
   predictions=classifier.predict(x_test)


   from sklearn.metrics import classification_report

   classification_report(y_test,predictions)

   from sklearn.metrics import confusion_matrix
   confusion_matrix(y_test,predictions)
   from sklearn.metrics import accuracy_score
   a=accuracy_score(y_test,predictions)
   data.shape

#    from sklearn import svm

#    classifier=svm.SVC(kernel='linear',gamma='auto',C=2)
#    classifier.fit(x_train,y_train)
#    y_predict=classifier.predict(x_test)

#    from sklearn.metrics import classification_report
#    classification_report(y_test,y_predict)
#    from sklearn.metrics import confusion_matrix,accuracy_score
#    confusion_matrix(y_test,y_predict)

#    a=accuracy_score(y_test,y_predict)
#    print(a)
   form_data= st_x.transform(form_data)
#    print(form_data) 
   prediction = classifier.predict(form_data)
   prediction_str = prediction.astype(str)

   print("Prediction"+str(prediction_str))
    # Return the prediction as a JSON response
   return prediction_str
output_data = predict(input_data_list)

# Send the output back to Node.js
sys.stdout.write(str(output_data))
sys.stdout.flush()

