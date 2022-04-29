import pandas as pd
from datetime import timedelta
import initial_values

orders_2023_df = pd.read_csv('py_v2/data_files/заказы на автосамосвалы в 2023 году.csv', dtype = str)

orders_2023_df['Базисный срок начала'] = pd.to_datetime(orders_2023_df['Базисный срок начала'])
print(orders_2023_df.info())
eo_data_df = pd.read_csv('py_v2/data_files/eo_data.csv', dtype = str)
eo_data_df["operation_start_date"] = pd.to_datetime(eo_data_df["operation_start_date"],format='%d.%m.%Y')

print(eo_data_df.info())

orders_eo_data = pd.merge(orders_2023_df, eo_data_df, on = 'eo_code', how = 'left')

print(orders_eo_data.info())
orders_eo_data["operation_start_date"] = eo_list_upload["operation_start_date"].dt.strftime("%d.%m.%Y")
orders_eo_data.to_csv('temp_files/orders_eo_data.csv')
