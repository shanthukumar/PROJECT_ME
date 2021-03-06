# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
print(__doc__)
              

import numpy as np
import scipy as sp
import pandas as pd
from subprocess import check_output

import time, json
from datetime import date

import time
import math
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.recurrent import LSTM
import numpy as np
import pandas as pd
import sklearn.preprocessing as prep
import matplotlib.pylab as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib.pylab import rcParams


# %%
df= pd.read_csv('groupeddf.csv')
df4=df.set_index("Code")


# %%
uniqueVals = df["Code"].unique() 


# %%
grouped_df=pd.DataFrame()
for i in uniqueVals:
    df5 = (df4.loc[i,:]).groupby(['Code','Date']).mean()
    # store DataFrame in list
    grouped_df=grouped_df.append(df5)
grouped_df.reset_index()
del df5


# %%
def create_dataset(dataset,past=5): # relating 5th day and 1st day
    dataX, dataY = [], []
    for i in range(len(dataset)-past-1):
        j = dataset[i:(i+past), 0]
        dataX.append(j)
        dataY.append(dataset[i + past, 0])
    return np.array(dataX), np.array(dataY)


# %%
from sklearn.preprocessing import MinMaxScaler
def testandtrain(prices):
    prices = prices.reshape(len(prices), 1)
    prices.shape
    scaler = MinMaxScaler(feature_range=(0, 1))
    prices = scaler.fit_transform(prices)
    trainsize = int(len(prices) * 0.80)
    testsize = len(prices) - trainsize
    train, test = prices[0:trainsize,:], prices[trainsize:len(prices),:]
    print(len(train), len(test))
    x_train,y_train = create_dataset(train,1)
    x_test,y_test = create_dataset(test,1)
    x_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1]))
    x_test = np.reshape(x_test, (x_test.shape[0], 1, x_test.shape[1]))
    
    return x_train,y_train, x_test,y_test


# %%
def trainingmodel(model, trainX, trainY):
    model = Sequential()
    model.add(LSTM(20, input_shape=(1,1)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='rmsprop')
    model.fit(trainX, trainY, epochs=10, batch_size=1, verbose=2)
    return model


# %%
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler

def predicting(prices, testX,testY,trainX):
    scaler = MinMaxScaler(feature_range=(0, 1))
    prices = prices.reshape(len(prices), 1)
    prices.shape
    scaler = MinMaxScaler(feature_range=(0, 1))
    prices = scaler.fit_transform(prices)
    
    testPredict = model.predict(testX)

    error = math.sqrt(mean_squared_error(testY, testPredict))
    print('Test RMSE: %.3f' % error)
    
    
    plt.plot(testPredict,color="blue",label='predicted')
    plt.plot(testY,color='red',label='expected')
    plt.xlabel("Days")
    plt.ylabel("Prices")
    plt.legend(loc=0)
    plt.title('Predicted prices VS Expected prices ')
    plt.show()
    return testPredict
 


# %%
for val in uniqueVals[1:2]:
    df1=grouped_df.loc[val,:]
    df2=df1.reset_index()
    prices = df2['Close'].values.astype('float32')

    model = Sequential()   
    trainX, trainY, testX, testY=testandtrain(prices)
    model = trainingmodel(model, trainX, trainY)
    model.summary()
    predictingY=predicting(prices,testX,testY,trainX)
    
    
       
    


# %%



