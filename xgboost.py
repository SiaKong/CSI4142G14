import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from  sklearn.metrics import r2_score

df = pd.read_csv('final.csv')

X = df.iloc[:,:-1]
y = df.iloc[:,-1]

X_train, X_test, y_train, y_test = train_test_split(X,y, random_state=100)

xg_reg = XGBRegressor()

xg_reg.fit(X_train, y_train)

y_pred = xg_reg.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

feature_names = X.columns
feature_importance = pd.DataFrame(xg_reg.feature_importances_, index = feature_names).sort_values(0, ascending=False)
