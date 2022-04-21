import zipfile
import yad

def unzip(file_path, file_name):
  with zipfile.ZipFile(file_path, 'r') as zipObj:
     # Extract all the contents of zip file in current directory
     zipObj.extractall()
  df = pd.read_csv()
  # yad.upload_file(file_path, file_name)
  yad.delete_file(file_path)

unzip('output_data/maintanance_jobs_df.zip', "maintanance_jobs_df.csv")