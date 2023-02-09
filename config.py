from binance import Client
import datetime
from PyQt5 import QtCore, Qt
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt
binance = {"1m": 1, "5m": 5, "30m": 30, "1h": 60, "4h": 240, "1d": 1440 , "1W": 10080, "1M": 43200}
jsonFile = "config.json"
k_algo = {"RSI": 1, "MACD": 2, "VORTEX": 3, "DMI": 4, "CMF": 5, "AROON": 6, "MFI": 7, "HA": 8}
API_KEY = ""
API_SECRET = ""
binance_client = Client(API_KEY, API_SECRET)
tradesembollistesi = []
class CheckableComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self._changed = False
        self.view().pressed.connect(self.handleItemPressed)
    def setItemChecked(self, index, checked=False):
        item = self.model().item(index, self.modelColumn()) # QStandardItem object
        if checked:
            item.setCheckState(QtCore.Qt.Checked)
        else:
            item.setCheckState(QtCore.Qt.Unchecked)
    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)

        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)
        self._changed = True
    def hidePopup(self):
        if not self._changed:
            super().hidePopup()
        self._changed = False
    def itemChecked(self, index):
        item = self.model().item(index, self.modelColumn())
        return item.checkState() == QtCore.Qt.Checked
    def addItems(self, texts, datalist=None):
        for i, text in enumerate(texts):
            try:
                data = datalist[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data)
    def currentData(self):
        res = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                res.append(self.model().item(i).data())
        return res
class GunleriDuzgunle():
    def tarih(gun, ay , yil):
        ayarlanandate = datetime.datetime(gun, ay, yil)
        ayarlanandate.strftime("%d %b %Y")
        print(ayarlanandate.strftime("%d %b, %Y"))
        return ayarlanandate.strftime("%d %b, %Y")