import yadisk
import os
import pandas as pd
y = yadisk.YaDisk(token="AQAAAABfSJVEAAfMGMams7U1xkJGgxmm7sinToc")

try:
  y.check_token()
except:
  print("не удалось подрубиться к ядиску")
# print(y.check_token()) # Проверим токен


def upload_file(file_path, file_name):
  y.upload(file_path, file_name, overwrite = True)


  
# upload_file('temp_files/df.csv', 'full_eo_list_actual.csv')
# upload_file('output_data/ktg_data_df.csv', 'ktg_data_df.csv')

# Получает общую информацию о диске
# print(y.get_disk_info())
# print(list(y.listdir("/")))

      
# y.mkdir("/test") # Создать папку
# y.upload("temp_files/maintanance_jobs_df.csv", "maintanance_jobs_df.csv") # Загружает первый файл
# y.upload("file2.txt", "/test/file2.txt") # Загружает второй файл

def get_file(file_name):
  try:
    y.download(file_name, "temp_files/df.csv")
  except:
    print("не получилось загрузить файл")

# get_file("maintanance_jobs_short.csv")
# get_file("full_eo_list_actual.csv")
# get_file("ktg_data_df.csv")



def delete_file(file_path):
  try:
    os.remove(file_path)
  except Exception as e:
    print("Не удалось удалить файл", e)
# get_file("/eo_job_catologue.csv")
# upload_file('data/job_list.csv', 'job_list.csv')

# upload_file('temp_files/maintanance_jobs_df.csv', 'maintanance_jobs_df.csv')
# delete_file('temp_files/maintanance_jobs_df.csv')

# upload_file('temp_files/maintanance_jobs_short.csv', 'maintanance_jobs_short.csv')
# delete_file('temp_files/maintanance_jobs_short.csv')

    

# РЕЕСТР
# full_eo_list_actual.csv
# maintanance_jobs_df.csv
# maintanance_jobs_short.csv

def maintanance_jobs_df_download():
  try:
    yad_file_name = "maintanance_jobs_df.csv"
    get_file(yad_file_name)
    maintanance_jobs_df_yad = pd.read_csv("temp_files/df.csv", decimal = ",", low_memory=False)
    print("maintanance_jobs_df получен и записан в df")
    # удаляем файл из временной папки
    delete_file("temp_files/df.csv")
    print("maintanance_jobs удален из временной папки")
    return maintanance_jobs_df_yad
  except Exception as e:
    print('не удалось скачать файл maintanance_jobs_df.csv')