#!/usr/bin/env python
#-*- coding: utf-8 -*-

import collections
import math
import pandas as pd
import numpy as np
from tqdm.contrib import tzip

class CsiDataProcess:
  
  def __init__(self, max_data_size):
    self.type = type
    self.max_data_size = max_data_size
    self.wave_num = 0
    self.perm_amp = collections.deque(maxlen=max_data_size)
    self.perm_phase = collections.deque(maxlen=max_data_size) 
  
  def get_data(self, df_csi):
    df_processed_csi = pd.DataFrame(columns=["amp_by_point", "phase_by_point", "amp_by_wave", "phase_by_wave", "time", "timelag"])
    all_data = df_csi["data"].to_list()
    index = df_csi.index.tolist()
    times = df_csi["time"].to_list()
    timelags = df_csi["timelag"].to_list()

    for data, file_name, time, timelag in tzip(all_data, index, times, timelags):
      self.perm_phase = collections.deque(maxlen=self.max_data_size)
      self.perm_amp = collections.deque(maxlen=self.max_data_size)
      
      perm_amps, perm_phases = self.__get_processed_data(data)
      amp_waves, phase_waves = self.__covert_point_to_wave(perm_amps, perm_phases)
      
      amp_by_wave = []
      phase_by_wave = []
      for amp_wave, phase_wave in zip(amp_waves, phase_waves):
        amp_by_wave.append(list(np.array_split(amp_wave, len(amp_wave)/self.max_data_size)))
        phase_by_wave.append(list(np.array_split(phase_wave, len(phase_wave)/self.max_data_size)))
      
      time = list(np.array_split(time, len(time)/self.max_data_size))
        
      df_processed_csi.loc[file_name] = [perm_amps, perm_phases, amp_by_wave, phase_by_wave, time, timelag]
    return df_processed_csi
  
  def __covert_point_to_wave(self, amp_groups, phase_groups):
    amp_wave = [[] for x in range(self.wave_num)]
    phase_wave = [[]for x in range(self.wave_num)]
    
    count = 0
    for amp_group, phase_group in zip(amp_groups, phase_groups):
      for amp_point, phase_point in zip(amp_group, phase_group):
        for i,(one_amp, one_phase) in enumerate(zip(amp_point, phase_point)):
          amp_wave[i].append(one_amp)
          phase_wave[i].append(one_phase)
    return amp_wave, phase_wave
  
  def __get_processed_data(self, data):
    perm_amps = []
    perm_phases = []

    for d in data:
      self.__process(d)
      if len(self.perm_amp) == self.max_data_size:
        perm_amps.append(self.perm_amp)
        self.perm_amp = collections.deque(maxlen=self.max_data_size)
      if len(self.perm_phase) == self.max_data_size:
        perm_phases.append(self.perm_phase)
        self.perm_phase = collections.deque(maxlen=self.max_data_size)
    
    if len(self.perm_amp) > 0: perm_amps.append(self.perm_amp)
    if len(self.perm_phase) > 0: perm_phases.append(self.perm_phase)
    
    return perm_amps, perm_phases

  def __process(self, data):
    #Parser
    csi_data = data.split(',')
    csi_data[0] = csi_data[0].replace("[", "")
    csi_data[-1] = csi_data[-1].replace("]", "")
    csi_data.pop()
    csi_data = [int(c) for c in csi_data if c]
    imaginary = []
    real = []
    for i, val in enumerate(csi_data):
        if i % 2 == 0:
            imaginary.append(val)
        else:
            real.append(val)

    csi_size = len(csi_data)
    self.wave_num = int(csi_size/2)
    amplitudes = []
    phases = []
    if len(imaginary) > 0 and len(real) > 0:
        for j in range(int(csi_size / 2)):
            amplitude_calc = math.sqrt(imaginary[j] ** 2 + real[j] ** 2)
            phase_calc = math.atan2(imaginary[j], real[j])
            amplitudes.append(amplitude_calc)
            phases.append(phase_calc)

        self.perm_phase.append(phases)
        self.perm_amp.append(amplitudes)
        