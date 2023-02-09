import tensorflow as tf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import pandas as pd
from keras import regularizers
def AI(data):
    data = data.drop(data.index[:20]).reset_index(drop=True)
    data2 = data
    scaler = MinMaxScaler(feature_range=(0,1))
    data = scaler.fit_transform(data)
    timesteps = int(len(data)*0.7)
    X = []
    y = []
    for i in range(timesteps, data.shape[0]):
        X.append(data[i-timesteps:i,:])
        y.append(data[i,3])
    X, y = np.array(X), np.array(y)
    batch_size = 32
    dataset = tf.data.Dataset.from_tensor_slices((X, y)).batch(batch_size)
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.LSTM(64, input_shape=(timesteps, data.shape[1]),return_sequences=True, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.3))
    model.add(tf.keras.layers.Dense(8,kernel_regularizer=regularizers.l2(0.01)))
    model.add(tf.keras.layers.LSTM(32, return_sequences=False, activation = 'relu'))
    model.add(tf.keras.layers.Dropout(0.3))
    model.add(tf.keras.layers.Dense(1))
    model.compile(optimizer="adam", loss="mean_squared_error")
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
    model.fit(dataset, epochs=250, callbacks=[early_stopping], validation_data=(X,y))
    last_timesteps = data[-timesteps:, :]
    prediction = model.predict(last_timesteps.reshape(1, timesteps, data.shape[1]))
    print(prediction)
    prediction = np.concatenate([prediction]*9, axis=1)
    prediction = scaler.inverse_transform(prediction)
    print(prediction)
    df = pd.DataFrame(prediction, columns=['open','high','low','close','volume','RSI','CMF','MFI','EMA'])
    print(df)
    data2 = data2.append(df)
    data2.index = np.arange(0, len(data2))
    print(data2)
    return data2 #-> close[-1] = prediction close[-2]=real