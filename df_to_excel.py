import pandas as pd

def df_to_excel(dict_of_dfs):
  """на входе - list с dfs. на выходе - эксель файл в котором во вкладках каждый df"""
  with pd.ExcelWriter('temp_files/output.xlsx') as writer:
    for key in dict_of_dfs:
      sheet_name = key
      df = dict_of_dfs[key]
      df.to_excel(writer, sheet_name=sheet_name, index = False)




# df1 = pd.read_csv('data/level_1.csv')
# df2 = pd.read_csv('data/level_upper.csv')
# df_dict = {"level_1":df1, "level_upper":df2}
# df_to_excel(df_dict)