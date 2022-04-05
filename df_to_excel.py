import pandas as pd

def df_to_excel(dict_of_dfs):
  """на входе - list с dfs. на выходе - эксель файл в котором во вкладках каждый df"""
  for key in dict_of_dfs:
    file_path = "temp_files/" + key + ".xlsx"
    sheet_name = key
    df = dict_of_dfs[key]
    with pd.ExcelWriter(file_path) as writer:
      df.to_excel(writer, sheet_name=sheet_name, index = False)
  
  
    
    




# df1 = pd.read_csv('data/level_1.csv')
# df2 = pd.read_csv('data/level_upper.csv')
# df_dict = {"level_1":df1, "level_upper":df2}
# df_to_excel(df_dict)