import pandas as pd
import datetime

arm_plan_date_raw_df = pd.read_csv('data/arm_planir_new_plan_date_2.csv', dtype = str)

arm_plan_df = arm_plan_date_raw_df.loc[:, ['Название ЕО', 'ЕО', 'ТекстПланаПредупрТОРО', 'Название ВРТ', 'ВидЗаказа', 'Заказ', 'КраткийТекст заказа', 'СистСтатус', 'ПользСтатус', 'ПланДатаНачала', 'НовДатаНачала']]



# values = {"НовДатаНачала": '1.1.1970', 'ПланДатаНачала':'1.1.1970'}
# arm_plan_df = arm_plan_df.copy()
# arm_plan_df.fillna(value=values, inplace=True)
arm_plan_df.dropna(subset=['НовДатаНачала', 'ПланДатаНачала'], inplace=True)

#  даты - в даты
date_column_list = ['ПланДатаНачала', 'НовДатаНачала']

for date_column in date_column_list:
  arm_plan_df.loc[:, date_column] = pd.to_datetime(arm_plan_df[date_column], infer_datetime_format=True, format='%d.%m.%Y')
  arm_plan_df.loc[:, date_column] = arm_plan_df.loc[:, date_column].apply(lambda x: datetime.date(x.year, x.month, x.day))
# сортируем по колонке close_event
arm_plan_df.sort_values(['ПланДатаНачала'], inplace=True)


arm_plan_df['ПланДатаНачала_month'] = pd.DatetimeIndex(arm_plan_df['ПланДатаНачала']).month
arm_plan_df['НовДатаНачала_month'] = pd.DatetimeIndex(arm_plan_df['НовДатаНачала']).month

# удаляем строки с задублированными заказами
arm_plan_df.drop_duplicates(subset=['Заказ'])

result_list = []
order_list = []
for index, row in arm_plan_df.iterrows():
  temp_dict = {}
  eo_name = row['Название ЕО']
  eo_code = row['ЕО']
  maint_type = row['Название ВРТ']
  order_type = row['ВидЗаказа']
  order_id =row['Заказ'] 
  order_description = row['КраткийТекст заказа']
  order_system_status = row['СистСтатус']
  order_user_status = row['ПользСтатус']
  order_initial_date = row['ПланДатаНачала']
  order_new_date = row['НовДатаНачала']
  order_initial_date_month = row['ПланДатаНачала_month']
  order_new_date_month = row['НовДатаНачала_month']
  
  # создаем категорию "Запланирован в январе и остался в январе"
  
  if order_initial_date_month != order_new_date_month:
    result_list.append("перенос в другой месяц")
  else:
    result_list.append("без переноса в другой месяц")
arm_plan_df['статус переноса'] = result_list
arm_plan_df.to_csv('data/arm_plan_df.csv')







