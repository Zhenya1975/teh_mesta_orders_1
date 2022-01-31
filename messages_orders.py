import pandas as pd
import datetime

def order_data_prepare():
  ############# подготовка данных в таблице заказов
  orders_raw_df = pd.read_csv('data/orders_messages/orders_vern_dump_truck_orders.csv')
  orders_raw_df = orders_raw_df.copy()

  ########### Дату Базисный срока начала - в формат даты #################
  date_column_list = ['БазисСрокНачала']
  for date_column in date_column_list:
      orders_raw_df.loc[:, date_column] = pd.to_datetime(orders_raw_df[date_column], infer_datetime_format=True, format='%m/%d/%Y')
      orders_raw_df.loc[:, date_column] = orders_raw_df.loc[:, date_column].apply(lambda x: datetime.date(x.year, x.month, x.day))
  # сортируем по колонке close_event
  orders_raw_df.sort_values(['БазисСрокНачала'], inplace=True)

  orders_raw_df['basis_start_year'] = pd.DatetimeIndex(orders_raw_df['БазисСрокНачала']).year
  orders_raw_df['basis_start_month'] = pd.DatetimeIndex(orders_raw_df['БазисСрокНачала']).month
  orders_raw_df['basis_start_date'] = pd.DatetimeIndex(orders_raw_df['БазисСрокНачала']).date

  orders_raw_df['basis_start_month_year'] = orders_raw_df['basis_start_month'].astype(str) + '_' + orders_raw_df['basis_start_year'].astype(str)

  #### получаем список с уникальными датами в поле Базисный срок начала
  basis_start_date_unique_list = orders_raw_df['basis_start_date'].unique()
  #### получаем список с уникальными датами в поле basis_start_month_year
  basis_start_date_month_year_unique_list = orders_raw_df['basis_start_month_year'].unique()
  # print(basis_start_date_unique_list)
  return orders_raw_df, basis_start_date_unique_list, basis_start_date_month_year_unique_list

# order_data_prepare()

