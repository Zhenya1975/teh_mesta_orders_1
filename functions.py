import pandas as pd

def level_checklist_data(df):
  '''Подготовка данных для чек-листа level_1'''
  level_1_checklist_data = []
  level_1_values = []
  for index, row in df.iterrows():
      dict_temp = {}
      dict_temp['label'] = " " + str(row['Код уровня']) + ' ' + str(row['Наименование'])
      dict_temp['value'] = row['code']
      level_1_checklist_data.append(dict_temp)
      level_1_values.append(row['code'])
  return level_1_checklist_data, level_1_values

def month_year_2022_checklist_data(df):
  '''Подготовка данных для чек-листа month_year_2022'''
  month_year_2022_checklist_data = []
  month_year_2022_values = []
  for index, row in df.iterrows():
      dict_temp = {}
      dict_temp['label'] = " " + row['month_year_description']
      dict_temp['value'] = row['month_year_code']
      month_year_2022_checklist_data.append(dict_temp)
      month_year_2022_values.append(row['month_year_code'])
  return month_year_2022_checklist_data, month_year_2022_values


def eo_class_checklist_data(df):
  '''Подготовка данных для чек-листа eo_class'''
  eo_class_checklist_data = []
  eo_class_values = []
  for index, row in df.iterrows():
      dict_temp = {}
      dict_temp['label'] = " " + row['eo_class_description']
      dict_temp['value'] = row['eo_class_code']
      eo_class_checklist_data.append(dict_temp)
      eo_class_values.append(row['eo_class_code'])
  return eo_class_checklist_data, eo_class_values

def main_eo_class_checklist_data(df):
  '''Подготовка данных для чек-листа main_eo_class'''
  main_eo_class_checklist_data = []
  main_eo_class_values = []
  for index, row in df.iterrows():
      dict_temp = {}
      dict_temp['label'] = " " + row['main_eo_class_description']
      dict_temp['value'] = row['main_eo_class_code']
      main_eo_class_checklist_data.append(dict_temp)
      main_eo_class_values.append(row['main_eo_class_code'])
  return main_eo_class_checklist_data, main_eo_class_values

  



def main_eo_class_prep():
  full_eo_list = pd.read_csv('data/full_eo_list.csv')
  main_eo_class_df = full_eo_list.loc[:, ['eo_main_class_code', 'eo_main_class_description']]
  main_eo_class_df = main_eo_class_df.loc[main_eo_class_df['eo_main_class_code'] != 'no_data']
  main_eo_class_df = main_eo_class_df.loc[main_eo_class_df['eo_main_class_description'] != 'Не присвоено']
  
  result_list = []
  main_eo_codes = []
  for index, row in main_eo_class_df.iterrows():
    temp_dict = {}
    main_eo_class_code = row['eo_main_class_code']
    main_eo_class_description = row['eo_main_class_description']
    if main_eo_class_code not in main_eo_codes:
      main_eo_codes.append(main_eo_class_code)
      temp_dict['main_eo_class_code'] = main_eo_class_code
      temp_dict['main_eo_class_description'] = main_eo_class_description
      result_list.append(temp_dict)
  main_eo_class_unique_df = pd.DataFrame(result_list)
  
  main_eo_class_unique_df.to_csv('data/main_eo_class.csv')


def eo_class_prep():
  full_eo_list = pd.read_csv('data/full_eo_list.csv')
  eo_class_df = full_eo_list.loc[:, ['eo_class_code', 'eo_class_description']]
  eo_class_df = eo_class_df.loc[eo_class_df['eo_class_code'] != 'no_data']
  eo_class_df = eo_class_df.loc[eo_class_df['eo_class_description'] != 'Не присвоено']
  
  result_list = []
  eo_codes = []
  for index, row in eo_class_df.iterrows():
    temp_dict = {}
    eo_class_code = row['eo_class_code']
    eo_class_description = row['eo_class_description']
    if eo_class_code not in eo_codes:
      eo_codes.append(eo_class_code)
      temp_dict['eo_class_code'] = eo_class_code
      temp_dict['eo_class_description'] = eo_class_description
      result_list.append(temp_dict)
  eo_class_unique_df = pd.DataFrame(result_list)
  
  eo_class_unique_df.to_csv('data/eo_class.csv')

def depending_checklists(level_1_table_filter, main_eo_table_filter):
  # на вход получили списки в level_1 и в main class - те что были приготовлены для фильтрации таблицы
  # нужно взять таблицу с полным списком eo и получить из нее список кодов eo_class
  full_eo_df = pd.read_csv('data/full_eo_list.csv')
  filtered_df = full_eo_df.loc[
    full_eo_df['level_1'].isin(level_1_table_filter)&
    full_eo_df['eo_main_class_code'].isin(main_eo_table_filter)
  ] 
  # eo_class_full_list_df = filtered_df['eo_class_code']
  eo_class_unique_list_df = pd.DataFrame(set(filtered_df['eo_class_code']), columns=['eo_class_code'])
  eo_class_list_df = pd.read_csv('data/eo_class.csv')
  eo_class_df = pd.merge(eo_class_unique_list_df, eo_class_list_df, on = 'eo_class_code', how = 'left')
  eo_class_df = eo_class_df.loc[:, ['eo_class_code', 'eo_class_description']]
  eo_class_checklist = eo_class_checklist_data(eo_class_df)[0]
  return eo_class_checklist


def level_upper_checklist_data(df):
  '''Подготовка данных для чек-листа level_upper'''
  level_upper_checklist_data = []
  level_upper_values = []
  for index, row in df.iterrows():
      dict_temp = {}
      dict_temp['label'] = " " + row['Название технического места']
      dict_temp['value'] = row['level_upper']
      level_upper_checklist_data.append(dict_temp)
      level_upper_values.append(row['level_upper'])
  return level_upper_checklist_data, level_upper_values



def depending_level_upper_checklist(level_1_table_filter, main_eo_table_filter):
  full_eo_df = pd.read_csv('data/full_eo_list.csv')
  filtered_df = full_eo_df.loc[
    full_eo_df['level_1'].isin(level_1_table_filter)&
    full_eo_df['eo_main_class_code'].isin(main_eo_table_filter)
  ]
  
  level_upper_unique_list_df = pd.DataFrame(set(filtered_df['level_upper']), columns=['teh_mesto'])
  level_upper_list_df = pd.read_csv('data/level_upper.csv')
  level_upper_df = pd.merge(level_upper_unique_list_df, level_upper_list_df, on='teh_mesto', how = 'left')
  level_upper_df = level_upper_df.loc[:, ['teh_mesto', 'Название технического места']]
  level_upper_df.rename(columns={'teh_mesto': 'level_upper'}, inplace=True)
  level_upper_checklist = level_upper_checklist_data(level_upper_df)[0]
  return level_upper_checklist
 


def level_upper_prep():
  teh_mesta_full_list = pd.read_csv('data/teh_mesta_full_list.csv')
  level_upper_full_list_df = teh_mesta_full_list.loc[:, ['level_upper']]

  level_upper_unique_df = pd.DataFrame(set(level_upper_full_list_df['level_upper']), columns=['teh_mesto'])
  level_upper_unique_df = level_upper_unique_df.loc[level_upper_unique_df['teh_mesto'] != 'no_data']
  level_upper_df = pd.merge(level_upper_unique_df, teh_mesta_full_list, on = 'teh_mesto', how = 'left')
  level_upper_df = level_upper_df.loc[:, ['teh_mesto', 'Название технического места']]
  level_upper_df.to_csv('data/level_upper.csv')
level_upper_prep()

