import pandas as pd
from datetime import timedelta
import initial_values

default_resource_period_in_years = 10
# есть данные о парке техники в файле data_files/eo_data.csv
# первое что нужно сделать - ответить на вопрос. На конец кажого месяца начиная с конца апреля 2022 вперед до конца 2034 года нужно ответить на вопрос - какая машина в эксплуатации. Для этого для точки month_year нужно сказать ео в эксплуатации или нет.
# что на это влияет. Значение в поле дата начала эксплуатациии. дата месяца должна между датами начала и завершения эксплуатации.
report_period_start = pd.to_datetime('01.04.2022', format='%d.%m.%Y')
report_period_finish = pd.to_datetime('01.01.2034', format='%d.%m.%Y')
month_date_range = pd.date_range(start=report_period_start, end = report_period_finish,freq='MS')
date_range_df = pd.DataFrame(month_date_range, columns = ['reference_date'])
# print(date_range_df.info())
# print(pd.date_range(start=report_period_start, end = report_period_finish,freq='M'))

eo_data_df = pd.read_csv('py_v2/data_files/eo_data.csv', dtype = str)
eo_data_df["operation_start_date"] = pd.to_datetime(eo_data_df["operation_start_date"],format='%d.%m.%Y')
eo_data_df["operation_finish_date_sap"] = pd.to_datetime(eo_data_df["operation_finish_date_sap"], format='%d.%m.%Y')
eo_data_df["expected_operation_finish_date"] = pd.to_datetime(eo_data_df["expected_operation_finish_date"], format='%d.%m.%Y')


# print(eo_data_df.info())



# итерируемся по этому списку
result_df_data = []
for reference_date in month_date_range:
  reference_date = reference_date
  for row in eo_data_df.itertuples():
    temp_dict = {}
    
    # дефолтное значение статуса  -  'in_operation'
    operation_status = 'in_operation'
    eo_code = getattr(row, "eo_code")
    operation_start_date = getattr(row, "operation_start_date")
    operation_finish_date_sap = getattr(row, "operation_finish_date_sap")
    expected_operation_finish_date = getattr(row, "expected_operation_finish_date")
    
    temp_dict['eo_code'] = eo_code
    temp_dict['reference_date'] = reference_date
    temp_dict['operation_start_date'] = operation_start_date
    temp_dict['operation_finish_date_sap'] = operation_finish_date_sap
    temp_dict['expected_operation_finish_date'] = expected_operation_finish_date
    
    # если дата начала эксплуатации позже текущей референсной даты то меняем статус на 'planned'
    if operation_start_date > reference_date:
      operation_status = 'planned'
    
    # если в поле operation_finish_date_sap есть дата и эта дата раньше референсной даты, то меняем статус на 'finished'
    if operation_finish_date_sap == operation_finish_date_sap and operation_finish_date_sap < reference_date:
        operation_status = 'finished'

    # если в поле expected_operation_finish_date есть дата и эта дата раньше референсной даты, то меняем статус на 'finished'
    if expected_operation_finish_date == expected_operation_finish_date and expected_operation_finish_date < reference_date:
        operation_status = 'finished'

    # если и в поле operation_finish_date_sap и в поле expected_operation_finish_date пусто, то берем 
    # дефолтную дату и прибавляеям ее к дате начала эксплуатации и получаем теоритическую дату завершения
    if operation_finish_date_sap != operation_finish_date_sap and expected_operation_finish_date != expected_operation_finish_date:
      teorethic_finish_date = operation_start_date + timedelta(days = 366*default_resource_period_in_years)
      # если теоритическая дата меньше, чем 1 января 2023 года, то делаем конечную дату первым января 2023 года.
      if teorethic_finish_date < pd.to_datetime('01.01.2023', format='%d.%m.%Y'):
        teorethic_finish_date = pd.to_datetime('01.01.2023', format='%d.%m.%Y')
      temp_dict['teorethic_finish_date'] = teorethic_finish_date
        
      if teorethic_finish_date < reference_date:
        operation_status = 'finished'
      
    
    
    temp_dict['operation_status'] = operation_status
    result_df_data.append(temp_dict)

reference_dates_df = pd.DataFrame(result_df_data)
reference_dates_df['month'] = reference_dates_df['reference_date'].dt.month
reference_dates_df['year'] = reference_dates_df['reference_date'].dt.year
reference_dates_df['month_year'] = reference_dates_df['month'].astype(str) +"_" + reference_dates_df['year'].astype(str)
reference_dates_df['месяц_год'] = reference_dates_df['month_year'].map(initial_values.period_dict)
reference_dates_df['period_sort_index'] = reference_dates_df['month_year'].map(initial_values.period_sort_index)
reference_dates_df['period'] = reference_dates_df['period_sort_index'].astype(str) +"_" + reference_dates_df['месяц_год']


reference_dates_df = pd.merge(reference_dates_df, eo_data_df, on='eo_code', how = 'left')
reference_dates_df['count'] = 1

reference_dates_df.to_csv('py_v2/data_files/reference_dates_df.csv')

