
from form_crypto import Ui_Form_Crypto
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *  
from PyQt5.QtGui import * 
import requests
import sys
import matplotlib.pyplot as plt  
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  
import yfinance as yf
from crypto2 import Window as CryptoWindow
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
    def opensubcrypto(self,btnname=None):              
        self.crypto_window2 = CryptoWindow(btnname=btnname)
        self.crypto_window2.show()
    def __init__(self,email=None):  
        super(Window, self).__init__()  
        self.email = email
        self.ui = Ui_Form_Crypto()  
        self.ui.setupUi(self)
        self.setWindowTitle("Cryptocurrency")
        username = self.email.split('@')[0]  
        self.ui.label_15.setText(f"wellcome dear {username}")

        self.ui.bitcoin.clicked.connect(lambda: self.opensubcrypto(btnname='bitcoin'))
        self.ui.ethereum.clicked.connect(lambda: self.opensubcrypto(btnname='ethereum'))
        self.ui.tether.clicked.connect(lambda: self.opensubcrypto(btnname='tether'))
        self.ui.tron.clicked.connect(lambda: self.opensubcrypto(btnname='tron'))
        self.ui.cardano.clicked.connect(lambda: self.opensubcrypto(btnname='cardano'))
        self.ui.dogcoin.clicked.connect(lambda: self.opensubcrypto(btnname='dogcoin'))
        self.ui.polkadot.clicked.connect(lambda: self.opensubcrypto(btnname='polkadot'))
        self.ui.sui.clicked.connect(lambda: self.opensubcrypto(btnname='sui'))
        self.ui.stellar.clicked.connect(lambda: self.opensubcrypto(btnname='stellar'))
        self.ui.litecoin.clicked.connect(lambda: self.opensubcrypto(btnname='litecoin'))
        self.ui.uniswap.clicked.connect(lambda: self.opensubcrypto(btnname='uniswap'))
        self.ui.pepe.clicked.connect(lambda: self.opensubcrypto(btnname='pepe'))
        self.ui.aptes.clicked.connect(lambda: self.opensubcrypto(btnname='aptos'))        
        
        cryptoies=[]        
        cryptoies = ['bitcoin', 'ethereum', 'tether','tron','cardano','dogcoin','polkadot','sui','stellar','litecoin','uniswap','pepe','aptos']        
        self.labels = [self.ui.label1, self.ui.label2, self.ui.label3, self.ui.label4,self.ui.label5,self.ui.label6,self.ui.label7, self.ui.label8,self.ui.label9, self.ui.label10, self.ui.label11, self.ui.label12,self.ui.label13]  # Adjust this if your labels are named differently  
        self.labels2 = [self.ui.label14,self.ui.label15,self.ui.label16,self.ui.label17,self.ui.label18,self.ui.label19,self.ui.label20,self.ui.label21,self.ui.label22,self.ui.label23,self.ui.label24,self.ui.label25,self.ui.label26]
        self.labels3 = [self.ui.label27,self.ui.label28,self.ui.label29,self.ui.label30,self.ui.label31,self.ui.label32,self.ui.label33,self.ui.label34,self.ui.label35,self.ui.label36,self.ui.label37,self.ui.label38,self.ui.label39]

        self.get_24h(cryptoies)
        self.get_crypto_prices(cryptoies)
        self.get_market(cryptoies)
        self.canvas = MplCanvas(self) 
        layout_names = [f'verticalLayout{i}' for i in range(3, 16)]
        vertl = [getattr(self.ui, name) for name in layout_names]        
        tickers = ['BIT-USD', 'ETH-USD', 'TET-USD', 'TRO-USD', 'CAR-USD', 'DOG-USD', 'POL-USD', 'SUI-USD', 'STE-USD', 'LIT-USD', 'UNI-USD', 'PEP-USD', 'APT-USD']
        for ticker,v in zip(tickers,vertl): 
          v.addWidget(self.canvas)
          self.plot_data(ticker)  
          self.canvas = MplCanvas(self)
    def plot_data(self,ticker):        
        data = yf.download(ticker, start="2021-01-01", end="2025-01-22")  
        self.canvas.plot(data)
    def get_24h(self,crypto_ids=None):
        
        currency = 'usd_24h_vol'
        if crypto_ids is None:
            crypto_ids = ['bitcoin', 'ethereum', 'tether']
        ids = ','.join(crypto_ids)
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_24hr_vol=true"
        response = requests.get(url)
        data = response.json()
        markets = []
        for crypto_id in crypto_ids:
            market = data[crypto_id][currency]
            markets.append(market)
            
        i = 0    
        for label in self.labels3:  
            if i < len(markets):  # Check to avoid IndexError                
                label.setText(f"{str(markets[i])[:4]}") # Use the correct indexing  
            i += 1 
    def get_market(self,crypto_ids=None):
        currency='usd_market_cap'
        if crypto_ids is None:
            crypto_ids = ['bitcoin', 'ethereum', 'tether']
        ids = ','.join(crypto_ids)
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_market_cap=true"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()  
        markets = []
        for crypto_id in crypto_ids:
            market = data[crypto_id][currency]
            markets.append(market)            
        i = 0    
        for label in self.labels2:  
            if i < len(markets):  # Check to avoid IndexError                  
                label.setText(f"{str(markets[i])[:4]}") # Use the correct indexing  
            i += 1 
    def get_crypto_prices(self,crypto_ids=None):        
        currency='usd'
        if crypto_ids is None:
            crypto_ids = ['bitcoin', 'ethereum', 'tether']
        ids = ','.join(crypto_ids)    
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies={currency}'    
        response = requests.get(url)     
        if response.status_code == 200:
            data = response.json()  
        prices = []        
        for crypto_id in crypto_ids: 
             
            price = data[crypto_id][currency]           
            prices.append(price)            
            print(f"The current price of {crypto_id.capitalize()} in {currency.upper()} is: {price}")    
        i = 0    
        
        for label in self.labels:  
            if i < len(prices):  # Check to avoid IndexError  
                
                label.setText(f"{prices[i]}")  # Use the correct indexing  
            i += 1 
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
    