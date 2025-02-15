import sys
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import datetime
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
poly = PolynomialFeatures(degree=3)
# input_date = sys.stdin
input_date = sys.stdin.readline().strip()
# Load the data
data = pd.read_csv("C:\\Users\\Vasudha\\Downloads\\owid-covid-data 2.csv")
print("hello world")
# Drop unnecessary columns
data.drop(columns=['tests_units', 'iso_code', 'continent'], inplace=True)
col = list(data.columns)
for col_name in col:
    if data[col_name].dtypes == 'object':
        data[col_name] = data[col_name].fillna(data[col_name].mode([0]))
    else:
        data[col_name] = data[col_name].fillna(data[col_name].mean())

# Define a function to perform predictions
def date(value):
     temp = pd.DataFrame()
     temp['date'] = [value]
     temp['date'] = temp['date'].astype('datetime64[ns]')
     p = np.array(temp["date"]).reshape(-1,1)
     P = poly.fit_transform(p)
     return P
def predict_cases(data_country, new_date):
    # # Reset the index
    # data_country.reset_index(drop=True, inplace=True)

    x = np.array(data_country["date"]).reshape(-1, 1)

    # Prepare the target variable (total_cases)
    y = np.array(data_country['total_cases']).reshape(-1, 1)

    # Create polynomial features
    
    X = poly.fit_transform(x)
    lin = LinearRegression()
    lin.fit(X, y)

    
    input_date = pd.to_datetime(new_date)
    # input_date_index = data_country[data_country['date'] == input_date].index[0]
    next_24_hours_index = input_date+datetime.timedelta(days=1)

    next_1_week_index = input_date+datetime.timedelta(weeks=1)

    next_1_month_index = input_date+datetime.timedelta(weeks=4)

    # # Predict the number of cases for the next dates
    next_24_hours_cases = lin.predict(date(next_24_hours_index))[0][0]
    next_1_week_cases = lin.predict(date(next_1_week_index))[0][0]
    next_1_month_cases = lin.predict(date(next_1_month_index))[0][0]

    return next_24_hours_cases, next_1_week_cases, next_1_month_cases


    

# Get the unique countries in the dataset
countries = data['location'].unique()
# Open the text file for writing
file_path = 'sample.txt'

# Remove the file if it already exists
if os.path.exists(file_path):
    os.remove(file_path)
predictions=[]
for country in countries:
    # Select data for the current country
    data_country = data.loc[data['location'].isin([country])]
    data_country = data_country[[ 'date',"location", "total_cases"]]
    data_country['date'] = data_country['date'].astype('datetime64[ns]')

    # Perform predictions for the user-selected date
    next_24_hours_cases, next_1_week_cases, next_1_month_cases = predict_cases(data_country, input_date)

    # Store predictions and country name
    predictions.append((country, next_24_hours_cases, next_1_week_cases, next_1_month_cases))

# Sort predictions in descending order based on total number of cases
predictions_sorted = sorted(predictions, key=lambda x: x[1], reverse=True)

# Write sorted predictions to the file
with open(file_path, 'a') as file:
    for country, next_24_hours_cases, next_1_week_cases, next_1_month_cases in predictions_sorted:
        file.write(f"{country}: \n")
        file.write("Predicted cases for the next 24 hours: {:.2f}\n".format(next_24_hours_cases))
        file.write("Predicted cases for the next 1 week: {:.2f}\n".format(next_1_week_cases))
        file.write("Predicted cases for the next 1 month: {:.2f}\n".format(next_1_month_cases))
        
# with open(file_path, 'a') as file:
#     # Loop through each country
#     for country in countries:
#         # Select data for the current country
#         data_country = data.loc[data['location'].isin([country])]
#         data_country = data_country[[ 'date',"location", "total_cases"]]
#         # data_country.reset_index(drop=True, inplace=True)
#         data_country['date']=data_country['date'].astype('datetime64[ns]')
#         # Perform predictions for the user-selected date
#         # input_date = "2024-09-29"  # User-selected date
#         next_24_hours_cases, next_1_week_cases, next_1_month_cases = predict_cases(data_country, input_date)

#         # Save predictions to a file
#         file.write(f"{country}: \n")
#         file.write("Predicted cases for the next 24 hours: {:.2f}\n".format(next_24_hours_cases))
#         file.write("Predicted cases for the next 1 week: {:.2f}\n".format(next_1_week_cases))
#         file.write("Predicted cases for the next 1 month: {:.2f}\n".format(next_1_month_cases))
