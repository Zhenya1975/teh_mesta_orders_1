import pandas as pd
import datetime

arm_plan_date_raw_df = pd.read_csv('data/arm_planirovshik/arm_01-02_2022_ver3.csv', dtype = str)
# arm_plan_date_raw_df = pd.read_csv('data/arm_planirovshik/arm_01_02_2022.csv', dtype = str)

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

# arm_plan_df.to_csv('data/arm_plan.csv')

result_list = []
order_list = []

# planned_in_jan_and_remaining_in_jan - колонка, в которой будут единички для подсчета количества заказов, запланированных на янваарь и оставшимся в январе
planned_in_jan_and_remaining_in_jan = []
# planned_in_jan_moved_to_somewhere
planned_in_jan_moved_to_somewhere = []

# planned_in_jan_moved_to_feb - запланированные в январе, но переехавшие в февраль
planned_in_jan_moved_to_feb = []

# planned_in_jan_moved_to_mar - запланированные в январе, но переехавшие в март
planned_in_jan_moved_to_mar = []
planned_in_jan_moved_to_apr = []
planned_in_jan_moved_to_may = []
planned_in_jan_moved_to_jun = []
planned_in_jan_moved_to_jul = []
planned_in_jan_moved_to_aug = []
planned_in_jan_moved_to_sep = []
planned_in_jan_moved_to_oct = []
planned_in_jan_moved_to_nov = []
planned_in_jan_moved_to_dec = []


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
  
  # проверяем условие на записи, которые были запланированы на январь и остались в январе
  if order_initial_date_month == 1 and order_initial_date_month == order_new_date_month:
    planned_in_jan_and_remaining_in_jan.append(1)
  else:
    planned_in_jan_and_remaining_in_jan.append(0)
  
  # проверяем условие на записи, которые были запланированы на январь но уехали куда-то в другие месяцы
  if order_initial_date_month == 1 and order_initial_date_month != order_new_date_month:
    planned_in_jan_moved_to_somewhere.append(1)
  else:
    planned_in_jan_moved_to_somewhere.append(0)

  # проверяем условие на записи, которые были запланированы на январь но уехали в февраль
  if order_initial_date_month == 1 and order_new_date_month == 2:
    planned_in_jan_moved_to_feb.append(1)
  else:
    planned_in_jan_moved_to_feb.append(0)

  # проверяем условие на записи, которые были запланированы на январь но уехали в март
  if order_initial_date_month == 1 and order_new_date_month == 3:
    planned_in_jan_moved_to_mar.append(1)
  else:
    planned_in_jan_moved_to_mar.append(0)

  # проверяем условие на записи, которые были запланированы на январь но уехали в апрель
  if order_initial_date_month == 1 and order_new_date_month == 4:
    planned_in_jan_moved_to_apr.append(1)
  else:
    planned_in_jan_moved_to_apr.append(0)
  
  # проверяем условие на записи, которые были запланированы на январь но уехали в май
  if order_initial_date_month == 1 and order_new_date_month == 5:
    planned_in_jan_moved_to_may.append(1)
  else:
    planned_in_jan_moved_to_may.append(0)

  # проверяем условие на записи, которые были запланированы на январь но уехали в июнь
  if order_initial_date_month == 1 and order_new_date_month == 6:
    planned_in_jan_moved_to_jun.append(1)
  else:
    planned_in_jan_moved_to_jun.append(0)
  
  # проверяем условие на записи, которые были запланированы на январь но уехали в июль
  if order_initial_date_month == 1 and order_new_date_month == 7:
    planned_in_jan_moved_to_jul.append(1)
  else:
    planned_in_jan_moved_to_jul.append(0)

  # проверяем условие на записи, которые были запланированы на январь но уехали в август
  if order_initial_date_month == 1 and order_new_date_month == 8:
    planned_in_jan_moved_to_aug.append(1)
  else:
    planned_in_jan_moved_to_aug.append(0)

  # проверяем условие на записи, которые были запланированы на январь но уехали в сентябрь
  if order_initial_date_month == 1 and order_new_date_month == 9:
    planned_in_jan_moved_to_sep.append(1)
  else:
    planned_in_jan_moved_to_sep.append(0)

  # проверяем условие на записи, которые были запланированы на январь но уехали в октябрь
  if order_initial_date_month == 1 and order_new_date_month == 10:
    planned_in_jan_moved_to_oct.append(1)
  else:
    planned_in_jan_moved_to_oct.append(0)

  # проверяем условие на записи, которые были запланированы на январь но уехали в ноябрь
  if order_initial_date_month == 1 and order_new_date_month == 11:
    planned_in_jan_moved_to_nov.append(1)
  else:
    planned_in_jan_moved_to_nov.append(0)

  # проверяем условие на записи, которые были запланированы на январь но уехали в декабрь
  if order_initial_date_month == 1 and order_new_date_month == 12:
    planned_in_jan_moved_to_dec.append(1)
  else:
    planned_in_jan_moved_to_dec.append(0)

arm_plan_df['статус переноса'] = result_list
arm_plan_df['planned_in_jan_and_remaining_in_jan'] = planned_in_jan_and_remaining_in_jan
arm_plan_df['planned_in_jan_moved_to_somewhere'] = planned_in_jan_moved_to_somewhere
arm_plan_df['planned_in_jan_moved_to_feb'] = planned_in_jan_moved_to_feb
arm_plan_df['planned_in_jan_moved_to_mar'] = planned_in_jan_moved_to_mar
arm_plan_df['planned_in_jan_moved_to_apr'] = planned_in_jan_moved_to_apr
arm_plan_df['planned_in_jan_moved_to_may'] = planned_in_jan_moved_to_may
arm_plan_df['planned_in_jan_moved_to_jun'] = planned_in_jan_moved_to_jun
arm_plan_df['planned_in_jan_moved_to_jul'] = planned_in_jan_moved_to_jul
arm_plan_df['planned_in_jan_moved_to_aug'] = planned_in_jan_moved_to_aug
arm_plan_df['planned_in_jan_moved_to_sep'] = planned_in_jan_moved_to_sep
arm_plan_df['planned_in_jan_moved_to_oct'] = planned_in_jan_moved_to_oct
arm_plan_df['planned_in_jan_moved_to_nov'] = planned_in_jan_moved_to_nov
arm_plan_df['planned_in_jan_moved_to_dec'] = planned_in_jan_moved_to_dec



# соединяем с таблицей ео
eo_table = pd.read_csv('data/full_eo_list.csv', dtype=str)
eo_table.rename(columns={'eo_code': 'ЕО'}, inplace=True)
arm_plan_eo_extension_df = pd.merge(arm_plan_df, eo_table, on = 'ЕО', how = 'left')

# arm_plan_eo_extension_df.to_csv('data/arm_plan_eo_extension_df.csv')


# соединяем с таблицей level_1
level_1 = pd.read_csv('data/level_1.csv')
arm_plan_extension_full_eo_list_level_1_df = pd.merge(arm_plan_eo_extension_df, level_1, on='level_1', how = 'left')

# arm_plan_extension_full_eo_list_level_1_df.to_csv('data/arm_plan_extension_full_eo_list_level_1_df.csv')

# соединяем с таблицей level_upper
level_upper = pd.read_csv('data/level_upper.csv')
level_upper.rename(columns={'teh_mesto': 'level_upper'}, inplace=True)
arm_plan_extension_full_eo_list_level_1_level_upper_df = pd.merge(arm_plan_extension_full_eo_list_level_1_df, level_upper, on='level_upper', how='left')

arm_plan_extension_full_eo_list_level_1_level_upper_df.to_csv('data/arm_plan_extension_full_eo_list_level_1_level_upper_df.csv')


## пробуем создать таблицу для построения диаграммы
####### Итерируемся по датафрему
result_list = []
for index, row in arm_plan_extension_full_eo_list_level_1_level_upper_df.iterrows():
  temp_dict = {}
  # если в колонке planned_in_jan_and_remaining_in_jan есть единичка, то в колонку "Месяц" мы пишем слово "январь"
  planned_in_jan_and_remaining_in_jan = row['planned_in_jan_and_remaining_in_jan']
  planned_in_jan_moved_to_somewhere = row['planned_in_jan_moved_to_somewhere']
  planned_in_jan_moved_to_feb = row['planned_in_jan_moved_to_feb']
  planned_in_jan_moved_to_mar = row['planned_in_jan_moved_to_mar']
  planned_in_jan_moved_to_apr = row['planned_in_jan_moved_to_apr']
  planned_in_jan_moved_to_may = row['planned_in_jan_moved_to_may']
  planned_in_jan_moved_to_jun = row['planned_in_jan_moved_to_jun']
  planned_in_jan_moved_to_jul = row['planned_in_jan_moved_to_jul']
  planned_in_jan_moved_to_aug = row['planned_in_jan_moved_to_aug']
  planned_in_jan_moved_to_sep = row['planned_in_jan_moved_to_sep']
  planned_in_jan_moved_to_oct = row['planned_in_jan_moved_to_oct']
  planned_in_jan_moved_to_nov = row['planned_in_jan_moved_to_nov']
  planned_in_jan_moved_to_dec = row['planned_in_jan_moved_to_dec']


  main_class_description = row['eo_main_class_description']
  order_id = row['Заказ']
  level_1 = row['level_1_description']
  level_upper = row['Название технического места']
  if planned_in_jan_and_remaining_in_jan ==1:
    temp_dict['месяц'] = 'январь'
    temp_dict['Бизнес единица'] = level_1
    temp_dict['Основной класс ЕО'] = main_class_description
    temp_dict['Вышест. техместо'] = level_upper
    temp_dict['Заказ'] = order_id
    temp_dict['Запланированные на январь и оставшиеся в январе'] = 1
    temp_dict['Запланированные на январь и перенесенные в другие месяцы'] = 0
    temp_dict['Перенесенные с января'] = 0
    result_list.append(temp_dict)
    temp_dict = {}
  
  elif planned_in_jan_moved_to_somewhere == 1:
    temp_dict['месяц'] = 'январь'
    temp_dict['Бизнес единица'] = level_1
    temp_dict['Основной класс ЕО'] = main_class_description
    temp_dict['Вышест. техместо'] = level_upper
    temp_dict['Заказ'] = order_id
    temp_dict['Запланированные на январь и оставшиеся в январе'] = 0
    temp_dict['Запланированные на январь и перенесенные в другие месяцы'] = 1
    temp_dict['Перенесенные с января'] = 0
    result_list.append(temp_dict)
    temp_dict = {}
  
  if planned_in_jan_moved_to_feb == 1:
    temp_dict['месяц'] = 'февраль'
    temp_dict['Бизнес единица'] = level_1
    temp_dict['Основной класс ЕО'] = main_class_description
    temp_dict['Вышест. техместо'] = level_upper
    temp_dict['Заказ'] = order_id
    temp_dict['Запланированные на январь и оставшиеся в январе'] = 0
    temp_dict['Запланированные на январь и перенесенные в другие месяцы'] = 0
    temp_dict['Перенесенные с января'] = 1
    result_list.append(temp_dict)
    temp_dict = {}

  if planned_in_jan_moved_to_mar == 1:
    temp_dict['месяц'] = 'март'
    temp_dict['Бизнес единица'] = level_1
    temp_dict['Основной класс ЕО'] = main_class_description
    temp_dict['Вышест. техместо'] = level_upper
    temp_dict['Заказ'] = order_id
    temp_dict['Запланированные на январь и оставшиеся в январе'] = 0
    temp_dict['Запланированные на январь и перенесенные в другие месяцы'] = 0
    temp_dict['Перенесенные с января'] = 1
    result_list.append(temp_dict)
    temp_dict = {}

  if planned_in_jan_moved_to_apr == 1:
    temp_dict['месяц'] = 'апрель'
    temp_dict['Бизнес единица'] = level_1
    temp_dict['Основной класс ЕО'] = main_class_description
    temp_dict['Вышест. техместо'] = level_upper
    temp_dict['Заказ'] = order_id
    temp_dict['Запланированные на январь и оставшиеся в январе'] = 0
    temp_dict['Запланированные на январь и перенесенные в другие месяцы'] = 0
    temp_dict['Перенесенные с января'] = 1
    result_list.append(temp_dict)
    temp_dict = {}
  
  if planned_in_jan_moved_to_may == 1:
    temp_dict['месяц'] = 'май'
    temp_dict['Бизнес единица'] = level_1
    temp_dict['Основной класс ЕО'] = main_class_description
    temp_dict['Вышест. техместо'] = level_upper
    temp_dict['Заказ'] = order_id
    temp_dict['Запланированные на январь и оставшиеся в январе'] = 0
    temp_dict['Запланированные на январь и перенесенные в другие месяцы'] = 0
    temp_dict['Перенесенные с января'] = 1
    result_list.append(temp_dict)
    temp_dict = {}

  if planned_in_jan_moved_to_jun == 1:
    temp_dict['месяц'] = 'июнь'
    temp_dict['Бизнес единица'] = level_1
    temp_dict['Основной класс ЕО'] = main_class_description
    temp_dict['Вышест. техместо'] = level_upper
    temp_dict['Заказ'] = order_id
    temp_dict['Запланированные на январь и оставшиеся в январе'] = 0
    temp_dict['Запланированные на январь и перенесенные в другие месяцы'] = 0
    temp_dict['Перенесенные с января'] = 1
    result_list.append(temp_dict)
    temp_dict = {}

  if planned_in_jan_moved_to_jul == 1:
    temp_dict['месяц'] = 'июль'
    temp_dict['Бизнес единица'] = level_1
    temp_dict['Основной класс ЕО'] = main_class_description
    temp_dict['Вышест. техместо'] = level_upper
    temp_dict['Заказ'] = order_id
    temp_dict['Запланированные на январь и оставшиеся в январе'] = 0
    temp_dict['Запланированные на январь и перенесенные в другие месяцы'] = 0
    temp_dict['Перенесенные с января'] = 1
    result_list.append(temp_dict)
    temp_dict = {}

  if planned_in_jan_moved_to_aug == 1:
    temp_dict['месяц'] = 'август'
    temp_dict['Бизнес единица'] = level_1
    temp_dict['Основной класс ЕО'] = main_class_description
    temp_dict['Вышест. техместо'] = level_upper
    temp_dict['Заказ'] = order_id
    temp_dict['Запланированные на январь и оставшиеся в январе'] = 0
    temp_dict['Запланированные на январь и перенесенные в другие месяцы'] = 0
    temp_dict['Перенесенные с января'] = 1
    result_list.append(temp_dict)
    temp_dict = {}

  if planned_in_jan_moved_to_sep == 1:
    temp_dict['месяц'] = 'сентябрь'
    temp_dict['Бизнес единица'] = level_1
    temp_dict['Основной класс ЕО'] = main_class_description
    temp_dict['Вышест. техместо'] = level_upper
    temp_dict['Заказ'] = order_id
    temp_dict['Запланированные на январь и оставшиеся в январе'] = 0
    temp_dict['Запланированные на январь и перенесенные в другие месяцы'] = 0
    temp_dict['Перенесенные с января'] = 1
    result_list.append(temp_dict)
    temp_dict = {}

  if planned_in_jan_moved_to_oct == 1:
    temp_dict['месяц'] = 'октябрь'
    temp_dict['Бизнес единица'] = level_1
    temp_dict['Основной класс ЕО'] = main_class_description
    temp_dict['Вышест. техместо'] = level_upper
    temp_dict['Заказ'] = order_id
    temp_dict['Запланированные на январь и оставшиеся в январе'] = 0
    temp_dict['Запланированные на январь и перенесенные в другие месяцы'] = 0
    temp_dict['Перенесенные с января'] = 1
    result_list.append(temp_dict)
    temp_dict = {}

  if planned_in_jan_moved_to_nov == 1:
    temp_dict['месяц'] = 'ноябрь'
    temp_dict['Бизнес единица'] = level_1
    temp_dict['Основной класс ЕО'] = main_class_description
    temp_dict['Вышест. техместо'] = level_upper
    temp_dict['Заказ'] = order_id
    temp_dict['Запланированные на январь и оставшиеся в январе'] = 0
    temp_dict['Запланированные на январь и перенесенные в другие месяцы'] = 0
    temp_dict['Перенесенные с января'] = 1
    result_list.append(temp_dict)
    temp_dict = {}
  
  if planned_in_jan_moved_to_dec == 1:
    temp_dict['месяц'] = 'декабрь'
    temp_dict['Бизнес единица'] = level_1
    temp_dict['Основной класс ЕО'] = main_class_description
    temp_dict['Вышест. техместо'] = level_upper
    temp_dict['Заказ'] = order_id
    temp_dict['Запланированные на январь и оставшиеся в январе'] = 0
    temp_dict['Запланированные на январь и перенесенные в другие месяцы'] = 0
    temp_dict['Перенесенные с января'] = 1
    result_list.append(temp_dict)
    temp_dict = {}

chart_df = pd.DataFrame(result_list)

chart_df.to_csv('data/chart_df.csv')
