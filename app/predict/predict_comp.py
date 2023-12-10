#!/usr/bin/env python
#-*- coding: utf-8 -*-

from tensorflow import keras
import numpy as np

from .module.read_csv import read_file
from .module.csi_data_process import CsiDataProcess

# constant definition
MODEL = 'app/predict/model/LSTM_model.hdf5'
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

  probs = model.predict(predict_data, batch_size=1)

  ans = {"sitdown":0, "standup":0, "fall":0, "walk":0}
  for prob, dict_key in zip(probs[0], ans.keys()):
    ans[dict_key] = str(prob)
  
  sorted_ans = sorted(ans.items(), key=lambda x:x[1], reverse=True)

  sorted_ans = dict(sorted_ans)

  pred_result = next(iter(sorted_ans))
  prob_result = str(sorted_ans)

  return pred_result, prob_result