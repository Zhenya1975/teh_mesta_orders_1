import pandas as pd
import functions
import initial_values
import func_main_jobs_prep_v2
from datetime import timedelta
import numpy as np
import yad
import func_eo_job_catalague_prep
import shutil
import zipfile

# 100000062379 785C Олимпиадинский ГОК
# 100000008673 785C Полюс Вернинское
# 100000065514 793D Олимпиадинский ГОК
# 100000084396 730 Полюс Магадан
# sl_730_1 Сухой лог
# ['100000062379', '100000008673', '100000065514', '100000084396', 'sl_730_1']

def maint_records_generator():
  # открываем почасовую таблицу и итерируясь по списку форм заполняем нулями строки где есть работы  
  # В maintanance_jobs_df будем создавать записи с работами
  
  eo_job_catologue_df = functions.eo_job_catologue_df_func()
  
  full_eo_list = functions.full_eo_list_func()
  full_eo_list_selected = full_eo_list.loc[:, ['eo_code','strategy_id', 'avearage_day_operation_hours', 'operation_start_date', 'operation_finish_date']]
  
  # full_eo_list_selected = full_eo_list_selected.loc[full_eo_list_selected['eo_code'].isin(["sl_730_3", "sl_730_61", "sl_730_62"])]
  # full_eo_list_selected = full_eo_list_selected.loc[full_eo_list_selected['eo_code'].isin(["100000065629"])]
  # full_eo_list_selected.to_csv('temp_files/full_eo_list_selected.csv')
  # full_eo_list_selected = full_eo_list_selected.loc[full_eo_list_selected['strategy_id'].isin([4])]
  # full_eo_list_selected = full_eo_list_selected.loc[full_eo_list_selected['strategy_id'].isin([2,4,5,6])]
  full_eo_list_selected = full_eo_list_selected.loc[full_eo_list_selected['eo_code'].isin(['100000062379', '100000008673', '100000065514', '100000084396', 'sl_730_1'])]

  eo_list = list(set(full_eo_list_selected['eo_code']))
  # maint_sorted_df = pd.read_csv('data/maint_forms_sorted_df.csv')
  maint_sorted_df = func_main_jobs_prep_v2.list_of_maintanance_forms_sorted(eo_list)

  ############################################
  # maint_sorted_df.to_csv('temp_files/maint_sorted_df.csv', index = False)
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
      # print("EO: ", eo_code, ". Работа ", j, " из ", number_of_maint_records)
      
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


      # строка, в которой значение счетчика  моточасов равно текущему значению наработки


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
        hours_df.loc[indexes_maint_job, ['maint_job']] = hours_df.loc[indexes_maint_job, ['maint_job']] + [[maintanance_name]]
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
    # name_file = 'temp_files/hours_df' + eo_code + ".csv"
    # hours_df.to_csv(name_file)

    # hours_df.to_csv(name_file)
  
    print("Данные для ео ", eo_code, 'добавлены в модель')
  
  counter_year_df = pd.DataFrame(year_counter_df_list)
  counter_year_df['year'] = counter_year_df['datetime'].dt.year
  counter_year_df.to_csv('output_data/counter_year.csv', index = False)
  
  ktg_data_df.to_csv('output_data/ktg_data_df.csv', index = False, decimal = ",")

  ##########################################
 
  full_eo_list_for_merge = full_eo_list.loc[:,['eo_code', 'level_1_description', 'eo_class_description','eo_model_name', 'eo_description']]


  
  maintanance_jobs_df_total_data['year_of_operation'] = maintanance_jobs_df_total_data['day_of_opearation']/365
  maintanance_jobs_df_total_data['year_of_operation'] = maintanance_jobs_df_total_data['year_of_operation'].apply(np.floor)+1

  
  
  maintanance_jobs_df_ = pd.merge(maintanance_jobs_df_total_data, full_eo_list_for_merge, on = 'eo_code', how='left')
  maintanance_jobs_df_.sort_values(['maintanance_start_datetime'], inplace=True)
  maintanance_jobs_df_['man_hours'] = maintanance_jobs_df_['man_hours'].astype(str)
  maintanance_jobs_df_['man_hours'] = (maintanance_jobs_df_['man_hours'].str.split()).apply(lambda x: float(x[0].replace(',', '')))
  maintanance_jobs_df_['year'] = maintanance_jobs_df_['maintanance_start_datetime'].dt.year
  maintanance_jobs_df_['month'] = maintanance_jobs_df_['maintanance_start_datetime'].dt.month
  
  maintanance_jobs_df_.to_csv('temp_files/maintanance_jobs_df.csv', decimal=",")


  # maintanance_jobs_df_.to_csv('output_data/maintanance_jobs_df.csv', decimal=",", index = False)
      

def update_ktg_data_df():
  try:
    yad_file_name = "ktg_data_df.csv"
    yad.get_file(yad_file_name)
    ktg_data_df_yad = pd.read_csv("temp_files/df.csv", decimal = ",")
    print("ktg_data_df_yad получен")
    # удаляем файл из временной папки
    
    yad.delete_file("temp_files/df.csv")
    print("ktg_data_df_yad удален")
    # удаляем строки с ео, которые есть в рассчитанном файле
    updated_ktg_data_df = pd.read_csv('output_data/ktg_data_df.csv', decimal = ",")
    eo_list = list(set(updated_ktg_data_df['eo']))
    ktg_data_df_yad = ktg_data_df_yad.loc[~ktg_data_df_yad['eo'].isin(eo_list)]
    # добавляем строки 
    ktg_data_df_yad = pd.concat([ktg_data_df_yad, updated_ktg_data_df])
    # сохраняем новый файл
    ktg_data_df_yad.to_csv('temp_files/ktg_data_df_yad.csv', index = False, decimal = ',')
    print('ktg_data_df_yad обновлен')
    # загружаем файл в yad
    yad.upload_file('temp_files/ktg_data_df_yad.csv', 'ktg_data_df.csv')
    print("ktg_data_df_yad выгружен")
    yad.delete_file("temp_files/ktg_data_df_yad.csv")
    print("ktg_data_df_yad удален")
    
    return ktg_data_df_yad
  except Exception as e:
    print('не удалось скачать файл ktg_data_df.csv', e)  


def update_maintanance_jobs_df():
  try:
    yad_file_name = "maintanance_jobs_df.csv"
    yad.get_file(yad_file_name)
    maintanance_jobs_df_yad = pd.read_csv("temp_files/df.csv", decimal = ",", low_memory=False)
    
    print("update_maintanance_jobs_df(). maintanance_jobs_df_yad прочитан")
    # удаляем файл из временной папки
    # удаляем строки с ео, которые есть в рассчитанном файле
    yad.delete_file("temp_files/df.csv")

    updated_maintanance_jobs_df = pd.read_csv('temp_files/maintanance_jobs_df.csv', decimal = ",")
    eo_list = list(set(updated_maintanance_jobs_df['eo_code']))
    maintanance_jobs_df_yad = maintanance_jobs_df_yad.loc[~maintanance_jobs_df_yad['eo_code'].isin(eo_list)]
    # добавляем строки 
    maintanance_jobs_df_yad = pd.concat([maintanance_jobs_df_yad, updated_maintanance_jobs_df])
    # сохраняем новый файл
    maintanance_jobs_df_yad.to_csv('temp_files/maintanance_jobs_df_yad.csv', index = False, decimal = ',')
    print("update_maintanance_jobs_df() maintanance_jobs_df обновлен")
    # загружаем файл в yad
    yad.upload_file('temp_files/maintanance_jobs_df_yad.csv', 'maintanance_jobs_df.csv')
    print("update_maintanance_jobs_df() maintanance_jobs_df выгружен в yad")
    yad.delete_file('temp_files/maintanance_jobs_df_yad.csv')
    print('update_maintanance_jobs_df() maintanance_jobs_df_yad удален из temp_files')
    
   
  except Exception as e:
    print('ошибка в update_maintanance_jobs_df: ', e)
    

def maintanance_jobs_df_short_prepare():    
  maintanance_jobs_df = pd.read_csv('temp_files/maintanance_jobs_df.csv', decimal=",")
  # maintanance_jobs_df = yad.maintanance_jobs_df_download()
  # print(maintanance_jobs_df.info())
  
  maintanance_jobs_df_short = maintanance_jobs_df.loc[:, ['level_1_description','eo_class_description', 'eo_model_name','eo_description', 'eo_code', 'maintanance_category_id', 'maintanance_name', 'interval_motohours','maintanance_start_datetime','maintanance_finish_datetime','downtime','man_hours','motohours_value', 'year', 'month', 'year_of_operation']]
  maintanance_jobs_df_short['count'] = 1
  # нужно убрать значения с точкой в полях с датой
  
  
  maintanance_jobs_df_short['maintanance_finish_datetime'] = pd.to_datetime(maintanance_jobs_df_short['maintanance_finish_datetime'])
  maintanance_jobs_df_short['maintanance_start_datetime'] = pd.to_datetime(maintanance_jobs_df_short['maintanance_start_datetime'])
  
  maintanance_jobs_df_short['maintanance_finish_datetime'] = maintanance_jobs_df_short['maintanance_finish_datetime'].dt.strftime("%Y-%d-%m %H:%M:%S")

  
  maintanance_jobs_df_short['man_hours'] = maintanance_jobs_df_short['man_hours'].astype(float)
  maintanance_jobs_df_short['year_of_operation'] = maintanance_jobs_df_short['year_of_operation'].astype(int)
  
  maintanance_jobs_df_short_renamed = maintanance_jobs_df_short.rename(columns=initial_values.rename_columns_dict)
  

  maintanance_jobs_df_short_renamed.to_csv('output_data/sac_report_maintanance_jobs.csv', decimal=",")
  
  
  print("output_data/maintanance_jobs_df_short.csv записан")

  
  return maintanance_jobs_df_short

def number_of_eo_by_years():
  try:
    # yad_file_name = "maintanance_jobs_df.csv"
    # yad.get_file(yad_file_name)
    # maintanance_jobs_df= pd.read_csv("temp_files/df.csv", decimal = ",", low_memory=False)
    maintanance_jobs_df= pd.read_csv("temp_files/maintanance_jobs_df.csv", decimal = ",", low_memory=False)
  
    maintanance_jobs_df['count'] = 1
    # print("maintanance_jobs_df_yad прочитан")
    # удаляем файл из временной папки
    # yad.delete_file("temp_files/df.csv")
    # print("maintanance_jobs_df_yad удален")
  except Exception as e:
    print("в def number_of_eo_by_years() не удалось загрузить maintanance_jobs_df", e)
  
  groupped_maintanance_jobs_df = maintanance_jobs_df.groupby(['level_1_description','eo_class_description', 'eo_model_name','year', 'month', 'eo_code'], as_index = False)[['count']].max()
  groupped_maintanance_jobs_df.to_csv('temp_files/groupped_maintanance_jobs_df.csv')
  
  number_of_eo_month_year = groupped_maintanance_jobs_df.groupby(['year', 'month','level_1_description','eo_class_description', 'eo_model_name'], as_index = False)[['count']].sum()
  number_of_eo_month_year['month_year'] = number_of_eo_month_year['month'].astype('str') + "_" + number_of_eo_month_year['year'].astype('str')

  
  number_of_eo_year = number_of_eo_month_year.loc[number_of_eo_month_year['month']==12]
  
  number_of_eo_year = number_of_eo_year.loc[:, ['year', 'level_1_description', 'eo_class_description', 'eo_model_name', 'count']]
  number_of_eo_year = number_of_eo_year.rename(columns=initial_values.rename_columns_dict)
	
  number_of_eo_month_year = number_of_eo_month_year.rename(columns=initial_values.rename_columns_dict)	
  
  number_of_eo_month_year.to_csv('output_data/number_of_eo_month_year.csv', index = False)
  print("output_data/number_of_eo_month_year.csv записан")
  number_of_eo_year.to_csv('output_data/number_of_eo_year.csv', index = False)
  print("output_data/number_of_eo_year.csv записан")



def zip():
  files = ["output_data/sac_report_maintanance_jobs.csv", 
           "output_data/number_of_eo_year.csv",
           "output_data/number_of_eo_month_year.csv",
           "ktg_data_df.csv"
          ]
  archive = "output_data/sac_report_maintanance_jobs.zip"

  with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
      for file in files:
          zf.write(file)
  for file in files:
    yad.delete_file(file)
  
# func_eo_job_catalague_prep.eo_job_catologue()
# maint_records_generator()
# update_ktg_data_df() 
# update_maintanance_jobs_df()
# yad.delete_file('temp_files/maintanance_jobs_df.csv')
# maintanance_jobs_df_short_prepare()
number_of_eo_by_years()
