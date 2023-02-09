import sys
sys.dont_write_bytecode = True
import Pages.loginscreen as loginscreen, Pages.mainscreen as mainscreen, main , config, json, os, sys
from binance.client import Client
from PyQt5 import QtWidgets
import Fonskiyonlar.sayfafonk.mainscreenfnc as mainscreensettings
import Fonskiyonlar.sayfafonk.loginscreenfnc as loginscreensettings
app = QtWidgets.QApplication(sys.argv)
login_screen = QtWidgets.QDialog()
main_screen = QtWidgets.QMainWindow()
UImain = mainscreen.Ui_MainWindow()
UIlogin = loginscreen.Ui_Dialog()
def showWindows(currentWindows):
    if(__name__== "__main__"):
        main.showWindows(currentWindows)
    else:
        if(currentWindows == "loginscreen"):
            UIlogin.setupUi(login_screen)
            loginscreensettings.ClickAndDesign()
            login_screen.show()
        if(currentWindows == "mainscreen"):
            UImain.setupUi(main_screen)
            mainscreensettings.design()
            main_screen.show() 
            login_screen.close()
if __name__ == "__main__":
    os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"   
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1" 
    os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"        
    if(not os.path.isfile(config.jsonFile)):
        showWindows("loginscreen")
    else:
        try:
            with open(config.jsonFile, "r") as f:
                JsonCopy = json.load(f)
            if("bilgiler" in JsonCopy):
                controljson = JsonCopy["bilgiler"]
                if((len(controljson)==2) and (('API_KEY'in controljson and 'API_SECRET' in controljson)) and
                    (len(controljson["API_KEY"]) == 64 and len(controljson["API_SECRET"]) == 64 )):
                    config.API_KEY = controljson["API_KEY"]
                    config.API_SECRET = controljson["API_SECRET"]
                    config.binance_client = Client(config.API_KEY, config.API_SECRET)
                    try:
                        config.binance_client.get_account()
                        showWindows("mainscreen")
                    except:
                        showWindows("loginscreen")
            else:
                print("Hata : config dosaysı bulunamadı")
                showWindows("loginscreen")
        except Exception as e:
            print(e)
            print("Hata")
            showWindows("loginscreen")
    os._exit(app.exec_())    