import pandas as pd
import datetime

############## ВВЕСТИ ИМЯ ФАЙЛА ВЫГРУЖЕННОГО ИЗ iw_39
uploaded_iw_39_file_name = 'iw_39_verninskoye_dump_tr_excav_02_02_2022.csv'

uploaded_iw_39_file_path = 'data/uploaded_data/' + uploaded_iw_39_file_name

uploaded_iw_39_df_ = pd.read_csv(uploaded_iw_39_file_path, dtype = str)

iw_39_coulumns = ['Заказ','Базисный срок начала', 'Базисный срок конца', 'БЕ',	'Группа плановиков', 'Сообщение',	'Вид заказа', 'Вид работы ТОРО', 'Время ремонтного простоя (Зкз)','Общее время простоя (Зкз)', 'Метка удаления', 'СистСтатус', 'ПользСтатус', 'Системный статус сообщения ТОРО', 'Наименование класса ЕО', 'Краткий текст', 'Единица оборудования', 'Техническое место',	'Название технического места',	'СПП - заголовок заказа']

# uploaded_iw_39_df = uploaded_iw_39_df_.loc[:, iw_39_coulumns].reset_index(drop=True, inplace=True)
uploaded_iw_39_df = uploaded_iw_39_df_[iw_39_coulumns]


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

# меняем текст типа "1_2022" на "январь 2022"
month_name_dict = {1: "январь", 2: "февраль", 3: "март", 4: "апрель", 5: "май", 6: "июнь", 7: "июль", 8: "август", 9: "сентябрь", 10: "октябрь", 11: "ноябрь", 12: "декабрь"} 
uploaded_iw_39_df['basis_start_month_name'] = uploaded_iw_39_df['basis_start_month'].map(month_name_dict)


uploaded_iw_39_df['basis_start_date'] = pd.DatetimeIndex(uploaded_iw_39_df['Базисный срок начала']).date
uploaded_iw_39_df['basis_start_month_year'] = uploaded_iw_39_df['basis_start_month'].astype(str) + '_' + uploaded_iw_39_df['basis_start_year'].astype(str)
uploaded_iw_39_df['basis_start_monthname_year'] = uploaded_iw_39_df['basis_start_month_name'].astype(str) + '_' + uploaded_iw_39_df['basis_start_year'].astype(str)


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
# создаем колонки с именами системных статусов
for status in order_system_status_full_list:
  uploaded_iw_39_df[status] = 0



# Итерируемся по основному датафрему
for index, row in uploaded_iw_39_df.iterrows():
  # получаем значение со списком системных статусов
  order_syst_status = row['order_system_status']
  #записываем в колонки статусов единички
  for status in order_syst_status:
    uploaded_iw_39_df.loc[index, status] = 1


# добавляем колонку с текстом "iw39" по этому статусу можно будет определить запись из iw39
uploaded_iw_39_df.loc[:, 'iw39'] = 'iw39'

# склеиваем с таблицей order_category для описания фильтров по виду заказа
order_category = pd.read_csv('data/catalogues/order_category.csv')
uploaded_iw_39_df_ = pd.merge(uploaded_iw_39_df, order_category, on='Вид заказа', how='left')
uploaded_iw_39_df_['Вид_заказа'] = uploaded_iw_39_df_['Вид заказа'] + "; " + uploaded_iw_39_df_['Вид заказа Описание']

uploaded_iw_39_df = uploaded_iw_39_df_.copy()

# готовим дикт для переименовывания колонок с кодами системных статусов заказов
order_system_status = pd.read_csv('data/catalogues/order_system_status.csv')
order_sytem_status_dict = {}
for index, row in order_system_status.iterrows():
  order_system_status_code = row['Системные статусы']
  order_system_status_description = row['Системные статусы Описание']
  order_sytem_status_dict[order_system_status_code] = order_system_status_code + "; " + order_system_status_description


# переименовываем колонки
uploaded_iw_39_df = uploaded_iw_39_df.rename(columns = order_sytem_status_dict)
# добавляем колонку count
uploaded_iw_39_df['count'] = 1


uploaded_iw_39_df.reset_index(drop=True, inplace=True)
uploaded_iw_39_df.to_csv('data/uploaded_iw_39_df.csv')
# print("len uploaded_iw_39_df", len(uploaded_iw_39_df))


# python orders_df_prep.py