import csv
import pandas as pd
from datetime import datetime

MAX_ROW_NUM = 280
    

def read_file(upload_file):
  csi = pd.DataFrame(columns=["data", "time", "timelag"])
  file_name = upload_file.name
  data = read_csv(upload_file)
  time = read_time(upload_file)
  time_lag = read_time_lag(upload_file)
  csi.loc[file_name] = [data, time, time_lag]
  return csi

def read_csv(csv_file):
  data = []
  with open(csv_file, encoding='utf-8') as fr:
    reader = csv.reader(fr)
    for row_num, row in enumerate(reader):
      if row_num <= MAX_ROW_NUM:
        data.append(row[-1])
    del data[0]
  return data

def read_time_lag(csv_file):
  time_lag = []
  time_format = '%Y-%m-%d %H:%M:%S.%f'

  with open(csv_file, encoding='utf-8') as fr:
    reader = csv.reader(fr)
    for row_num, row in enumerate(reader):
      if row_num == 0:
        continue

      original_data = datetime.strptime(row[0], time_format)
      if row_num == 1:
        previous_data = original_data
        continue

      if row_num <= MAX_ROW_NUM:
        data = original_data - previous_data
        data = data.total_seconds()
        time_lag.append(data)
        previous_data = original_data
  return time_lag

def read_time(csv_file):
  time = []
  time_format = '%Y-%m-%d %H:%M:%S.%f'

  with open(csv_file, encoding='utf-8') as fr:
    reader = csv.reader(fr)
    for row_num, row in enumerate(reader):
      if row_num == 0:
        continue

      original_data = datetime.strptime(row[0], time_format)
      if row_num == 1:
        start_time = original_data
      
      if row_num <= MAX_ROW_NUM:
        data = original_data - start_time
        data = data.total_seconds()
        time.append(data)
  return time