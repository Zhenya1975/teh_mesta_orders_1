import pandas as pd
import initial_values
import yad

def month_year_index_for_sac():
  period_sort_index_dict = initial_values.period_sort_index
  result_list = []
  for key in period_sort_index_dict:
    temp_dict = {}
    # print(key)
    # print(period_sort_index_dict[key])
    temp_dict['month_year'] = key
    temp_dict['sort_index'] = period_sort_index_dict[key]
    result_list.append(temp_dict)
  period_temp_df = pd.DataFrame(result_list)

  period_dict = initial_values.period_dict
  period_temp_df['period']  = period_temp_df['month_year'].map(period_dict)
  period_temp_df['index_period'] = period_temp_df['sort_index'].astype(str)+"_"+period_temp_df['period']

  period_temp_df.to_csv('sac_files/period_indexes.csv', index = False)
  return period_temp_df
  # print(period_temp_df)




def jobs_for_sac():
# получаем файл maintanance_jobs_df.csv
  yad.get_file("maintanance_jobs_df.csv")
  print("maintanance_jobs_df загружен")
  maintanance_jobs_df = pd.read_csv('temp_files/df.csv', low_memory=False)
  yad.delete_file('temp_files/df.csv')
  print("maintanance_jobs_df прочитан и удален")
  

  
  # temp_maintanance_jobs_df.to_csv('temp_files/temp_maintanance_jobs_df.csv', index = False)
  level_1 = pd.read_csv('data/level_1.csv')
  maintanance_jobs_df = pd.merge(maintanance_jobs_df,level_1,on='level_1', how='left')
  print(maintanance_jobs_df.info()) 
  maintanance_jobs_df.head().to_csv('sac_files/maintanance_jobs_df_temp.csv')
  # Выбираем поля 
  # джойним с таблицей индексов month_year для sac
  # sac_month_year_indexes_df = month_year_index_for_sac()
  maintanance_jobs_df["maintanance_start_date"] = pd.to_datetime(maintanance_jobs_df["maintanance_start_date"])
  maintanance_jobs_df["maintanance_start_date_str"] = maintanance_jobs_df["maintanance_start_date"].dt.strftime("%Y-%m-%d %H:%m:%s")
  # 2023-01-01 05:06:49.090909
  
  sac_month_year_indexes_df = pd.read_csv('sac_files/period_indexes.csv')

  temp_maintanance_jobs_df = pd.merge(maintanance_jobs_df, sac_month_year_indexes_df, on='month_year', how='left')
  
  
  maintanance_jobs_df_for_sac = temp_maintanance_jobs_df.loc[:, ["level_1_description","eo_model_name","eo_code",'index_period', 'month_year_sort_index', 'year', 'month','maintanance_start_date_str',"maintanance_name", 'man_hours']]

  # прикручиваем имена месяцев 
  # period_dict = initial_values.period_dict
  
  # maintanance_jobs_df_for_sac['period']  = maintanance_jobs_df_for_sac['month_year'].map(period_dict)
  maintanance_jobs_df_for_sac.sort_values(['month_year_sort_index'], inplace = True)
  maintanance_jobs_df_for_sac.to_csv('sac_files/maintanance_jobs_for_manhours.csv', index = False)
  

jobs_for_sac()

