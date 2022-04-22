import pandas as pd
import functions
import initial_values

# full_eo_list = functions.full_eo_list_func()

# ktg_data = pd.read_csv('temp_files/df.csv')
# full_eo_list_for_merge = full_eo_list.loc[:,['eo_code', 'level_1_description', 'eo_class_description','eo_model_name', 'eo_description']]
# ktg_data_df = pd.merge(ktg_data, full_eo_list_for_merge, left_on='eo', right_on='eo_code', how='left')
# ktg_data_df = ktg_data_df.rename(columns=initial_values.rename_columns_dict)
# ktg_data_df.drop(['eo'], axis=1, inplace=True)
# ktg_data_df.to_csv('output_data/ktg_data_df.csv', index = False, decimal = ",")

sac_report_maintanance_jobs = pd.read_csv('output_data/sac_report_maintanance_jobs.csv')
print(len(list(set(sac_report_maintanance_jobs['ЕО']))))