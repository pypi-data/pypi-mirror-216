#!/usr/bin/env python3
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import joblib
import numpy as np
from pkg_resources import resource_filename
import fire, warnings
from dataclasses import dataclass

@dataclass
class Regbot:
  asks: float
  bids: float
  grad_hist: float
  rsi_05: float
  rsi_15: float
  close_grad: float
  close_grad_neg: float

  reg_model_path: str = resource_filename(__name__, 'minute_model.h5')
  scaler_path: str = resource_filename(__name__, 'minutescaler.gz')

  def loadmodel(self):
    try:
      return joblib.load(open(f'{self.reg_model_path}', 'rb'))
    except Exception as e:
      return {
        'Error': e
      }


  def prepareInput(self):
    try:
      test_data = np.array([[self.asks,self.bids,self.grad_hist,self.rsi_05,self.rsi_15,self.close_grad,
                            self.close_grad_neg]])
      scaler = joblib.load(f'{self.scaler_path}')
      return scaler.transform(test_data)
    except Exception as e:
      return {
        'Error': e
      }


  def buySignalGenerator(self):
    try:
      return (self.loadmodel().predict_proba(self.prepareInput())[:,1][0])
    except Exception as e:
      return {
        'Error': e
      }



def signal(asks,bids,grad_hist,rsi_05,rsi_15,close_grad,close_grad_neg):
  try:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        return Regbot(asks,bids,grad_hist,rsi_05,rsi_15,close_grad,close_grad_neg).buySignalGenerator()
  except Exception as e:
    return {
      'Error': e
    }


if __name__ == '__main__':
  fire.Fire(signal)
