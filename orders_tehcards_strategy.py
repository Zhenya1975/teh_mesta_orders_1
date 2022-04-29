import pandas as pd

orders_df = pd.read_csv('output_data/orders_sap.csv')
# print(orders_df.info())
orders_df['group_counter'] = orders_df['Группа'] + orders_df['СчетГруппТехкарт']
orders_df.to_csv('temp_files/orders_df.csv')

tehcards_df = pd.read_csv('output_data/tehcards.csv')
tehcards_df.to_csv('temp_files/tehcards_df.csv')
tehcards_df.drop(columns=['Группа'], inplace = True)

orders_tehcards_df = pd.merge(orders_df, tehcards_df, left_on = 'group_counter', right_on = 'группа_счетчик', how = 'left')
orders_tehcards_df.to_csv('temp_files/orders_tehcards_df.csv')