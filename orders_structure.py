import pandas as pd

# изучаем структуру по видам заказов

iw_39_full = pd.read_csv('data/uploaded_iw_39_df.csv')
iw_39_2022 = iw_39_full.loc[iw_39_full['basis_start_year'] == 2022]


#iw_39_order_category_distribution = iw_39_2022.groupby(['basis_start_monthname_year', 'basis_start_month'], as_index=False)[[
#  'ТЗКР; Технически закрыто', 
#  'ПДТВ; Подтверждено'
#  ]].sum()

iw_39_order_category_distribution = iw_39_2022.groupby(['basis_start_monthname_year', 'basis_start_month', 'Вид_заказа'], as_index=False)[['count']].sum()

iw_39_order_category_distribution.to_csv('data/iw_39_order_category_distribution.csv')

# iw_39_order_category_distribution.sort_values(by=['basis_start_month'],ignore_index=True, inplace = True)

# iw_39_order_category_distribution = iw_39_order_category_distribution.T
# print(type(iw_39_order_category_distribution))
# iw_39_order_category_distribution.to_csv('data/iw_39_order_category_distribution.csv', header=None)

# user_plan_df = customer_plan_df.groupby(['user_id'], as_index=False)[['visit_plan']].sum()

# fact_df = events_fact_df.groupby(['user_id'], as_index=False)['qty'].sum()



# python orders_structure.py