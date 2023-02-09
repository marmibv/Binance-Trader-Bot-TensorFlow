import main, config, json
from binance import Client

def ClickAndDesign():
    main.UIlogin.buttonBox.clicked.connect(lambda:login())
def login():
        config.API_KEY = main.UIlogin.lineEdit.text()
        config.API_SECRET = main.UIlogin.lineEdit_2.text()
        config.binance_client = Client(config.API_KEY, config.API_SECRET)
        try:
            print(config.API_KEY)
            print(config.API_SECRET)
            config.binance_client.get_account()
            print(config.jsonFile)
            JsonFile = {"bilgiler": {"API_KEY": config.API_KEY, "API_SECRET": config.API_SECRET}}
            with open (config.jsonFile, "w") as f:
                json.dump(JsonFile,f)
            main.showWindows("mainscreen")
        except Exception as e:
            print("API HATASI")
            print(e)