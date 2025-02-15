#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# In[2]:


data = pd.read_csv("C:\\Users\\Vasudha\\Downloads\\covid_data_2020-2021 (1).csv")
data=data.head(60000)


# In[3]:


data.shape


# In[4]:


data.info()


# In[5]:


data.isnull().sum()


# In[6]:


col=list(data.columns)
col


# In[7]:


# for col_name in col:
#     if(data[col_name].dtypes=='int64' or data[col_name].dtypes=='float64'):
#         sns.boxplot(data[col_name])
#         plt.xlabel(col_name)
#         plt.ylabel('count')
#         plt.show()


# In[8]:


data['cough'].value_counts()


# In[9]:


data['test_indication'].value_counts()


# In[10]:


data.dtypes


# In[11]:


data[['test_date','corona_result','age_60_and_above','gender','test_indication']] = data[['test_date','corona_result','age_60_and_above','gender','test_indication']].astype('category')
data['test_date'] = data['test_date'].cat.codes
data['corona_result'] = data['corona_result'].cat.codes
data['age_60_and_above'] = data['age_60_and_above'].cat.codes
data['gender'] = data['gender'].cat.codes
data['test_indication'] = data['test_indication'].cat.codes


# In[12]:


data


# In[13]:


data.dtypes


# In[14]:


from statsmodels.stats.outliers_influence import variance_inflation_factor 
col_list = []
for col in data.columns:
    if (col !='corona_result'):
        col_list.append(col)

X = data[col_list]
vif_data = pd.DataFrame() 
vif_data["feature"] = X.columns 
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))] 
print(vif_data)


# In[15]:


data.drop(columns=['test_indication'],axis=1,inplace=True)
data


# In[16]:


data.columns


# In[17]:


col_list = []
for col in data.columns:
    if (col !='corona_result'):
        col_list.append(col)

X = data[col_list]
vif_data = pd.DataFrame() 
vif_data["feature"] = X.columns 
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))] 
print(vif_data)


# In[18]:


data.drop(columns=['test_date'],axis=1,inplace=True)
data


# In[19]:


col_list = []
for col in data.columns:
    if (col !='corona_result'):
        col_list.append(col)

X = data[col_list]
vif_data = pd.DataFrame() 
vif_data["feature"] = X.columns 
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))] 
print(vif_data)


# In[20]:


x=data.drop("corona_result",axis=1)
y=data["corona_result"]


# In[21]:


from sklearn.model_selection import train_test_split


# In[22]:


x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=1)


# In[23]:


from sklearn.preprocessing import StandardScaler    
st_x= StandardScaler()    
x_train= st_x.fit_transform(x_train.values)    
x_test= st_x.transform(x_test.values) 


# In[24]:


from sklearn.linear_model import LogisticRegression  
classifier= LogisticRegression()  
classifier.fit(x_train, y_train)  


# In[25]:


predictions=classifier.predict(x_test)


# In[26]:


from sklearn.metrics import classification_report


# In[27]:


classification_report(y_test,predictions)


# In[28]:


from sklearn.metrics import confusion_matrix
confusion_matrix(y_test,predictions)


# In[29]:


from sklearn.metrics import accuracy_score
accuracy_score(y_test,predictions)


# In[30]:


data.shape


# In[ ]:


from sklearn import svm

classifier=svm.SVC(kernel='linear',gamma='auto',C=2)
classifier.fit(x_train,y_train)
y_predict=classifier.predict(x_test)


# In[ ]:


from sklearn.metrics import classification_report
classification_report(y_test,y_predict)


# In[ ]:


from sklearn.metrics import confusion_matrix,accuracy_score


# In[ ]:


confusion_matrix(y_test,y_predict)


# In[ ]:


a=accuracy_score(y_test,y_predict)
print(a)











