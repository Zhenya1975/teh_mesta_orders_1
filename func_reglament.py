import pandas as pd
import initial_values
import yad

def reglament_df():
  reglament_df = pd.read_csv('data/maintanance_job_list_general.csv')
  reglament_df = reglament_df.loc[:, ['upper_level_tehmesto_description', 'maintanance_code', 'maintanance_name', 'interval_type', 'interval_motohours', 'downtime_planned',	'man_hours',	'tr_downtime_start_value','tr_downtime_finish_value','tr_man_hours_start_value','tr_man_hours_finish_value','tr_start_motohour','tr_finish_motohour', 'pass_interval', 'go_interval']]
  reglament_df = reglament_df.rename(columns=initial_values.rename_columns_dict)
  # maintanance_jobs_short = yad.get_file('maintanance_jobs_short.csv')
  reglament_df.to_csv('output_data/reglament_df.csv', index = False)
  
  
  # print(reglament_df.info())
  # print(reglament_df.head())