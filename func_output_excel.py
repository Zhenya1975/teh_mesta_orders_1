import pandas as pd
import yad
import df_to_excel
import initial_values
import functions

def output_excel():
  dict_of_df = {}
  
  maintanance_job_list_general = functions.maintanance_job_list_general_func()
  maintanance_job_list_general = maintanance_job_list_general.loc[:, ['maintanance_code', 'maintanance_name', 'upper_level_tehmesto_description', 'interval_type',	'interval_motohours','downtime_planned',	'man_hours',	'tr_man_hours_start_value',	'tr_man_hours_finish_value',	'tr_downtime_start_value',	'tr_downtime_finish_value',	'tr_start_motohour',	'tr_finish_motohour']]
  

  maintanance_job_list_general.rename(columns=initial_values.rename_columns_dict, inplace = True)
  dict_of_df['Регламент'] = maintanance_job_list_general
  
  
  file_df = yad.get_file("maintanance_jobs_short.csv")
  maintanance_jobs_short_df = pd.read_csv('temp_files/df.csv', decimal = ",")
  
  maintanance_jobs_short_df = maintanance_jobs_short_df.astype({'eo_code': str})
  maintanance_jobs_short_df["maintanance_start_date"] = pd.to_datetime(maintanance_jobs_short_df["maintanance_start_date"])
  maintanance_jobs_short_df["maintanance_finish_date"] = pd.to_datetime(maintanance_jobs_short_df["maintanance_finish_date"])
  maintanance_jobs_short_df["maintanance_start_date"] = maintanance_jobs_short_df["maintanance_start_date"].dt.strftime("%d.%m.%Y")
  maintanance_jobs_short_df["maintanance_finish_date"] = maintanance_jobs_short_df["maintanance_finish_date"].dt.strftime("%d.%m.%Y")
  
  maintanance_jobs_short_df = maintanance_jobs_short_df.rename(columns=initial_values.rename_columns_dict)
  # yad.delete_file('temp_files/df.csv')
  # print(maintanance_jobs_short_df.info())
  dict_of_df["Воздействия ТОИР"] = maintanance_jobs_short_df

  # подготовка листа ЕО в эксплуатации
  full_eo_list = functions.full_eo_list_func()
  
  
  

  df_to_excel.df_to_excel(dict_of_df)
  

# output_excel()


    