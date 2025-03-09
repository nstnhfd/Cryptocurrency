import yfinance as yf  
import matplotlib.pyplot as plt  

def plot_crypto(ticker, start_date, end_date):  
  """  
  Fetches cryptocurrency data from yfinance and plots the historical price.  

  Args:  
    ticker: The ticker symbol of the cryptocurrency (e.g., "BTC-USD").  
    start_date: The start date for the data (e.g., "2023-01-01").  
    end_date: The end date for the data (e.g., "2023-12-31").  
  """  

  try:  
    # Download data from yfinance  
    data = yf.download(ticker, start=start_date, end=end_date)  

    # Check if data was successfully downloaded  
    if data.empty:  
      print(f"No data found for {ticker} between {start_date} and {end_date}.")  
      return  

    # Create the plot  
    plt.figure(figsize=(12, 6))  # Adjust figure size for better readability  
    plt.plot(data['Close'], label='Closing Price')  
    plt.title(f'{ticker} Price History')  
    plt.xlabel('Date')  
    plt.ylabel('Price (USD)')  
    plt.grid(True)  # Add grid for better readability  
    plt.legend()  
    plt.show()  

  except Exception as e:  
    print(f"An error occurred: {e}")  

# Example usage:  
if __name__ == '__main__':  
  plot_crypto("BTC-USD", "2024-01-01", "2025-03-07")  # Bitcoin in USD  
  # plot_crypto("ETH-USD", "2024-01-01", "2025-03-07")  # Ethereum in USD  
  # plot_crypto("DOGE-USD", "2024-01-01", "2025-03-07") # Dogecoin in USD  