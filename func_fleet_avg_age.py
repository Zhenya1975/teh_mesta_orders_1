import pandas as pd
import functions
# import maint_records_generator
import zipfile
import yad
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

# получаем данные о машинах

full_eo_list = functions.full_eo_list_func()
full_eo_list_selected = full_eo_list.loc[:, ['eo_code', 'operation_start_date', 'operation_finish_date']]

# итерируемся по машинам в списке
eo_age_result_data = []
list_len = len(full_eo_list_selected)
i = 0
for row in full_eo_list_selected.itertuples():
  eo_code = getattr(row, "eo_code")
  i = i+1
  # print("Машина ", i, " из ",list_len)
  operation_start_date = getattr(row, "operation_start_date")
  operation_finish_date = getattr(row, "operation_finish_date")

  # первый день месяца когда началась эксплуатация
  operation_start_month_first_day = operation_start_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
  month_first_day_datetime = operation_start_month_first_day + relativedelta(months=+1)
  time_delta_betw_start_of_operation_end_next_month = (month_first_day_datetime - operation_start_date).total_seconds()

  first_day_of_month = month_first_day_datetime

  age_in_sec = time_delta_betw_start_of_operation_end_next_month
  
  while first_day_of_month < operation_finish_date:
    # print("first_day_of_month: ", first_day_of_month, "operation_finish_date: ", operation_finish_date)
    temp_dict = {}
    temp_dict['eo_code'] = eo_code
    temp_dict['operation_start_date'] = operation_start_date
    temp_dict['first_day_of_month_datetime'] = first_day_of_month
    temp_dict['year'] = first_day_of_month.year
    temp_dict['month'] = first_day_of_month.month
    temp_dict['day'] = first_day_of_month.day
    temp_dict['age_in_sec'] = age_in_sec
    eo_age_result_data.append(temp_dict)
    next_first_day_of_month = first_day_of_month + relativedelta(months=+1)
    time_delta_in_sec = (next_first_day_of_month - first_day_of_month).total_seconds()
    age_in_sec = age_in_sec + time_delta_in_sec
    first_day_of_month = next_first_day_of_month
  
  # print(operation_start_date, operation_start_month_first_day, month_first_day_datetime, time_delta_betw_start_of_operation_end_next_month)

eo_age_df = pd.DataFrame(eo_age_result_data)    

eo_age_df.to_csv('temp_files/eo_age_df.csv')


# print(full_eo_list_selected.info())



# получаем данные о maintanance_jobs_df
def extract_maintanance_jobs_df():
  with zipfile.ZipFile('output_data/maintanance_jobs_df.zip', 'r') as zipObj:
    
    # Extract all the contents of zip file in current directory
    zipObj.extractall()
    maintanance_jobs_df = pd.read_csv('output_data/maintanance_jobs_df.csv')
    # yad.upload_file(file_path, file_name)
    yad.delete_file('output_data/maintanance_jobs_df.csv')

