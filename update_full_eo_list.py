import pandas as pd
import yad

# class_subclass_df = pd.read_csv("temp_files/class_subclass.csv")

# # список главных классов
# main_class_list = list(set(class_subclass_df['Код класса']))

# # итерируемся по списку классов
# for main_class in main_class_list:
#   # режем основной датафрейм
#   class_subclass_df_filtered = class_subclass_df.loc[class_subclass_df['Код класса'] ==main_class]
#   main_class_title_df = class_subclass_df.loc[class_subclass_df['Код класса подкласса'] ==main_class]
#   main_class_title = ""
#   try:
#     main_class_title = main_class_title_df.iloc[0]["Наименование класса"]
#   except Exception as e:
#     print("Исключение при попытке получить наименование класса", e)
#   # print(main_class_title)
#   indexes_list = class_subclass_df_filtered.index.values
#   # вставляем в исходную таблицу значения имени основного класса
#   class_subclass_df.loc[class_subclass_df.index[indexes_list],['Наименование основного класса']]=main_class_title
# class_subclass_df.to_csv('temp_files/class_subclass.csv')

# получаем full eo list

