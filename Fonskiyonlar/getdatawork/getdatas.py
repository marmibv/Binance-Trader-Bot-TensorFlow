import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import websocket, json,threading, config, pandas as pd
from binance.client import Client
import Fonskiyonlar.sayfafonk.mainscreenfnc as mainscreenfnk
import Fonskiyonlar.TAAI.AI as AI
import Fonskiyonlar.TAAI.ftalib as fta
import pandas_ta as ta
from binance.enums import *
globaldatas = threading.local()
def binance_order(synbol, side, quantity, order_type=ORDER_TYPE_MARKET):
    if(False):
        try:
            print("Sending binance order")
            order = config.binance_client.create_order(synbol=synbol, side=side, quantity=quantity, type=order_type)
            print(order)
        except Exception as e:
            print("Hata oluştu")
            print(e)
    else:
        return False
def realTime(TradeSymbol,SOCKET,budget,oldtdatas, stoploss,karhedefi):
    globaldatas.budget_first = float(budget)
    globaldatas.kar_hedefi = float(karhedefi)
    globaldatas.stop_loss = float(stoploss)
    globaldatas.in_position = False
    globaldatas.budgetnow = float(budget)
    globaldatas.tradeBoyutu = float(0)
    globaldatas.real = True
    data_pandas = pd.DataFrame(columns = ['open', 'high', 'low', 'close', 'volume'])
    for x in range (1,len(oldtdatas) -1, +1):
        data_pandas = data_pandas.append(oldtdatas[x:x+1])
    print(data_pandas)
    def on_open(ws):
        print("bağlanıyor")
    def on_close(ws):
        print("bağlantı kapanıyor")
    def on_message(ws, message):
        print("mesaj alindi")
        json_message = json.loads(message)
        jsonkcolums = json_message['k']
        if(jsonkcolums['x']):
            data_pandas.loc[len(data_pandas)+1] = [jsonkcolums['o'], jsonkcolums['h'], jsonkcolums['l'], jsonkcolums['c'], jsonkcolums['v']] 
            data_pandas2=pd.DataFrame(columns=['open','high','low','close','volume'])
            data_pandas2 = data_pandas.astype(float)
            print(data_pandas2)
            for i in range(150,len(data_pandas2)):
                print(i,len(data_pandas2))
                if(len(data_pandas2)>150):
                    data_pandas2 = data_pandas2.drop(data_pandas2.index[0])
            print(data_pandas2)
            check_sell_or_buy(data_pandas2)
    ws = websocket.WebSocketApp(SOCKET, on_open = on_open, on_close=on_close, on_message=on_message)
    ws.run_forever()
def backtesting(budget, data, TradeSymbol, stoploss, karhedefi):   
    data_pandas = pd.DataFrame(columns = ['open', 'high', 'low', 'close', 'volume'])
    globaldatas.predicted_closes = []
    globaldatas.predicted_closes.append(0.0000)
    globaldatas.real = False
    globaldatas.budget_first = float(budget)
    globaldatas.kar_hedefi = float(karhedefi)
    globaldatas.stop_loss = float(stoploss)
    globaldatas.in_position = False
    globaldatas.budgetnow = float(budget)
    globaldatas.tradeBoyutu = float(0)
    loop = 0
    for x in range (1,len(data) -1, +1):
        data_pandas = data_pandas.append(data[x:x+1])
        if(len(data_pandas)> 110):
            print("Loop :"+str(loop))
            loop = loop +1
            check_sell_or_buy(data_pandas)
            if(len(data_pandas)>180):
                data_pandas = data_pandas.drop(data_pandas.index[0])
    print("done")
def check_sell_or_buy(data):
    tensow_df = AI.AI(fta.TA(data))
    predict_closes = tensow_df.iloc[-1,tensow_df.columns.get_loc('close')]
    from_closes = data.iloc[-2, data.columns.get_loc('close')]
    data_closes = data.iloc[-1, data.columns.get_loc('close')]
    globaldatas.predicted_closes.append(predict_closes)
    anisat = False
    inpositionbudget(data)
    if(globaldatas.in_position and globaldatas.budgetnow > globaldatas.budget_first + (globaldatas.budget_first * globaldatas.kar_hedefi/100)):
        globaldatas.budget_first = globaldatas.budgetnow
        anisat = True
        mainscreenfnk.tabPrint("karedildi")
    if(globaldatas.in_position and globaldatas.budget_first - (globaldatas.budget_first * globaldatas.stop_loss/100)) > (globaldatas.budgetnow):
        globaldatas.budget_first = globaldatas.budgetnow
        anisat = True
        mainscreenfnk.tabPrint("Satıldı")
    if(anisat):
        globaldatas.in_position = False
        globaldatas.budget_first = globaldatas.tradeBoyutu * data_closes
        mainscreenfnk.tabPrint("Ani Satıldı: "+ str(globaldatas.budget_first)+ " ---> "+str(data_closes)+" Predicted Close :"+str(globaldatas.predicted_closes[-2])+ " From >> :"+str(from_closes))
    if(predict_closes > data_closes and not globaldatas.in_position):
        mainscreenfnk.tabPrint("Al :"+ str(data_closes)+" Predicted Close :"+str(globaldatas.predicted_closes[-2])+ " From >> :"+str(from_closes))
        globaldatas.in_position = True
        globaldatas.tradeBoyutu = globaldatas.budget_first/ data_closes
    if(predict_closes < data_closes and globaldatas.in_position):
        globaldatas.in_position = False
        globaldatas.budget_first = globaldatas.tradeBoyutu * data_closes
        globaldatas.tradeBoyutu = 0
        mainscreenfnk.tabPrint("Sat: "+ str(globaldatas.budget_first)+ " ---> "+str(data_closes)+" Predicted Close :"+str(globaldatas.predicted_closes[-2])+ " From >> :"+str(from_closes))
def inpositionbudget(data):
    if(globaldatas.in_position):
        globaldatas.budgetnow = float(globaldatas.tradeBoyutu * data.iloc[-1, data.columns.get_loc('close')])  
