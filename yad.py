import yadisk
import os
import pandas as pd
import zipfile

y = yadisk.YaDisk(token="AQAAAABfSJVEAAfMGMams7U1xkJGgxmm7sinToc")

try:
  y.check_token()
except:
  print("не удалось подрубиться к ядиску")
# print(y.check_token()) # Проверим токен


def upload_file(file_path, file_name):
  try:
    y.upload(file_path, file_name, overwrite = True)
    print("Файл ", file_name, " успешно выгружен")
  except Exception as e:
    print('не получилось upload_file ', file_name, " Ошибка: ", e)


# upload_file('temp_files/full_eo_list_actual.csv', 'full_eo_list_actual.csv')
# upload_file('output_data/ktg_data_df.csv', 'ktg_data_df.csv')
# upload_file('output_data/sac_report_maintanance_jobs.csv', 'sac_report_maintanance_jobs.csv')
    
    
# Получает общую информацию о диске
# print(y.get_disk_info())
# print(list(y.listdir("/")))

      
# y.mkdir("/test") # Создать папку
# y.upload("temp_files/maintanance_jobs_df.csv", "maintanance_jobs_df.csv") # Загружает первый файл
# y.upload("file2.txt", "/test/file2.txt") # Загружает второй файл

def get_file(file_name):
  try:
    y.download(file_name, "temp_files/df.csv")
  except Exception as e:
    print("не получилось get_file", e)

# get_file("maintanance_jobs_df.csv")
get_file("full_eo_list_actual.csv")
# get_file("ktg_data_df.csv")
# get_file("sac_report_maintanance_jobs.csv")
    
    
# df = pd.read_csv('temp_files/df.csv')
# print(df.info())

def delete_file(file_path):
  try:
    os.remove(file_path)
    print("Файл ", file_path, " удален")
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


# теперь в яд мы будем отправлять не файлы, а архив
# делаем первичную загрузку архива
# получаем с яд maintanance_jobs_df
# get_file("full_eo_list_actual.csv")


# upload_file("output_data/maintanance_jobs_df.zip", "maintanance_jobs_df.zip")

# file_names_list = ["eo_job_catologue", "full_eo_list_actual", "ktg_data_df", "maintanance_jobs_df", "number_of_eo_month_year",  "number_of_eo_year"]
# for file_name in file_names_list:
#   archive = "output_data/" + file_name + ".zip"
#   file_name_ = file_name + ".zip"
#   upload_file(archive, file_name_)
#   print(file_name, " выгружен")

# for file_name in file_names_list:
#   file_path = "output_data/" + file_name  + ".csv"
  
#   files_to_zip = [file_path]
#   archive = "output_data/" + file_name + ".zip"
#   with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
#     for file in files_to_zip:
#       zf.write(file)
def unzip():
  with zipfile.ZipFile('output_data/maintanance_jobs_df.zip', 'r') as zipObj:
     # Extract all the contents of zip file in current directory
     zipObj.extractall()
  
  upload_file("output_data/maintanance_jobs_df.csv", "maintanance_jobs_df.csv")
  delete_file("output_data/maintanance_jobs_df.csv")
  