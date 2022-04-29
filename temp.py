import pandas as pd
import functions
import initial_values
import functions
from datetime import timedelta


# sac_report_maintanance_jobs = pd.read_csv('temp_files/df.csv')
full_eo_list_actual = pd.read_csv('temp_files/full_eo_list_actual.csv', dtype = str)

new_eo_df_for_update = pd.read_csv('temp_files/new_eo_df - new_eo_df.csv', dtype = str)
new_eo_df_for_update['operation_start_date'] = pd.to_datetime(new_eo_df_for_update['operation_start_date'])
for row in new_eo_df_for_update.itertuples():
  operation_start_date = getattr(row, "operation_start_date")
  index_new_eo_df_for_update = row.Index
  new_eo_df_for_update.loc[index_new_eo_df_for_update, ['operation_finish_date']] = operation_start_date + timedelta(days = 3650)

# print(new_eo_df_for_update['operation_start_date'])
new_eo_df_for_update.to_csv('temp_files/new_eo_df_for_update.csv')  

full_eo_list_updated = pd.concat([full_eo_list_actual,new_eo_df_for_update])
full_eo_list_updated.to_csv('temp_files/full_eo_list_updated.csv')
# full_eo_list_actual = full_eo_list_actual.loc[full_eo_list_actual['eo_model_name'] !="no_data"]
# full_eo_list_actual = full_eo_list_actual.loc[full_eo_list_actual['level_1_description'] !="Сухой Лог"]

# список ео в текущем списоке 
# current_eo_list = list(full_eo_list_actual['eo_code'])
# eo_list_sap_2604 = pd.read_csv('temp_files/eo_list_sap_2604.csv', dtype = str)
# new_eo_df =  eo_list_sap_2604.loc[~eo_list_sap_2604['eo_code'].isin(current_eo_list)]
# new_eo_df.to_csv('temp_files/new_eo_df.csv')

# print(eo_list_sap_2604.info())
# eo_list_sap_2604 = eo_list_sap_2604.loc[:, ['eo_code', 'ДатВвода в эксплуат.']]
# eo_list_sap_2604['ДатВвода в эксплуат.'] = pd.to_datetime(eo_list_sap_2604['ДатВвода в эксплуат.'])
# full_eo_list_actual = pd.merge(full_eo_list_actual, eo_list_sap_2604, on='eo_code', how = 'left')
# full_eo_list_actual.to_csv('temp_files/eo_list_actual.csv', index = False)
# print(eo_list_sap_2604)

# full_eo_list = functions.full_eo_list_func()

# ktg_data = pd.read_csv('temp_files/df.csv')
# full_eo_list_for_merge = full_eo_list.loc[:,['eo_code', 'level_1_description', 'eo_class_description','eo_model_name', 'eo_description']]
# ktg_data_df = pd.merge(ktg_data, full_eo_list_for_merge, left_on='eo', right_on='eo_code', how='left')
# ktg_data_df = ktg_data_df.rename(columns=initial_values.rename_columns_dict)
# ktg_data_df.drop(['eo'], axis=1, inplace=True)
# ktg_data_df.to_csv('output_data/ktg_data_df.csv', index = False, decimal = ",")

# sac_report_maintanance_jobs = pd.read_csv('output_data/sac_report_maintanance_jobs.csv')
# print(len(list(set(sac_report_maintanance_jobs['ЕО']))))

# full_eo_list_act = functions.full_eo_list_actual_func()
# print(full_eo_list_act.info())

# updated_eo_df = pd.read_csv('temp_files/eo_list_sap_2604.csv', dtype = str)

# updated_eo_df['ДатВвода в эксплуат.'] = pd.to_datetime(updated_eo_df['ДатВвода в эксплуат.'])
# print(updated_eo_df.info())


# минимально необходимые поля: "eo_code" "eo_description" Техническое место "Центр затрат"	"Название Центра затрат" "Наименование БЕ"
# 

# eo_rename_dict = {"Единица оборудования": "eo_code", "Название технического объекта":"eo_description", "Техническое место": }



# print(updated_eo_df.info())

# добавляем в df новые ео
# Список новых ео
# eo_list = list(full_eo_list_act['eo_code'])
# new_eo_df = pd.read_csv('temp_files/eo_ih08_25_04.csv', dtype = str)
# new_eo_df['operation_start_date'] = pd.to_datetime(new_eo_df['operation_start_date'])
# print(new_eo_df.info())
# new_eo = updated_eo_df.loc[~updated_eo_df['eo_code'].isin(eo_list)]
# new_eo.to_csv('temp_files/new_eo.csv')
# new_eo_df = new_eo.loc[:, ['eo_code']]
# print(new_eo_df)
# updated_eo_df = pd.concat([full_eo_list_act, new_eo_df])
# updated_start_operation_date_df = new_eo.loc[:, ['eo_code', 'ДатВвода в эксплуат.']]

# full_eo_df = pd.merge(updated_eo_df, updated_start_operation_date_df, on = 'eo_code', how = 'left')

# print(updated_eo_df.info())
# full_eo_df.to_csv('temp_files/full_eo_df.csv')

