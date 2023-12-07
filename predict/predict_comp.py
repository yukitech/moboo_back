#!/usr/bin/env python
#-*- coding: utf-8 -*-

from tensorflow import keras
import numpy as np
import sys

sys.path.append('./predict')
from module.read_csv import read_file
from module.csi_data_process import CsiDataProcess

# constant definition
MODEL = 'predict/model/LSTM_model.hdf5'
MAX_TIMESTEP = 280
CLASS_NUM = 4

def pre_process(original_data, division_num):
  process = CsiDataProcess(int(MAX_TIMESTEP/division_num))
  processed_data = process.get_data(original_data)

  all_action_data = processed_data["phase_by_point"]
  data = []
  for action_data in all_action_data:
    for point_group in action_data:
      data.append(point_group)

  data = np.array(data, dtype=float)

  return data

def predict(csi_data_file, file_name):
  predict_original_data = read_file(csi_data_file, file_name)
  predict_data = pre_process(predict_original_data, 1)

  model = keras.models.load_model(MODEL)

  all_prob = model.predict(predict_data, batch_size=1)

  ans = []
  for probs in all_prob:
    labels = {"sitdown":0, "standup":1, "fall":2, "walk":3}
    for prob, dict_key in zip(probs, labels.keys()):
      labels[dict_key] = prob
    ans.append(labels)
  
  sorted_ans = []
  for dic in ans:
    sort_dict = sorted(dic.items(), key=lambda x:x[1], reverse=True)
    sorted_ans.append(sort_dict)
  
  for ans in sorted_ans:
    print('========================')
    for e in ans:
      print(str(e))
    print('========================')