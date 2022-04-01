import boto3
import os
import pandas as pd

# Create an S3 access object
s3 = boto3.client("s3")

# "maintanance_jobs_df.csv"

def get_file(file_name):
  s3.download_file(
      Bucket="pydatabucket", Key=file_name, Filename="temp_files/df.csv"
  )
  file_path = "temp_files/df.csv"
  # temp_df = pd.read_csv("temp_files/maintanance_jobs_df.csv")
  # print(temp_df.info())
  # os.remove("temp_files/maintanance_jobs_df.csv")
  return file_path

def delete_file():
  try:
    os.remove("temp_files/df.csv")
  except:
    pass

# получаем файл
maintanance_jobs_df = pd.read_csv(get_file("maintanance_jobs_df.csv"))
# удаляем файл
# delete_file()
# print(maintanance_jobs_df.info())