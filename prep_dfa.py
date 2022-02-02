import pandas as pd
import datetime

############## ВВЕСТИ ИМЯ ФАЙЛА ВЫГРУЖЕННОГО ИЗ iw_39
uploaded_iw_39_file_name = 'iw_39_verninskoye_dump_tr_excav_02_02_2022.csv'

uploaded_iw_39_file_path = 'data/uploaded_data/' + uploaded_iw_39_file_name

uploaded_iw_39_df = pd.read_csv(uploaded_iw_39_file_path, dtype = str)

# удаляем строки с ETO и НД из колонки Вид работы ТОРО

uploaded_iw_39_df = uploaded_iw_39_df.loc[uploaded_iw_39_df['Вид работы ТОРО'] != 'ЕТО']
uploaded_iw_39_df = uploaded_iw_39_df.loc[uploaded_iw_39_df['Вид работы ТОРО'] != 'НД']
uploaded_iw_39_df.dropna(subset=['Вид работы ТОРО'], inplace=True)

########### Дату Базисный срока начала - в формат даты #################
date_column_list = ['Базисный срок начала']
for date_column in date_column_list:
  uploaded_iw_39_df.loc[:, date_column] = pd.to_datetime(uploaded_iw_39_df[date_column], infer_datetime_format=True, format='%m/%d/%Y')
  uploaded_iw_39_df.loc[:, date_column] = uploaded_iw_39_df.loc[:, date_column].apply(lambda x: datetime.date(x.year, x.month, x.day))
# сортируем по колонке Базисный срок начала
uploaded_iw_39_df.sort_values(['Базисный срок начала'], inplace=True)

uploaded_iw_39_df['basis_start_year'] = pd.DatetimeIndex(uploaded_iw_39_df['Базисный срок начала']).year
uploaded_iw_39_df['basis_start_month'] = pd.DatetimeIndex(uploaded_iw_39_df['Базисный срок начала']).month
uploaded_iw_39_df['basis_start_date'] = pd.DatetimeIndex(uploaded_iw_39_df['Базисный срок начала']).date
uploaded_iw_39_df['basis_start_month_year'] = uploaded_iw_39_df['basis_start_month'].astype(str) + '_' + uploaded_iw_39_df['basis_start_year'].astype(str)

# парсим статусы и укладываем их в листы.
order_system_status = []
order_system_status_full_list = []
for index, row in uploaded_iw_39_df.iterrows():
  order_system_status_string = row['СистСтатус']
  order_user_status_string = row['ПользСтатус']
  message_system_status_string = row['Системный статус сообщения ТОРО']
  
  # делим строку на лист со статусами
  order_system_status_list = order_system_status_string.split(sep = " ")
  # итерируемся по полученному списку
  for order_status in order_system_status_list:
    # если значение статуса еще нет в общем списке статусов, то добавляем его
    if order_status not in order_system_status_full_list:
      order_system_status_full_list.append(order_status)

  order_system_status.append(order_system_status_list)

uploaded_iw_39_df['order_system_status'] = order_system_status

print(order_system_status_full_list)
uploaded_iw_39_df.to_csv('data/uploaded_iw_39_df_delete.csv')



# python prep_dfa.py