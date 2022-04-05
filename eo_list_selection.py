import functions
import initial_values

#############################################################################################
def select_eo_for_calculation():
  """Выборка ео из полного списка full_eo_list_actual в full_eo_list"""
  maintanance_job_list_general_df = functions.maintanance_job_list_general_func()
  
  strategy_list = list(set(maintanance_job_list_general_df['strategy_id']))

  full_eo_list = functions.full_eo_list_actual_func()
  full_eo_list['strategy_id'] = full_eo_list['strategy_id'].astype(int)
  maintanance_job_list_general_df['strategy_id'] = maintanance_job_list_general_df['strategy_id'].astype(int)
    
  full_eo_list = full_eo_list.loc[full_eo_list['strategy_id'].isin(strategy_list)]
  # режем выборку по датам ввод и вывда из эксплуатации
  first_day_of_selection = initial_values.first_day_of_selection
  last_day_of_selection = initial_values.last_day_of_selection

  full_eo_list = full_eo_list.loc[full_eo_list['operation_start_date']<last_day_of_selection]
  full_eo_list = full_eo_list.loc[full_eo_list['operation_finish_date']>first_day_of_selection]
  
  
  full_eo_list.to_csv('data/full_eo_list.csv', index=False)
  return full_eo_list
  #################
# select_eo_for_calculation()