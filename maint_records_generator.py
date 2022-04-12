import pandas as pd
import functions
import func_main_jobs_prep_v2
from datetime import timedelta
import numpy as np

def maint_records_generator():
  # открываем почасовую таблицу и итерируясь по списку форм заполняем нулями строки где есть работы  
  # В maintanance_jobs_df будем создавать записи с работами
  
  eo_job_catologue_df = functions.eo_job_catologue_df_func()
  
  full_eo_list = functions.full_eo_list_func()
  full_eo_list_selected = full_eo_list.loc[:, ['eo_code','strategy_id', 'avearage_day_operation_hours', 'operation_start_date', 'operation_finish_date']]
  
  # full_eo_list_selected = full_eo_list_selected.loc[full_eo_list_selected['eo_code'].isin(["sl_730_3", "sl_730_61", "sl_730_62"])]
  full_eo_list_selected = full_eo_list_selected.loc[full_eo_list_selected['eo_code'].isin(["sl_730_1"])]
  full_eo_list_selected.to_csv('temp_files/full_eo_list_selected.csv')
  #full_eo_list_selected = full_eo_list_selected.loc[full_eo_list_selected['strategy_id'].isin([6])]
  
  # full_eo_list_selected = full_eo_list_selected.loc[full_eo_list_selected['eo_code'].isin(["sl_730_1", "sl_730_2", "sl_730_3"])]

  eo_list = list(set(full_eo_list_selected['eo_code']))
  # maint_sorted_df = pd.read_csv('data/maint_forms_sorted_df.csv')
  maint_sorted_df = func_main_jobs_prep_v2.list_of_maintanance_forms_sorted(eo_list)

  ############################################
  maint_sorted_df.to_csv('temp_files/maint_sorted_df.csv', index = False)
  ##############################################
  # итерируемся по списку машин
  # eo_list = list(set(maint_sorted_df['eo_code']))
  eo_len = len(full_eo_list_selected)
  ktg_data_df = pd.DataFrame()
  maintanance_jobs_df_total_data = pd.DataFrame()
  i = 0
  # итерируемся по списку машин
  for row in full_eo_list_selected.itertuples():
    i = i+1
    maintanance_jobs_df_list = []
    eo_code = getattr(row, "eo_code")
    
    print("формирование maintanance_jobs_df. Машина ", i, " из", eo_len,". ео:", eo_code)
    
    operation_start_date = getattr(row, "operation_start_date")
    operation_finish_date = getattr(row, "operation_finish_date")
  
    hours_df = func_main_jobs_prep_v2.hours_df_prep(eo_code, operation_start_date, operation_finish_date)
    # print("hours_df", hours_df)
    # коэффициент, кооторый дает количество календарных часов при умножении на значение наработки по счетчику
    # motohours_koef = avearage_day_operation_hours/24
    # заполняем данные о ето
    # значение простоя и трудозатрат на ето для текущей машины
    eto_df_data = eo_job_catologue_df.loc[eo_job_catologue_df['eo_code']==eo_code] 
    eto_df_data = eto_df_data.loc[eto_df_data['maintanance_category_id']=='eto']
    maintanance_job_code = eto_df_data.iloc[0]['eo_maintanance_job_code']
    maintanance_category_id = eto_df_data.iloc[0]['maintanance_category_id']
    maintanance_name = eto_df_data.iloc[0]['maintanance_name']
    man_hours = eto_df_data.iloc[0]['man_hours']
    
    eo_downtime = eto_df_data.iloc[0]['downtime_planned']
    # eo_manhours = eto_df_data.iloc[0]['man_hours']
    # режем hours-df на 8 утра
    hours_df_eto_selection = hours_df.loc[hours_df['hour']==8]
    indexes_hours_df_eto_selection = hours_df_eto_selection.index.values
      
    # записываем значение простоя на ето
    hours_df.loc[indexes_hours_df_eto_selection, ['downtime_status']] = eo_downtime
    # записываем состояние счетчика в час, в который проходит ЕТО
    hours_df.loc[indexes_hours_df_eto_selection, ['motohour_hour_status']] = 1-eo_downtime
    
    ##################################################################################
    # hours_df.to_csv("temp_files/hours_df_with_eto_data.csv", index = False)
    
    ###########################################################################################
    ################# СОЗДАЕМ ЗАПИСИ О ЕТО В maintanance_jobs_df
    ##############################################################################################
    eto_motohours_df = hours_df_eto_selection.loc[hours_df_eto_selection['eo_motohour_hour']<operation_finish_date]

    maintanance_start_datetime_eto_list = list(eto_motohours_df['eo_motohour_hour'])
    maintanance_jobs_df_eto = pd.DataFrame(maintanance_start_datetime_eto_list, columns = ['maintanance_start_datetime'])
    
    maintanance_jobs_df_eto['maintanance_finish_datetime'] = maintanance_jobs_df_eto['maintanance_start_datetime'] + timedelta(hours = eo_downtime)
    maintanance_jobs_df_eto['maintanance_job_code'] = maintanance_job_code
    maintanance_jobs_df_eto['eo_code'] = eo_code
    maintanance_jobs_df_eto['maintanance_category_id'] = maintanance_category_id
    maintanance_jobs_df_eto['maintanance_name'] = maintanance_name
    maintanance_jobs_df_eto['interval_motohours'] = 24
    maintanance_jobs_df_eto['man_hours'] = man_hours
    maintanance_jobs_df_eto['downtime'] = eo_downtime
    maintanance_jobs_df_eto['day_of_opearation'] = (maintanance_jobs_df_eto['maintanance_start_datetime'] - operation_start_date).dt.total_seconds()/(60*60*24)
    # добавляем данные по eto в общую таблицу 
    maintanance_jobs_df_total_data = pd.concat([maintanance_jobs_df_total_data, maintanance_jobs_df_eto])

    print("Данные eto для ео ", eo_code, 'добавлены в модель')
    ####################################################################################################
    ####################################################################################################
    maint_sorted_df_selected_by_eo = maint_sorted_df.loc[maint_sorted_df['eo_code'].isin([eo_code])]
    number_of_maint_records = len(maint_sorted_df_selected_by_eo)
    j=0
    for row in maint_sorted_df_selected_by_eo.itertuples():
      # print("eo_code в цикле по работам", eo_code)
      j = j+1
      print("Работа ", j, " из ", number_of_maint_records)
      
      maintanance_job_code = getattr(row, "maintanance_job_code")
      maintanance_name = getattr(row, "maintanance_name")
      eo_code = getattr(row, "eo_code")
      maintanance_category_id = getattr(row, "maintanance_category_id")
      
      maint_interval = getattr(row, "maint_interval")
      downtime = getattr(row, "downtime")
      man_hours = getattr(row, "man_hours")
      hours_df['cumsum'] = hours_df['motohour_hour_status'].cumsum()
      # hours_df['cumsum'] = hours_df['cumsum'].apply(lambda x: round(x,0))
      hours_df['cumsum'] = hours_df['cumsum'].round(0)

      # print(hours_df.info())
      # строка, в которой значение счетчика  моточасов равно текущему значению наработки
      # hours_df.to_csv('temp_files/hours_dff_with_cumsum.csv', index = False)
     
      hours_df_selected = hours_df.loc[hours_df['cumsum']==maint_interval, ['eo_motohour_hour', 'cumsum']]
 
      hours_df_selected = hours_df_selected.iloc[:1]
      
      maintanance_start_datetime = hours_df_selected.iloc[0]['eo_motohour_hour']
      
      if maintanance_start_datetime < operation_finish_date:
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

        ##############################################
        #################################################
        maintanance_jobs_df_temp_dict['day_of_opearation'] = (maintanance_start_datetime - operation_start_date).total_seconds()/(60*60*24)
        
        maintanance_jobs_df_list.append(maintanance_jobs_df_temp_dict)
        

        # получаем диапазон в таблице часов
        model_hours_df_cut_by_maint_job = hours_df.loc[
            (hours_df['eo_motohour_hour'] > maintanance_start_datetime) &
            (hours_df['eo_motohour_hour'] <= maintanance_finish_datetime)]
        indexes_maint_job = model_hours_df_cut_by_maint_job.index.values
     
      
        # записываем ноль в поле motohour_hour_status - значит в этом интервале счетчик моточасов не работает
        hours_df.loc[indexes_maint_job, ['motohour_hour_status']] = 0
        hours_df.loc[indexes_maint_job, ['downtime_status']] = 1
        # режем hours_df
        # hours_df = hours_df.loc[hours_df['eo_motohour_hour'] < operation_finish_date]
    hours_df = hours_df.loc[hours_df['eo_motohour_hour'] < operation_finish_date]
    # hours_df.to_csv('temp_files/hours_df_with_all_data.csv', index = False)
    month_year_groupped_df = hours_df.groupby(['eo', 'year', 'month'], as_index = False)[['calendar_fond', 'downtime_status']].sum()

    ################## подготовка таблицы со значением наработки после года эксплуатации
    year_counter_df_list = []
    current_datetime = operation_start_date
    while current_datetime < operation_finish_date:
      current_datetime = current_datetime + timedelta(days = 365)
      try:
        temp_dict = {}
        hours_df_selected = hours_df.loc[hours_df['eo_motohour_hour']==current_datetime]
        counter_value = hours_df_selected.iloc[0]['cumsum']
        temp_dict['eo_code'] = eo_code
        temp_dict['datetime'] = current_datetime
        temp_dict['counter_value'] = counter_value
        year_counter_df_list.append(temp_dict)
      except:
        pass
    
    
    ktg_data_df = pd.concat([ktg_data_df, month_year_groupped_df])

    maintanance_jobs_df = pd.DataFrame(maintanance_jobs_df_list)
    # режем maintanance_jobs_df
    maintanance_jobs_df = maintanance_jobs_df.loc[maintanance_jobs_df['maintanance_start_datetime'] < operation_finish_date]
    # добавляем данные по eto в общую таблицу 
    maintanance_jobs_df_total_data = pd.concat([maintanance_jobs_df_total_data, maintanance_jobs_df])
    maintanance_jobs_df = pd.DataFrame()
    name_file = 'temp_files/hours_df' + eo_code + ".csv"
    hours_df.to_csv(name_file)
  
    print("Данные для ео ", eo_code, 'добавлены в модель')
  
  counter_year_df = pd.DataFrame(year_counter_df_list)
  counter_year_df['year'] = counter_year_df['datetime'].dt.year
  counter_year_df.to_csv('output_data/counter_year.csv', index = False)
  
  ktg_data_df.to_csv('output_data/ktg_data_df.csv', index = False, decimal = ",")
  

  full_eo_list_for_merge = full_eo_list.loc[:,['eo_code', 'level_1_description', 'eo_class_description','eo_model_name', 'eo_description']]


  
  maintanance_jobs_df_total_data['year_of_operation'] = maintanance_jobs_df_total_data['day_of_opearation']/365
  maintanance_jobs_df_total_data['year_of_operation'] = maintanance_jobs_df_total_data['year_of_operation'].apply(np.floor)+1

  
  
  maintanance_jobs_df_ = pd.merge(maintanance_jobs_df_total_data, full_eo_list_for_merge, on = 'eo_code', how='left')
  maintanance_jobs_df_.sort_values(['maintanance_start_datetime'], inplace=True)
  maintanance_jobs_df_['man_hours'] = maintanance_jobs_df_['man_hours'].astype(str)
  maintanance_jobs_df_['man_hours'] = (maintanance_jobs_df_['man_hours'].str.split()).apply(lambda x: float(x[0].replace(',', '')))
  maintanance_jobs_df_['year'] = maintanance_jobs_df_['maintanance_start_datetime'].dt.year
  maintanance_jobs_df_['month'] = maintanance_jobs_df_['maintanance_start_datetime'].dt.month
  
  maintanance_jobs_df_.to_csv('temp_files/maintanance_jobs_df.csv', decimal=",", index = False)


  # maintanance_jobs_df_.to_csv('output_data/maintanance_jobs_df.csv', decimal=",", index = False)
   
 
  


    
# list_of_maintanance_forms_sorted()
maint_records_generator()
maintanance_jobs_df = pd.read_csv('temp_files/maintanance_jobs_df.csv', decimal=",")
maintanance_jobs_df_short = maintanance_jobs_df.loc[:, ['eo_code', 'maintanance_category_id', 'maintanance_name', 'interval_motohours','maintanance_start_datetime','maintanance_finish_datetime','downtime','man_hours','motohours_value', 'year', 'month', 'year_of_operation']]

maintanance_jobs_df_short.to_csv('output_data/maintanance_jobs_df_short.csv', decimal=",", index = False)
# список машин
eo_list = list(set(maintanance_jobs_df_short['eo_code']))
# print(eo_list)
year_list = list(set(maintanance_jobs_df_short['year']))
year_list = sorted(year_list)
# print(year_list)
month_list = list(set(maintanance_jobs_df_short['month']))
month_list = sorted(month_list)
result_list = []
for year_el in year_list:
  for month_el in month_list:
    temp_dict  = {}
    temp_df = maintanance_jobs_df_short.loc[maintanance_jobs_df_short['year']==year_el]
    temp_df = temp_df.loc[temp_df['month']==month_el]
    number_of_eo= len(list(set(temp_df['eo_code'])))
    temp_dict['year'] = year_el
    temp_dict['month'] = month_el
    temp_dict['number_of_eo'] = number_of_eo
    # print(number_of_eo, month_el)
    result_list.append(temp_dict)
number_of_eo_df = pd.DataFrame(result_list)
number_of_eo_df.to_csv('output_data/number_of_eo.csv', index = False)