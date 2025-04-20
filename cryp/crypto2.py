
from sub_form_crypto import Ui_sub_form_crypto
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *  
from PyQt5.QtGui import * 
import requests
import sys
import time
from datetime import datetime
import matplotlib.pyplot as plt  
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  
import yfinance as yf
class MplCanvas(FigureCanvas):  
    def __init__(self, parent=None):  
        fig, self.ax = plt.subplots(figsize=(8, 5))  
        super().__init__(fig)  
    def plot(self, data):  
        self.ax.clear()  # Clear the previous plot 
        self.figure.set_facecolor('white')    
        self.ax.set_facecolor('white')       
        self.figure.set_edgecolor('white') 
        self.ax.plot(data['Close'], color='darkgreen')          
        self.draw()
class Window(QMainWindow):
    def __init__(self,btnname=None):  
        super(Window, self).__init__()  
        self.name = btnname     
        self.ui = Ui_sub_form_crypto()  
        self.ui.setupUi(self)
        self.setWindowTitle("Cryptocurrencysub")
        # self.ui.cryptoname.setText(self.name)
        name=self.name
        capname=name[0].upper() + name[1:]
        self.ui.commandLinkButton.setText(capname)
        self.get_24h(self.name)
        # self.get_crypto_prices(self.name)
        self.get_market(self.name)        
        self.canvas = MplCanvas(self)             
        self.ui.verticalLayout.addWidget(self.canvas)
        self.plot_data('BIT-USD')  
        self.canvas = MplCanvas(self)
    def plot_data(self,ticker):   
        while True: 
            try:
                data = yf.download(ticker, start="2021-01-01", end="2025-01-22")
                return  data
            except yf.YFRatelimiterror as e:
                print(f"rate {e}")
                time.sleep(60)
            except Exception as e:
                print(f"an unexpected {e}")
                return None    
         
        self.canvas.plot(data)
    def get_24h(self,crypto_ids=None):
        currency = 'usd_24h_vol'
        if crypto_ids is None:
            crypto_ids = ['bitcoin']          
        url = f"https://api.coingecko.com/api/v3/coins/{crypto_ids}/market_chart?vs_currency=usd&days=1"  
        headers = {"accept": "application/json"}        
        response = requests.get(url, headers=headers)        
        data = response.json()
        prices = data['prices']         
        for timestamp, price in prices:  
            timestamp = timestamp / 1000      
            readable_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')  
            # print(f"Time: {readable_time}, Price: {price}")   
        price=str(price)
        time = str(readable_time)
        self.ui.volume.setText(f"{time} : {price}")
    def get_market(self,crypto_ids=None):
        currency='usd_market_cap'
        if crypto_ids is None:
            crypto_ids = ['bitcoin', 'ethereum', 'tether']
        ids = ','.join(crypto_ids)
        # url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_market_cap=true"
        url = "https://api.coingecko.com/api/v3/coins/bitcoin?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()  
        headers = {"accept": "application/json"}        
        response = requests.get(url, headers=headers) 
        data = response.json()
        print(data)
        # self.ui.aed1.setText(str(data['market_data']['current_price']['aed']))
        # self.ui.ars1.setText(str(data['market_data']['current_price']['ars']))

        # self.ui.aud1.setText(str(data['market_data']['current_price']['aud']))
        # self.ui.bch1.setText(str(data['market_data']['current_price']['bch']))

        # self.ui.bdt1.setText(str(data['market_data']['current_price']['bdt']))
        # self.ui.bhd1.setText(str(data['market_data']['current_price']['bhd']))

        # self.ui.bmd1.setText(str(data['market_data']['current_price']['bmd']))
        # self.ui.bnb1.setText(str(data['market_data']['current_price']['bnb']))

        # self.ui.brl1.setText(str(data['market_data']['current_price']['brl']))
        # self.ui.btc1.setText(str(data['market_data']['current_price']['btc']))

        # self.ui.cad1.setText(str(data['market_data']['current_price']['cad']))
        # self.ui.chf1.setText(str(data['market_data']['current_price']['chf']))        
    def get_crypto_price(self, crypto_id='bitcoin'):  
        currency = 'usd'  
    
    # CoinGecko API URL for the price  
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={currency}'    
        response = requests.get(url)     
    
        if response.status_code == 200:  
            data = response.json()  
        
        # Get the price for the specified cryptocurrency  
            price = data[crypto_id][currency]  
            print(f"The current price of {crypto_id.capitalize()} in {currency.upper()} is: {price}")  
        
        # Update the label if applicable  
            if self.labels:  # Ensure self.labels is not empty  
                self.labels[0].setText(f"{price}")  # Assuming you want to update the first label  
            
        else:  
            print("Error fetching data from CoinGecko API")  
            print("Status Code:", response.status_code)

def main():      
    qt_app = QApplication(sys.argv)  
    qt_app.setApplicationName("Cryptocurrency")  
    qt_app.setApplicationVersion("1.0")  
    win = Window()  
    win.show() 
    sys.exit(qt_app.exec_())  

if __name__ == "__main__":  
    main()  
    