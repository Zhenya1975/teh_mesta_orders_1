import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import linear_model

moto_hours_data_df = pd.read_csv("data/moto_hours_data.csv")
# input_set = moto_hours_data_df.loc[:, ["datetime"]]
## output_set = moto_hours_data_df.loc[:, ["motohours"]

model = linear_model.LinearRegression()

model.fit(moto_hours_data_df[['datetime']].values, moto_hours_data_df.motohours)

prediction = model.predict([[1641427200], [1668124800]])
print(prediction)
print("model.coef: ", model.coef_)
print("model.intercept: ", model.intercept_)



# input_set = moto_hours_data_df.loc[:, ["datetime"]]
# output_set = moto_hours_data_df.loc[:, ["motohours"]]

# X = input_set
# y = output_set

# model = DecisionTreeClassifier()
# model.fit(X.values,y)
# predictions = model.predict([[1641427200], [1668124800]])
# print(predictions)













date_list = ['01.01.2021', '01.01.2022', '01.01.2023', '01.01.2024', '01.01.2025']
date_list = ['01.06.2022', '11.11.2022']
datetime_list =  pd.to_datetime(date_list)
timestamp_list = (datetime_list.astype(int) / 10**9).astype(int)
# print(timestamp_list)
