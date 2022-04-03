import yadisk
import os
y = yadisk.YaDisk(token="AQAAAABfSJVEAAfMGMams7U1xkJGgxmm7sinToc")

try:
  y.check_token()
except:
  print("не удалось подрубиться к ядиску")
# print(y.check_token()) # Проверим токен


def upload_file(file_path, file_name):
  y.upload(file_path, file_name, overwrite = True)

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


def delete_file():
  try:
    os.remove("temp_files/df.csv")
  except:
    pass
# get_file("maintanance_jo_df.csv")
# upload_file('data/job_list.csv', 'job_list.csv')