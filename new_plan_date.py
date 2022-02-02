import pandas as pd
import datetime

def chart_data_prep():
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
  # arm_plan_extension_full_eo_list_level_1_level_upper_df.rename(columns={'Название технического места': 'Вышестоящее техместо'}, inplace=True)
  arm_plan_extension_full_eo_list_level_1_level_upper_df.to_csv('data/arm_plan_extension_full_eo_list_level_1_level_upper_df.csv')


  ## создаем таблицу для SAC


# chart_data_prep()

# готовим датафрейм для таблицы
# импортируем присланные комменты
comments_raw_df = pd.read_csv('data/orders_comments_raw.csv', dtype = str)
# проверяем на дубли
order_list = []
result_list = []
for index, row in comments_raw_df.iterrows():
  temp_dict = {}
  order_id = row['Заказ']
  comment = row['Комментарии']
  if order_id not in order_list:
    order_list.append(order_id)
    temp_dict['Заказ'] = order_id
    temp_dict['Комментарий'] = comment
    result_list.append(temp_dict)
comments_df = pd.DataFrame(result_list)

# склеиваем данные из большой таблицы с комментами

arm_plan_data = pd.read_csv('data/arm_plan_extension_full_eo_list_level_1_level_upper_df.csv', dtype = str)

arm_plan_data_with_comments = pd.merge(arm_plan_data, comments_df, on = 'Заказ', how = 'left')
# заполянем пустые строки в комментах
values = {"Комментарий": 'нет комментария'}
arm_plan_data_with_comments = arm_plan_data_with_comments.copy()
arm_plan_data_with_comments.fillna(value=values, inplace=True)

# заполянем колонку с категориями комментов. 
# status_dict = {0: "Не выполнен", 1: "Выполнен"}
# customer_plan_fact_table_data['status'] = customer_plan_fact_table_data['status'].map(status_dict)

comment_text_comment_category = pd.read_csv('data/comment_text_comment_category.csv')
comment_dict = {}
for index, row in comment_text_comment_category.iterrows():
  comment_text = row['comment_text']
  comment_category = row['comment_category']
  comment_dict[comment_text] = comment_category
arm_plan_data_with_comments['comment_category'] = arm_plan_data_with_comments['Комментарий'].map(comment_dict)

arm_plan_data_with_comments.to_csv('data/arm_plan_data_with_comments.csv')

# готовим таблицу для SAC Перенесенные заказы
# в переменной reference_month будем держать номер месяца, который нам интересен
reference_month = "1"
moved_orders_further = arm_plan_data_with_comments.loc[arm_plan_data_with_comments['ПланДатаНачала_month'] ==reference_month]
moved_orders_further = moved_orders_further.loc[moved_orders_further['НовДатаНачала_month'] !=reference_month]

columns_for_moved_orders_report = ['Название ЕО', 'ЕО', 'Название ВРТ',	'ВидЗаказа',	'Заказ', 'КраткийТекст заказа',	'СистСтатус',	'ПользСтатус',	'ПланДатаНачала',	'НовДатаНачала', 'eo_main_class_description', 'level_1_description', 'Вышестоящее техместо', 'Комментарий',	'comment_category']
moved_orders_report = moved_orders_further.loc[:, columns_for_moved_orders_report]
moved_orders_report['calc'] = 1
moved_orders_report.to_csv('data/result_dfs/moved_orders_report.csv')



# python new_plan_date.py
