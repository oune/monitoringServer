import pandas as pd
import numpy as np
from numpy import random
import matplotlib.pyplot as plt
from typing import List
import asyncio
from configparser import ConfigParser
from model import Model
import pickle

class ErrorData():
    
    def __init__(self):
        self.df = pd.read_csv('error_data.csv')

        mean_df = self.df.mean()
        std_df = self.df.std()
        self.df = (self.df-mean_df)/std_df
        self.cursor = 0
        
    def getItem(self,index):
        return self.df.loc[index]
    
    def getNext(self):
        if self.cursor > len(self.df):
            return None
        value = self.df.loc[self.cursor:self.cursor+383]
        self.cursor += 383
        return value

    
conf = ConfigParser()
conf.read('resource/config.ini')
model_path = conf['model']['score_model']
init_data_path = conf['model']['calc_init']
reg_model_path = conf['model']['time_model']
db_1_path = conf['database']['machine1']
db_2_path = conf['database']['machine2']
raw_directory = conf['csv']['directory']
model_sampling_rate = int(conf['model']['rate'])
model_batch_size = int(conf['model']['batch_size'])
threshold = int(conf['model']['threshold'])
send_sampling_rate = int(conf['server']['sampling_rate'])
is_test = conf['test']['is_test']

model = Model(model_path, init_data_path, reg_model_path)

with open(init_data_path, "rb") as fr:
    init_data = pickle.load(fr)

    
def get_score(score):
    x = (score - init_data['mean'])
    return np.matmul(np.matmul(x, init_data['std']), x.T)

error = ErrorData()
df = pd.DataFrame(columns= ['name','score','remain_time','anomaly','threshold','left','right','temp'])

async def model_req(left: List[float], right: List[float], temp: List[float],name:str):
    try:
        score, exp_time = await model.get_model_res(left,right,temp)
        score = get_score(score)
        anomaly = score >= threshold
        message = {
            'name': name,
            'score': score,
            'remain_time': exp_time,
            'anomaly': bool(anomaly),
            'threshold': threshold
        }
        df.loc[len(df)] = [name,score,exp_time,anomaly,threshold,list(left.values), list(right.values), list(temp.values)]
        print(message)
        #await sio.emit('model', message)
    except Exception as e:
        print(e)




if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        count = 0
        d = error.getNext()
        while(len(d) == 384):
            d = error.getNext()
            left = d['left']
            right = d['right']
            temp = d['temp']
            
            loop.run_until_complete(model_req(left,right,temp,'test'))
        df.to_csv('log.csv',index=False)
    except Exception as e:
        print(e)