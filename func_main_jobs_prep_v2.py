import pandas as pd
from datetime import timedelta
import functions
# первое - создаем датафрейм в котором строки- это минуты срока эксплуатации машины. 
# заполняем единичками поля статуа счетчика моточасов. то есть по умолчанию счетчик работает в каждую минуту

# operation_start_datetime = pd.to_datetime('01.01.2023', format='%d.%m.%Y')
# operation_finish_datetime = pd.to_datetime('31.12.2033', format='%d.%m.%Y')
# eo = "sl_730_1"

def hours_df_prep(eo, operation_start_datetime, operation_finish_datetime):
  hour_df_data = []
  current_hours_datetime = operation_start_datetime
  while current_hours_datetime < operation_finish_datetime:
    temp_dict = {}
    temp_dict['eo'] = eo
    current_hours_datetime = current_hours_datetime + timedelta(hours=1)
    temp_dict['eo_motohour_hour'] = current_hours_datetime
    temp_dict["motohour_hour_status"] = 1
    temp_dict['downtime_status'] = 0
    hour_df_data.append(temp_dict)

  motohours_hour_df = pd.DataFrame(hour_df_data)

  return motohours_hour_df



def eo_job_catologue_df_func():
  """чтение eo_job_catologue_df"""
  eo_job_catologue_df = pd.read_csv('data/eo_job_catologue.csv', dtype=str)
  eo_job_catologue_df["downtime_planned"] = eo_job_catologue_df["downtime_planned"].astype('float')
  
  return eo_job_catologue_df


def list_of_maintanance_forms_sorted():
  
  eo_job_catologue_df = eo_job_catologue_df_func()
  # создаем список форм ТОиР. eo, номинальная наработка с начала эксплуатации, простой, тип ТОИР
  # итерируемся по строкам файла eo_job_catologue_df
  full_eo_list = functions.full_eo_list_func()
  full_eo_list_selected = full_eo_list.loc[:, ['eo_code', 'avearage_day_operation_hours', 'operation_start_date', 'operation_finish_date']]
  
  # print("full_eo_list_selected info", full_eo_list_selected.info())
  # eo_job_catologue_df["operation_start_date"] = pd.to_datetime(eo_job_catologue_df["operation_start_date"])
  # eo_job_catologue_df["operation_finish_date"] = pd.to_datetime(eo_job_catologue_df["operation_finish_date"])
  
  eo_maint_plan = pd.merge(eo_job_catologue_df, full_eo_list_selected, on='eo_code', how='left')
  eo_maint_plan.to_csv("data/eo_maint_plan_by_eo_delete.csv")
  eo_list = list(set(eo_maint_plan['eo_code']))
  
  result_list_df = []
  # eo_maint_plan = eo_maint_plan.loc[eo_maint_plan['eo_code']=='sl_730_1']
  i = 0
  ############## ИТЕРИРУЕМСЯ ПО СПИСКУ ЕО ##########################
  for eo in eo_list:
    # print("eo:", eo)
    i = i+1
    # print("формирование таблицы data/maint_forms_sorted_df.csv. eo ", i, " из", eo_list)
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

    
      # ищем работы с поглащениями
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
        temp_dict['downtime'] = plan_downtime
        temp_dict['man_hours'] = man_hours
        result_list_df.append(temp_dict)

      # 3. если попалась строка без поглащений
      elif tr_category !='tr' and maintanance_category_id != 'eto' and go_interval =='not':
        temp_dict = {}
        temp_dict['maintanance_job_code'] = maintanance_job_code
        temp_dict['eo_code'] = eo_code
        temp_dict['maintanance_category_id'] = maintanance_category_id
        temp_dict['maintanance_name'] = maintanance_name
        temp_dict['maint_interval'] = float(interval_motohours)
        temp_dict['downtime'] = plan_downtime
        temp_dict['man_hours'] = man_hours
        result_list_df.append(temp_dict)
      

    maint_sorted_df = pd.DataFrame(result_list_df)
    maint_sorted_df.sort_values(['maint_interval', 'downtime'], inplace = True)
    maint_sorted_df.to_csv('data/maint_forms_sorted_df.csv', index = False)
    # print("Завершено формирование таблицы data/maint_forms_sorted_df.csv")


    #############################################
    ############################################
    ###############################################
def maint_records_generator():
  # открываем почасовую таблицу и итерируясь по списку форм заполняем нулями строки где есть работы  
  # В maintanance_jobs_df будем создавать записи с работами
  maintanance_jobs_df_list = []
  full_eo_list = functions.full_eo_list_func()
  full_eo_list_selected = full_eo_list.loc[:, ['eo_code', 'avearage_day_operation_hours', 'operation_start_date', 'operation_finish_date']]
  
  full_eo_list_selected = full_eo_list_selected.loc[full_eo_list_selected['eo_code'].isin(["sl_730_1"])]
  maint_sorted_df = pd.read_csv('data/maint_forms_sorted_df.csv')
  maint_sorted_df = maint_sorted_df.loc[maint_sorted_df['eo_code'].isin(["sl_730_1"])]
  # итерируемся по списку машин
  i = 0
  eo_len = len(full_eo_list_selected)
  for row in full_eo_list_selected.itertuples():
    i = i+1
    eo_code = getattr(row, "eo_code")
    # print("формирование maintanance_jobs_df. Машина ", i, " из", eo_len,". ео:", eo_code)
    operation_start_date = getattr(row, "operation_start_date")
    operation_finish_date = getattr(row, "operation_finish_date")
  
    hours_df = hours_df_prep(eo_code, operation_start_date, operation_finish_date)
    # print("hours_df", hours_df)
    # коэффициент, кооторый дает количество календарных часов при умножении на значение наработки по счетчику
    # motohours_koef = avearage_day_operation_hours/24
    
    # print(maint_sorted_df.info())
    for row in maint_sorted_df.itertuples():
      
      maintanance_job_code = getattr(row, "maintanance_job_code")
      maintanance_name = getattr(row, "maintanance_name")
      eo_code = getattr(row, "eo_code")
      maintanance_category_id = getattr(row, "maintanance_category_id")

      
      maint_interval = getattr(row, "maint_interval")
      downtime = getattr(row, "downtime")
      man_hours = getattr(row, "downtime")
      hours_df['cumsum'] = hours_df['motohour_hour_status'].cumsum()
      # строка, в которой значение счетчика  моточасов равно текущему значению наработки
      try:
        hours_df_selected = hours_df.loc[hours_df['cumsum']==maint_interval, ['eo_motohour_hour', 'cumsum']]
     
        maintanance_start_datetime = hours_df_selected.iloc[0]['eo_motohour_hour']
        motohours_value = hours_df_selected.iloc[0]['cumsum']
        
        # interval_motohours	interval_type	maint_interval	downtime_plan	man_hours
        ################ НАБИВАЕМ maintanance_jobs_df ДАННЫМИ ###################################
        maintanance_jobs_df_temp_dict = {}
        maintanance_jobs_df_temp_dict['maintanance_job_code'] = maintanance_job_code
        maintanance_jobs_df_temp_dict['eo_code'] = eo_code
        maintanance_jobs_df_temp_dict['maintanance_category_id'] = maintanance_category_id
        maintanance_jobs_df_temp_dict['maintanance_name'] = maintanance_name
        maintanance_jobs_df_temp_dict['interval_motohours'] = maint_interval
        maintanance_jobs_df_temp_dict['maintanance_start_datetime'] = maintanance_start_datetime
        
        # maintanance_start_datetime = operation_start_date + timedelta(hours = calendar_interval_hours)
        maintanance_finish_datetime = maintanance_start_datetime + timedelta(hours = downtime)
        maintanance_jobs_df_temp_dict['maintanance_finish_datetime'] = maintanance_finish_datetime
        maintanance_jobs_df_temp_dict['downtime'] = float(downtime)
        maintanance_jobs_df_temp_dict['man_hours'] = float(man_hours)
        maintanance_jobs_df_temp_dict['motohours_value'] = motohours_value

        maintanance_jobs_df_list.append(maintanance_jobs_df_temp_dict)

        # получаем диапазон в таблице часов
        model_hours_df_cut_by_maint_job = hours_df.loc[
            (hours_df['eo_motohour_hour'] > maintanance_start_datetime) &
            (hours_df['eo_motohour_hour'] <= maintanance_finish_datetime)]
        indexes_maint_job = model_hours_df_cut_by_maint_job.index.values
       
        
        # записываем ноль в поле motohour_hour_status - значит в этом интервале счетчик моточасов не работает
        hours_df.loc[indexes_maint_job, ['motohour_hour_status']] = 0
        hours_df.loc[indexes_maint_job, ['downtime_status']] = 1
      except:
        pass
       
  
  maintanance_jobs_df = pd.DataFrame(maintanance_jobs_df_list)
  maintanance_jobs_df = maintanance_jobs_df.copy()
  full_eo_list_for_merge = full_eo_list.loc[:,['eo_code', 'level_1_description', 'eo_class_description','eo_model_name', 'eo_description']]
  # print(full_eo_list_for_merge.info())
  # print("maintanance_jobs_df", maintanance_jobs_df.info())
  
  maintanance_jobs_df_ = pd.merge(maintanance_jobs_df, full_eo_list_for_merge, on = 'eo_code', how='left')
  maintanance_jobs_df_.to_csv('temp_files/maintanance_jobs_df_temp.csv', decimal=",")
  hours_df.to_csv("temp_files/hours_df_delete.csv")
  ## а что если проверить
      


    
# list_of_maintanance_forms_sorted()
maint_records_generator()