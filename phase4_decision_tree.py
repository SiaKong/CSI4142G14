# -*- coding: utf-8 -*-
"""Phase4_decision_tree.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zw7lkQjnSiUdfuMJ5OWxs2W5ZaqRAChu
"""

import pandas as pd

df = pd.read_csv("final.csv")
df.head()

inputs = df.drop('suicides_per_100k', axis='columns')
target = df['suicides_per_100k']

target

from sklearn.preprocessing import LabelEncoder

from sklearn.model_selection import train_test_split

from sklearn import tree

model = tree.DecisionTreeClassifier()

inputs.gdp_for_year[:10]

inputs.percent_pop_depression[:10]

inputs

print(inputs.dtypes)

inputs.isnull().sum()

from sklearn.tree import DecisionTreeRegressor

from sklearn.model_selection import train_test_split

from sklearn.metrics import mean_squared_error as MSE

X_train, X_test, y_train, y_test = train_test_split(inputs, target, test_size=0.2, random_state=3)

dt = DecisionTreeRegressor(max_depth=4, min_samples_leaf=0.1, random_state=3)

dt.fit(X_train, y_train)

y_pred = dt.predict(X_test)

mse_dt = MSE(y_test, y_pred)

rmse_dt = mse_dt**(1/2)

print(rmse_dt)

tree.plot_tree(dt)

import matplotlib.pyplot as plt

plt.figure(figsize=(20,20))

tree.plot_tree(dt, fontsize=10)

plt.figure(figsize=(12,12))

tree.plot_tree(dt, fontsize=6)

plt.savefig('tree_high_dpi', dpi=100)

from sklearn.tree import export_text

fig = plt.figure(figsize=(25,20))
_ = tree.plot_tree(dt,
                   class_names=True,
                   filled=True,
                   fontsize=12)