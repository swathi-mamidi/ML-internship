# import numpy as np
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# data = pd.read_csv("C:\\Users\\Vasudha\\Downloads\\owid-covid-data 2.csv")
# data.head()
# data.shape
# temp = data['total_cases']
# data.drop('total_cases',axis= 1, inplace=True)
# data['total_cases'] = temp
# data.columns
# data.isnull().sum()
# data.dtypes
# col = list(data.columns)
# for col_name in col:
#     if data[col_name].dtypes == 'object':
#         data[col_name] = data[col_name].fillna(data[col_name].mode([0]))
#     else:
#         data[col_name] = data[col_name].fillna(data[col_name].mean())
        
# data.isnull().sum()
# data.drop(columns = ['tests_units','iso_code','continent'], inplace =True)
# data.columns
# data.isnull().sum()
# data['location'].value_counts()
# data1 = data.loc[data['location'].isin(['India'])]
# data1
# data1 = data1[[ "location", "total_cases"]]
# data1
# data1 = data1.reset_index()
# data1['index'] = data1.index
# data1
# # plt.plot(data1['total_cases'])
# # plt.show()
# from sklearn.preprocessing import PolynomialFeatures
# from sklearn.linear_model import LinearRegression
# x = np.array(data1["index"]).reshape(-1,1)
# y = np.array(data1["total_cases"]).reshape(-1,1)
# data1.info()
# poly = PolynomialFeatures(degree = 3)
# X = poly.fit_transform(x)
# lin = LinearRegression()
# lin.fit(X,y)
# lin.score(X,y)
# # plt.plot(data1['total_cases'])
# # plt.plot(lin.predict(X), 'r--')
# # plt.show()
# # lin.predict(poly.fit_transform([[265]]))
# # lin.predict(poly.fit_transform([[271]]))
# # lin.predict(poly.fit_transform([[294]]))   
# predictions = []
# new_data_points = [[[265]], [[271]], [[294]]]
# for point in new_data_points:
#     prediction = lin.predict(poly.transform(point))
#     print("hello")
#     predictions.append(prediction[0])

# # Save predictions to a file
# with open('predictions.txt', 'w') as file:
#     for prediction in predictions:
#         file.write(str(prediction) + '\n')
import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# Load the data
data = pd.read_csv("C:\\Users\\Vasudha\\Downloads\\owid-covid-data 2.csv")

# Drop unnecessary columns
data.drop(columns=['tests_units', 'iso_code', 'continent'], inplace=True)
col = list(data.columns)
for col_name in col:
    if data[col_name].dtypes == 'object':
        data[col_name] = data[col_name].fillna(data[col_name].mode([0]))
    else:
        data[col_name] = data[col_name].fillna(data[col_name].mean())
# Get the unique countries in the dataset
countries = data['location'].unique()
countries= list(set(countries))
# Open the text file for writing
with open('predictions.txt', 'w') as file:
    # Loop through each country
    for country in countries:
        print("hello world")
        # Select data for the current country
        # data_country = data[data['location'] == country].copy()
        data_country = data.loc[data['location'].isin([country])]
        # Reset the index
        # data_country.reset_index(drop=True, inplace=True)
        data_country = data_country[[ "location", "total_cases"]]
        data_country = data_country.reset_index()
        data_country['index'] = data_country.index
       

        x = np.array(data_country['index']).reshape(-1, 1)

        # Prepare the target variable (total_cases)
        y = np.array(data_country['total_cases']).reshape(-1, 1)

        # Create polynomial features
        poly = PolynomialFeatures(degree=3)
        X = poly.fit_transform(x)

        # Fit the linear regression model
        lin = LinearRegression()
        lin.fit(X, y)
        predictions = []
        new_data_points = [[[265]]]
        for point in new_data_points:
          prediction = lin.predict(poly.transform(point))
  
          predictions.append(prediction[0])

# # Save predictions to a file
#      
        for prediction in predictions:
         file.write(country+str(prediction) + '\n')
       
