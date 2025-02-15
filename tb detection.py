import pandas as pd
import numpy as np
import sys

def predict(form_data):
    form_data=np.array(form_data)
     # Example input data
    form_data= np.reshape(form_data, (1, -1))
    df = pd.read_csv("C:\\Users\\Vasudha\\Downloads\\sample2.csv")
    df = df.head(5000)
    df = df.drop(['name'], axis=1)
    df=df.drop(['id'],axis=1)
    df = pd.get_dummies(df, columns=['gender'], drop_first=True)
    df.replace({True: 1, False: 0}, inplace=True)

    x = df.drop("tuberculosis yes or no", axis=1)
    y = df["tuberculosis yes or no"]

    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

    from sklearn.preprocessing import StandardScaler
    st_x = StandardScaler()
    x_train = st_x.fit_transform(x_train.values)
    x_test = st_x.transform(x_test.values)

    from sklearn.linear_model import LogisticRegression
    classifier = LogisticRegression()
    classifier.fit(x_train, y_train)
    predictions = classifier.predict(x_test)

    from sklearn.metrics import classification_report, accuracy_score
    # print(classification_report(y_test, predictions, zero_division=1))
    accuracy = accuracy_score(y_test, predictions)
    # print("Accuracy:", accuracy)

    form_data = st_x.transform(form_data)
    # print("Transformed form_data:", form_data)

    prediction = classifier.predict(form_data)
    prediction_str = prediction.astype(str)
    print("Prediction:", prediction_str)

    return prediction_str

input_data_list = []
for line in sys.stdin:
    input_data = line.strip()
    input_data_list.append(input_data)

output_data = predict(input_data_list)
sys.stdout.write('Prediction:'+str(output_data))
sys.stdout.flush()

