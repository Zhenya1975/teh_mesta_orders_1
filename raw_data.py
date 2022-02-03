import pandas as pd

raw_data = pd.read_csv('data/raw_data.csv')
raw_data.dropna(subset=['object_class'], inplace=True)

# пусть в списке actions, будет список с действиям. 
# вручную заполняю список. а в принте проверяю где чего не хватает 
action_list = [
  'создал новую сделку',
  'установил компанию',
  'Создана новая задача',
  'создал событие календаря',
  'изменил этап сделки',
  'создал новый комментарий',
  'изменил значение в поле "Дата контрактации"',
  'изменил скидку на товар'
]
for index, row in raw_data.iterrows():
  description = row['description']
  for item in action_list:
    if item in description:
      raw_data.loc[index, 'action'] = item

raw_data.to_csv('data/raw_data.csv')
raw_data.fillna('no_data', inplace=True)

raw_data_filtered = raw_data.loc[raw_data['action'] == 'no_data']
print(raw_data_filtered['description'])