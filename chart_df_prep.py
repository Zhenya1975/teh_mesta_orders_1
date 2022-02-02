import pandas as pd
# подготовка таблицы для SAC

####### Итерируемся по датафрему
arm_plan_extension_full_eo_list_level_1_level_upper_df = pd.read_csv('data/arm_plan_extension_full_eo_list_level_1_level_upper_df.csv')
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

chart_df.to_csv('data/result_dfs/chart_df.csv')