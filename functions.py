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