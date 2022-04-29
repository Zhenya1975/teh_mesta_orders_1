import pandas as pd
import functions


full_eo_list_actual = functions.full_eo_list_actual_func()
# print(full_eo_list_actual.info())
eo_ih08_25_04 = pd.read_csv('temp_files/eo_ih08_25_04.csv', dtype = str)
eo_ih08_25_04 = eo_ih08_25_04.loc[:, ['eo_code', 'operation_start_date']]
eo_ih08_25_04["operation_start_date"] = pd.to_datetime(eo_ih08_25_04["operation_start_date"])
# print(eo_ih08_25_04.info())
current_eo_list = list(full_eo_list_actual['eo_code'])
# список новых ео, которых ранее не было
new_eo_data = eo_ih08_25_04.loc[~eo_ih08_25_04['eo_code'].isin(current_eo_list)]
print()