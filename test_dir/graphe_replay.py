import pickle
import numpy as np
import pandas as pd

FRAME_SIZE = 100

path = "replay.pkl"
with open(path, 'rb') as file:
    print("\t \t Loading processed data =========>>>>>>>>")
    df = pickle.load(file)

def get_rms_acceleration(signal):
    print("in rms")
    rms = []
    for i in range(0, len(signal), FRAME_SIZE):
        current_rms = np.sqrt(np.sum(signal[i:i+FRAME_SIZE]**2)/FRAME_SIZE)
        rms.append(current_rms)
    return rms




def rms_data():
    signal_b = get_rms_acceleration(df["acc_broche"])
    signal_t = get_rms_acceleration(df["acc_table"])
    data = {
        'rms_b': np.array(signal_b),
        'rms_t': np.array(signal_t)
    }
