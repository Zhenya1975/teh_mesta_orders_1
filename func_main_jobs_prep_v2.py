import pandas as pd
from datetime import timedelta
import functions
import initial_values
# первое - создаем датафрейм в котором строки- это минуты срока эксплуатации машины. 
# заполняем единичками поля статуа счетчика моточасов. то есть по умолчанию счетчик работает в каждую минуту

# operation_start_datetime = pd.to_datetime('01.01.2023', format='%d.%m.%Y')
# operation_finish_datetime = pd.to_datetime('31.12.2033', format='%d.%m.%Y')
# eo = "sl_730_1"

def hours_df_prep(eo, operation_start_datetime, operation_finish_datetime):
  hour_df_data = []
  current_hours_datetime = operation_start_datetime
  while current_hours_datetime < operation_finish_datetime + timedelta(hours=150000):
    temp_dict = {}
    temp_dict['eo'] = eo
    current_hours_datetime = current_hours_datetime + timedelta(hours=1)
    temp_dict['eo_motohour_hour'] = current_hours_datetime
    temp_dict["motohour_hour_status"] = 1
    temp_dict['downtime_status'] = 0
    temp_dict['calendar_fond'] = 1
    temp_dict['year'] = current_hours_datetime.year
    temp_dict['month'] = current_hours_datetime.month
    temp_dict['hour'] = current_hours_datetime.hour
    temp_dict['maint_job'] = []
    hour_df_data.append(temp_dict)

  motohours_hour_df = pd.DataFrame(hour_df_data)

  return motohours_hour_df



def eo_job_catologue_df_func():
  """чтение eo_job_catologue_df"""
  eo_job_catologue_df = pd.read_csv('data/eo_job_catologue.csv', dtype=str)
  eo_job_catologue_df["downtime_planned"] = eo_job_catologue_df["downtime_planned"].astype('float')
  
  return eo_job_catologue_df


def list_of_maintanance_forms_sorted(list_of_eos):
  
  eo_job_catologue_df = eo_job_catologue_df_func()
  eo_job_catologue_df = eo_job_catologue_df.loc[eo_job_catologue_df['eo_code'].isin(list_of_eos)]
  # создаем список форм ТОиР. eo, номинальная наработка с начала эксплуатации, простой, тип ТОИР
  # итерируемся по строкам файла eo_job_catologue_df
  full_eo_list = functions.full_eo_list_func()
  full_eo_list_selected = full_eo_list.loc[:, ['eo_code', 'avearage_day_operation_hours', 'operation_start_date', 'operation_finish_date']]
  
  # print("full_eo_list_selected info", full_eo_list_selected.info())
  # eo_job_catologue_df["operation_start_date"] = pd.to_datetime(eo_job_catologue_df["operation_start_date"])
  # eo_job_catologue_df["operation_finish_date"] = pd.to_datetime(eo_job_catologue_df["operation_finish_date"])
  
  eo_maint_plan = pd.merge(eo_job_catologue_df, full_eo_list_selected, on='eo_code', how='left')
  # eo_maint_plan.to_csv("data/eo_maint_plan_by_eo_delete.csv")
  eo_list = list(set(eo_maint_plan['eo_code']))
  
  result_list_df = []
  # eo_maint_plan = eo_maint_plan.loc[eo_maint_plan['eo_code']=='sl_730_1']
  i = 0
  ############## ИТЕРИРУЕМСЯ ПО СПИСКУ ЕО ##########################
  for eo in eo_list:
    # print("eo:", eo)
    i = i+1
    print("формирование таблицы data/maint_forms_sorted_df.csv. eo ", i, " из", len(eo_list))
    eo_maint_plan_by_eo = eo_maint_plan.loc[eo_maint_plan['eo_code'] == eo]
    
    
    for row in eo_maint_plan_by_eo.itertuples():
      maintanance_job_code = getattr(row, "eo_maintanance_job_code")
      eo_code = getattr(row, "eo_code")
      standard_interval_motohours = float(getattr(row, "interval_motohours"))
      plan_downtime = getattr(row, "downtime_planned")
      man_hours = getattr(row, "man_hours")
      operation_start_date = getattr(row, "operation_start_date")
      operation_finish_date = getattr(row, "operation_finish_date")
      # avearage_day_operation_hours = getattr(row, "avearage_day_operation_hours")
      maintanance_category_id = getattr(row, "maintanance_category_id")
      maintanance_name = getattr(row, "maintanance_name")
      tr_category = getattr(row, "tr_category")
      interval_type = getattr(row, "interval_type")
      go_interval = getattr(row, "go_interval")
      interval_motohours = getattr(row, "interval_motohours")
      tr_service_interval = getattr(row, "tr_service_interval")

   
      # создаем строки, расставляя межсервисные интервалы
      
      # 1. если попалась строка с поглащениями
      if go_interval !='not' and tr_category !='tr':
        temp_dict = {}
        go_interval_list = go_interval.split(';')
        go_interval_list = [int(i) for i in go_interval_list]
        # итерируемся по списку go_interval
        for maintanance_interval_value in go_interval_list:
          temp_dict = {}
          temp_dict['maintanance_job_code'] = maintanance_job_code
          temp_dict['eo_code'] = eo_code
          temp_dict['maintanance_category_id'] = maintanance_category_id
          temp_dict['maintanance_name'] = maintanance_name
          temp_dict['maint_interval'] = float(maintanance_interval_value)
          temp_dict['downtime'] = plan_downtime
          temp_dict['man_hours'] = man_hours
          result_list_df.append(temp_dict)
          
      
      # 2. если попалась строка с ТР
      elif tr_category =='tr':
        temp_dict = {}
        temp_dict['maintanance_job_code'] = maintanance_job_code
        temp_dict['eo_code'] = eo_code
        temp_dict['maintanance_category_id'] = maintanance_category_id
        temp_dict['maintanance_name'] = maintanance_name
        temp_dict['maint_interval'] = float(tr_service_interval)
        temp_dict['tr_service_interval'] = float(tr_service_interval)
        
        temp_dict['downtime'] = plan_downtime
        temp_dict['man_hours'] = man_hours
        result_list_df.append(temp_dict)

      # 3. если попалась строка без поглащений
      elif tr_category !='tr' and maintanance_category_id != 'eto' and go_interval =='not':

        mth_counter = 0
        while mth_counter < 150000:
          mth_counter = mth_counter + float(interval_motohours)
          temp_dict = {}
          temp_dict['maintanance_job_code'] = maintanance_job_code
          temp_dict['eo_code'] = eo_code
          temp_dict['maintanance_category_id'] = maintanance_category_id
          temp_dict['maintanance_name'] = maintanance_name
          temp_dict['maint_interval'] = mth_counter
          temp_dict['downtime'] = plan_downtime
          temp_dict['man_hours'] = man_hours
          result_list_df.append(temp_dict)
      
      
    maint_sorted_df = pd.DataFrame(result_list_df)
    maint_sorted_df.sort_values(['maint_interval', 'downtime'], inplace = True)
    maint_sorted_df.to_csv('data/maint_forms_sorted_df.csv', index = False)
    # print("Завершено формирование таблицы data/maint_forms_sorted_df.csv")
  return maint_sorted_df

    #############################################
    ############################################
    ###############################################



