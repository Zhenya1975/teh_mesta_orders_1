import pandas as pd
import functions
# import maint_records_generator
import zipfile
import yad
import initial_values
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

def func_fleet_data_infopage():
  # получаем данные о машинах
  
  full_eo_list = functions.full_eo_list_func()
  full_eo_list_selected = full_eo_list.loc[:, ['eo_code', 'operation_start_date', 'operation_finish_date', 'level_1_description', 'eo_class_description','eo_model_name', 'eo_description']]

  sac_report_maintanance_jobs = pd.read_csv('output_data/sac_report_maintanance_jobs.csv', low_memory=False)
  eo_list = list(set(sac_report_maintanance_jobs['ЕО']))
  full_eo_list_selected = full_eo_list_selected.loc[full_eo_list_selected['eo_code'].isin(eo_list)]
  full_eo_list_selected = full_eo_list_selected.rename(columns=initial_values.rename_columns_dict)
  full_eo_list_selected['count'] = 1
  full_eo_list_selected.to_csv('output_data/fleet_data.csv', index = False)

func_fleet_data_infopage()

def func_all_fleet_data_infopage():
  # получаем данные о машинах
  
  full_eo_list = functions.full_eo_list_actual_func()
  full_eo_list_selected = full_eo_list.loc[:, ['eo_code', 'eo_model_id', 'operation_start_date', 'operation_finish_date', 'level_1_description', 'eo_class_description','eo_model_name', 'eo_description']]
  # print(full_eo_list_selected.info())
  full_eo_list_selected = full_eo_list_selected.loc[full_eo_list_selected['eo_model_id'] != 'no_data']
 
  full_eo_list_selected = full_eo_list_selected.rename(columns=initial_values.rename_columns_dict)
  full_eo_list_selected['count'] = 1
  full_eo_list_selected.to_csv('output_data/all_fleet_data.csv', index = False)

# func_all_fleet_data_infopage()
