import sys  
import requests  
import datetime  
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel)  
from PyQt5.QtGui import QPixmap, QImage  
import matplotlib.pyplot as plt  
import io  
import matplotlib.dates as mdates  

def get_crypto_chart_image(coin_id, currency, start_date, end_date):  
    """  
    Fetches cryptocurrency data from CoinGecko API and generates a chart image.  

    Args:  
        coin_id (str): CoinGecko ID (e.g., "bitcoin").  
        currency (str): Currency (e.g., "usd").  
        start_date (str): Start date (YYYY-MM-DD).  
        end_date (str): End date (YYYY-MM-DD).  

    Returns:  
        QImage:  A QImage of the chart, or None if an error occurred.  
    """  
    try:  
        # Date to timestamp conversion  
        start_timestamp = int(datetime.datetime.strptime(start_date, "%Y-%m-%d").timestamp())  
        end_timestamp = int(datetime.datetime.strptime(end_date, "%Y-%m-%d").timestamp())  

        # CoinGecko API URL  
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range?vs_currency={currency}&from={start_timestamp}&to={end_timestamp}"  

        # API Request  
        response = requests.get(url)  
        response.raise_for_status()  

        data = response.json()  

        # Extract Prices and Dates  
        prices = data['prices']  
        dates = [datetime.datetime.fromtimestamp(ts / 1000) for ts, _ in prices]  
        price_values = [price for _, price in prices]  

        # Plotting with Matplotlib  
        plt.figure(figsize=(8, 4))  # Smaller figure size for Qt  
        plt.plot(dates, price_values, label=f'{coin_id.capitalize()} Price', color='green')  
        plt.title(f'{coin_id.capitalize()} Price History ({start_date} - {end_date})')  
        plt.xlabel('Date')  
        plt.ylabel(f'Price ({currency.upper()})')  
        plt.grid(True)  
        plt.legend()  
        plt.xticks(rotation=45)  
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format date axis  
        plt.tight_layout()  

        # Convert Matplotlib plot to QImage  
        buf = io.BytesIO()  
        plt.savefig(buf, format='png')  
        buf.seek(0)  
        im = QImage.fromData(buf.read())  
        plt.close()  # Close the plot to free memory  

        return im  

    except requests.exceptions.RequestException as e:  
        print(f"API request failed: {e}")  
        return None  
    except KeyError:  
        print("Error: Could not extract data. Check the coin_id and currency.")  
        return None  
    except ValueError:  
        print("Error: Invalid date format. Use YYYY-MM-DD.")  
        return None  
    except Exception as e:  
        print(f"An unexpected error occurred: {e}")  
        return None  

class CryptoChartWidget(QWidget):  
    def __init__(self, coin_id, currency, start_date, end_date):  
        super().__init__()  
        self.coin_id = coin_id  
        self.currency = currency  
        self.start_date = start_date  
        self.end_date = end_date  
        self.initUI()  

    def initUI(self):  
        self.setWindowTitle(f'{self.coin_id.capitalize()} Chart')  
        self.layout = QVBoxLayout()  

        # Fetch the chart image  
        image = get_crypto_chart_image(self.coin_id, self.currency, self.start_date, self.end_date)  

        if image:  
            # Display the chart in a QLabel  
            pixmap = QPixmap.fromImage(image)  
            self.chart_label = QLabel(self)  
            self.chart_label.setPixmap(pixmap)  
            self.layout.addWidget(self.chart_label)  
        else:  
            error_label = QLabel("Failed to load chart.")  
            self.layout.addWidget(error_label)  


        self.setLayout(self.layout)  
        self.setGeometry(300, 300, 800, 600) #set initial size of window  


if __name__ == '__main__':  
    app = QApplication(sys.argv)  
    widget = CryptoChartWidget("bitcoin", "usd", "2024-01-01", "2025-03-07")  
    widget.show()  
    sys.exit(app.exec_())  