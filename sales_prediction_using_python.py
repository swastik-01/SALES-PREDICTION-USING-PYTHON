# -*- coding: utf-8 -*-
"""SALES PREDICTION USING PYTHON.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1sbE7c6EJYoWyIRexsDePgS8cpMBqjsDA

SALES PREDICTION USING PYTHON

Sales prediction involves forecasting the amount of a product that customers will purchase, taking into
account various factors such as advertising expenditure, target audience segmentation, and advertising
platform selection. In businesses that offer products or services, the role of a Data Scientist is crucial for
predicting future sales. They utilize machine learning techniques in Python to analyse and interpret data,
allowing them to make informed decisions regarding advertising costs. By leveraging these predictions,
businesses can optimize their advertising strategies and maximize sales potential. Let' s embark on the
journey of sales prediction using machine learning in Python.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the datasets
train_df = pd.read_csv('train.csv')
test_df = pd.read_csv('test.csv')
store_df = pd.read_csv('store.csv')

test_df.isnull().sum()

test_df.info()

"""Handling missing values in the test dataset"""

test_df['Open'].fillna(1, inplace=True)

train_df.info()

train_df.isnull().sum()

store_df.info()

store_df.isnull().sum()

"""Handling missing values in the store dataset"""

store_df['CompetitionDistance'].fillna(store_df['CompetitionDistance'].max(), inplace=True)
store_df['CompetitionOpenSinceMonth'].fillna(0, inplace=True)
store_df['CompetitionOpenSinceYear'].fillna(0, inplace=True)
store_df['Promo2SinceWeek'].fillna(0, inplace=True)
store_df['Promo2SinceYear'].fillna(0, inplace=True)
store_df['PromoInterval'].fillna('None', inplace=True)

store_df.isnull().sum()

"""Convert 'Date' columns to datetime objects"""

train_df['Date'] = pd.to_datetime(train_df['Date'])
test_df['Date'] = pd.to_datetime(test_df['Date'])

train_df['Year'] = train_df['Date'].dt.year
train_df['Month'] = train_df['Date'].dt.month
train_df['Day'] = train_df['Date'].dt.day
train_df['WeekOfYear'] = train_df['Date'].dt.isocalendar().week

test_df['Year'] = test_df['Date'].dt.year
test_df['Month'] = test_df['Date'].dt.month
test_df['Day'] = test_df['Date'].dt.day
test_df['WeekOfYear'] = test_df['Date'].dt.isocalendar().week

"""# Merging"""

train_df = pd.merge(train_df, store_df, on='Store', how='left')
test_df = pd.merge(test_df, store_df, on='Store', how='left')

train_df['CompetitionOpenSince'] = (train_df['Year'] - train_df['CompetitionOpenSinceYear']) * 12 + (train_df['Month'] - train_df['CompetitionOpenSinceMonth'])
test_df['CompetitionOpenSince'] = (test_df['Year'] - test_df['CompetitionOpenSinceYear']) * 12 + (test_df['Month'] - test_df['CompetitionOpenSinceMonth'])

"""Promo2 open duration"""

train_df['Promo2OpenSince'] = (train_df['Year'] - train_df['Promo2SinceYear']) * 12 + (train_df['WeekOfYear'] - train_df['Promo2SinceWeek']) / 4.0
test_df['Promo2OpenSince'] = (test_df['Year'] - test_df['Promo2SinceYear']) * 12 + (test_df['WeekOfYear'] - test_df['Promo2SinceWeek']) / 4.0

train_df.fillna(0, inplace=True)
test_df.fillna(0, inplace=True)

train_df.head()

test_df.head()

"""Applying model now"""

from sklearn.model_selection import train_test_split

X = train_df.drop(['Sales', 'Customers', 'Date'], axis=1)
y = train_df['Sales']

# Spliting the data
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

model = RandomForestRegressor(n_estimators=100, random_state=42)

"""One hot encoding"""

X_combined = pd.concat([X_train, X_val])
for col in X_combined.columns:
    if X_combined[col].dtype == 'object':
        print(f"Column '{col}' is non-numeric. Applying one-hot encoding.")
        X_combined = pd.get_dummies(X_combined, columns=[col], drop_first=True)

# Split the combined dataframe back into X_train and X_val
X_train = X_combined.iloc[:X_train.shape[0], :]
X_val = X_combined.iloc[X_train.shape[0]:, :]

model.fit(X_train, y_train)

"""Predicting"""

y_pred = model.predict(X_val)

"""mean_absolute_error"""

mae = mean_absolute_error(y_val, y_pred)
mae

""" test data preparing"""

X_test = test_df.drop(['Id', 'Date'], axis=1)

# Predict sales for the test data
test_predictions = model.predict(X_test)

# Create a DataFrame for the submission
submission = pd.DataFrame({'Id': test_df['Id'], 'Sales': test_predictions})

# Save the submission to a CSV file
submission.to_csv('sales_predictions.csv', index=False)
print("Predictions saved to sales_predictions.csv")