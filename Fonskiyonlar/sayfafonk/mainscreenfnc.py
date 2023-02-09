import main, Fonskiyonlar.getdatawork.getdatas as getdatas
import ctypes
from threading import *
from PyQt5 import QtCore, QtGui, QtWidgets 
import config, itertools, threading, datetime
import pandas as pd
from datetime import datetime

def design():
    main.UImain.tabWidget.setTabsClosable(True)
    main.UImain.tabWidget.tabCloseRequested.connect(closeTab)
    main.UImain.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
    main.UImain.dateEdit_2.setDateTime(QtCore.QDateTime.currentDateTime())
    main.UImain.tabWidget.tabBar().setTabButton(0, QtWidgets.QTabBar.RightSide, None)
    main.UImain.textEdit.setReadOnly(True)
    main.UImain.comboBox.addItems(config.binance)
    main.UImain.comboBox_3.addItems(config.k_algo)
    exchangeinfo = config.binance_client.get_exchange_info()
    main.UImain.pushButton.clicked.connect(lambda:goStart())
    for s in exchangeinfo["symbols"]:
        if(s["quoteAsset"] == "USDT"):
            config.tradesembollistesi.append(s["symbol"])
    main.UImain.comboBox_2.addItems(config.tradesembollistesi)
    # for i in range(len(config.k_algo)):
    #     main.UImain.comboBox_3.setItemChecked(i, True)
    for i in range(len(config.tradesembollistesi)):
        main.UImain.comboBox_2.setItemChecked(i, False)
    for i in range(len(config.binance)):
        main.UImain.comboBox.setItemChecked(i,False)

def listeleyici(combobox):
    combobox_dizi = []
    for i in range (combobox.count()):
        if (combobox.itemChecked(i)):
            combobox_dizi.append(combobox.itemText(i))
    return combobox_dizi    

def kartezyen(dizi1, dizi2):
    return list(itertools.product(dizi1,dizi2))

def goStart():
    tabPrint("Created by FurkanAdmin")
    trade_dizi = listeleyici(main.UImain.comboBox_2)
    period_dizi = listeleyici(main.UImain.comboBox)
    for i in range(len(kartezyen(trade_dizi, period_dizi))):
        createThread(kartezyen(trade_dizi, period_dizi)[i][0]+kartezyen(trade_dizi, period_dizi)[i][1], kartezyen(trade_dizi, period_dizi)[i][0], kartezyen(trade_dizi, period_dizi)[i][1])

def createThread(procces_name, tradeName, PeriodName):
    t1=Thread(target=dataandwork,args=(tradeName, PeriodName, procces_name))
    t1.name = procces_name
    tab = QtWidgets.QWidget()
    main.UImain.tabWidget.addTab(tab, procces_name)
    newGridLayout = QtWidgets.QGridLayout(tab)
    newGridLayout.setObjectName(procces_name +"Grid")
    newTextEdit =  QtWidgets.QTextEdit(tab)
    newTextEdit.setObjectName(procces_name +"Text") 
    newTextEdit.setReadOnly(True)
    newGridLayout.addWidget(newTextEdit, 0, 0, 1, 1)  
    t1.start()

def tabPrint(yazi):
    main.UImain.textEdit.append("["+threading.current_thread().name+"] :" +" "+yazi)
    if(not threading.current_thread().name == "MainThread"):
        main.UImain.tabWidget.findChild(QtWidgets.QTextEdit, threading.current_thread().name+"Text").append(yazi)

def dataandwork(symbol, time, proccesname):
    tabPrint("Downloading data for : "+ str(threading.current_thread().name))
    klines = config.binance_client.get_historical_klines(symbol, time, gunleriduzenle(main.UImain.dateEdit) , gunleriduzenle(main.UImain.dateEdit_2))
    datafile = pd.DataFrame(klines, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    klinesold = config.binance_client.get_historical_klines(symbol, time, gunleriduzenle(main.UImain.dateEdit) , datetime.utcnow().strftime("%d %b %Y %H:%M:%S"))
    datafile2=pd.DataFrame(klinesold, columns=  ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
    binancesocket = "wss://stream.binance.com:9443/ws/"+symbol.lower()+"@kline_"+time.lower()
    budget = int(main.UImain.lineEdit.text())
    tabPrint("--Indırme Tamamlandı--")
    datafile2 = datafile2.astype(float)
    datafile = datafile.astype(float)
    datafile = datafile.drop(['close_time','quote_av','trades','tb_base_av','tb_quote_av','ignore'], axis=1)
    datafile2 = datafile2.drop(['close_time','quote_av','trades','tb_base_av','tb_quote_av','ignore'], axis=1)
    datafile = datafile.drop(['timestamp'], axis=1)
    datafile2 = datafile2.drop(['timestamp'], axis=1)
    datafile2.astype(float)
    datafile.astype(float)
    if(main.UImain.checkBox.isChecked()): 
        getdatas.backtesting(budget, datafile, symbol, float(main.UImain.lineEdit_2.text()) ,float(main.UImain.lineEdit_3.text()))
        tabPrint("Thread Bitti: "+str(threading.currentThread().name))
        for thread in threading.enumerate(): 
            if(thread.name == "MainThread"):
                thread.join()
    else:
        getdatas.realTime(symbol,binancesocket,budget,datafile2,float(main.UImain.lineEdit_2.text()), float(main.UImain.lineEdit_3.text()))

def killprocces(tabname):           
    for thread in threading.enumerate(): 
        if(thread.name == tabname):
            print("killed(terminated)")
            tabPrint("Killed :"+ str(tabname))
            exc = ctypes.py_object(SystemExit)
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), exc)
            print("Killed via main")

def closeTab(index):
    tab_name = main.UImain.tabWidget.tabText(index)
    main.UImain.tabWidget.removeTab(index)
    killprocces(tab_name)

def gunleriduzenle(object):
    ay = object.date().month()
    gun = object.date().year()
    yil = object.date().day()
    print(ay, gun, yil)
    return config.GunleriDuzgunle.tarih(gun=gun,ay=ay,yil=yil)