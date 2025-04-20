 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *  
from PyQt5.QtGui import * 
from login import Ui_Log_In
from createuser import Ui_Create_User
from PyQt5 import QtWidgets 
from crypto1 import Window as CryptoWindow
import sys
import requests  
# uvicorn cryp.appss:app --reload
# pyuic5 -x sub_form_crypto.ui -o sub_form_crypto.py
# data = yf.download(ticker, start="2021-01-01", end="2025-01-22", cache=True)  
class Window(QMainWindow):      
    def openwindow(self):                
        self.create_user_window =QtWidgets.QMainWindow()
        self.ui=Ui_Create_User()
        self.ui.setupUi(self.create_user_window)
        self.create_user_window.show() 
        self.ui.confirm.clicked.connect(self.user_create)  
    def opencrypto(self):       
        email = self.ui.emailadd.text()        
        # Create an instance of the CryptoWindow and show it
        self.crypto_window = CryptoWindow(email=email)
        self.crypto_window.show() 
        self.close()       
  
    def __init__(self):  
        super(Window, self).__init__()  
        self.ui = Ui_Log_In()          
        self.ui.setupUi(self)
        self.setWindowTitle("Cryptocurrency")   
        self.ui.createuser.clicked.connect(self.openwindow)  
        self.ui.login.clicked.connect(self.user_login)

    def close_windows(self):  
        if self.create_user_window:   
            self.create_user_window.close()  
    def user_create(self):
        param1 = self.ui.email.text()  
        param2 = self.ui.password.text()
        payload = {  
            "email": param1,  
            "password": param2  
        }  
        # Send POST request to FastAPI  
        try:  
            response = requests.post('http://127.0.0.1:8000/users', json=payload)  
            if  response.status_code == 201:                  
                print("User created successfully!")  
                QMessageBox.information(self, "message",  
                                     f"user created: {response.status_code}. Response: {response.text}")
                
                self.close_windows()             
            else:  
                QMessageBox.critical(self, "Error",  
                                     f"Request failed with status code: {response.status_code}. Response: {response.text}")  
        except requests.exceptions.RequestException as e:  
            QMessageBox.critical(self, "Error", f"Request failed: {e}")  
    def user_login(self):        
        param1 = self.ui.emailadd.text()
        param2 = self.ui.password.text()
        if param1 and param2 :
           payload = {  
             "username": param1,  
             "password": param2  
             }
        else:
              QMessageBox.critical(self, "Error",  
                                     "username and password are required")
        try:  
            response = requests.post('http://127.0.0.1:8000/login', data=payload)          
            if  response.status_code==200 :  
                self.opencrypto()
                #print("log in")
                               
            else:  
                QMessageBox.critical(self, "Error",  
                                     f"Request failed with status code: {response.status_code}. Response: {response.text}")  
        except requests.exceptions.RequestException as e:  
            QMessageBox.critical(self, "Error", f"Request failed: {e}")

def main():     
    qt_app = QApplication(sys.argv)  

    qt_app.setApplicationName("Cryptocurrency")  
    qt_app.setApplicationVersion("1.0")  
    win = Window()  
    win.show() 
    sys.exit(qt_app.exec_()) 
main()
 

    