import pandas as pd
import functions
import maint_records_generator

# получаем данные о машинах

full_eo_list = functions.full_eo_list_func()
full_eo_list_selected = full_eo_list.loc[:, ['eo_code', 'operation_start_date', 'operation_finish_date']]

# получаем данные о maintanance_jobs_df_short
maintanance_jobs_df_short = maint_records_generator.maintanance_jobs_df_short_prepare()
maintanance_jobs_df_short['month_datetime'] = maintanance_jobs_df_short.to_datetime((maintanance_jobs_df_short['year'].astype(str) + maintanance_jobs_df_short['month'].astype(str)), format = '%Y%m')
