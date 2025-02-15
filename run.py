import sys
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
poly = PolynomialFeatures(degree=3)

data = pd.read_csv("C:\\Users\\Vasudha\\Downloads\\owid-covid-data 2.csv")

# Drop unnecessary columns
data.drop(columns=['tests_units', 'iso_code', 'continent'], inplace=True)
col = list(data.columns)
for col_name in col:
    if data[col_name].dtypes == 'object':
        data[col_name] = data[col_name].fillna(data[col_name].mode([0]))
    else:
        data[col_name] = data[col_name].fillna(data[col_name].mean())
# Define a function to perform predictions
def predict_cases(data_country, new_date):
    # Reset the index
    data_country.reset_index(drop=True, inplace=True)

    x = np.array(data_country.index).reshape(-1, 1)

    # Prepare the target variable (total_cases)
    y = np.array(data_country['total_cases']).reshape(-1, 1)

    # Create polynomial features
    
    X = poly.fit_transform(x)

    # Fit the linear regression model
    lin = LinearRegression()
    lin.fit(X, y)
    input_date_index=input_date
    # Calculate the index values for next 24 hours, 1 week, and 1 month
    next_24_hours_index = input_date_index + 1
    next_1_week_index = input_date_index + 7
    next_1_month_index = input_date_index + 30

    # Predict the number of cases for the next dates
    next_24_hours_cases = lin.predict(poly.transform([[next_24_hours_index]]))[0][0]
    next_1_week_cases = lin.predict(poly.transform([[next_1_week_index]]))[0][0]
    next_1_month_cases = lin.predict(poly.transform([[next_1_month_index]]))[0][0]

    return next_24_hours_cases, next_1_week_cases, next_1_month_cases


# Get the unique countries in the dataset
countries = data['location'].unique()

# Open the text file for writing
with open('sample.txt', 'w') as file:
    # Loop through each country
    for country in countries:
        # Select data for the current country
        data_country = data[data['location'] == country].copy()
        data_country = data_country[[ "location", "total_cases"]]
        data_country.reset_index(drop=True, inplace=True)
        
        # Perform predictions for the user-selected date
        input_date = input("Enter the date (YYYY-MM-DD): ")  # User-selected date
        next_24_hours_cases, next_1_week_cases, next_1_month_cases = predict_cases(data_country, input_date)

        # Save predictions to a file
        file.write(f"{country}: \n")
        file.write("Predicted cases for the next 24 hours: {}\n".format(next_24_hours_cases))
        file.write("Predicted cases for the next 1 week: {}\n".format(next_1_week_cases))
        file.write("Predicted cases for the next 1 month: {}\n".format(next_1_month_cases))
