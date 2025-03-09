import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the user interface
        self.initUI()

    def initUI(self):
        # Create a button to run main.py
        btn_run_main = QPushButton('Run main.py', self)
        btn_run_main.clicked.connect(self.run_main)

        # Create a button to run another Python file
        btn_run_another = QPushButton('Run another.py', self)
        btn_run_another.clicked.connect(self.run_another)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(btn_run_main)
        layout.addWidget(btn_run_another)

        self.setLayout(layout)
        self.setWindowTitle('Run Python Files')
        self.show()

    def run_main(self):
        try:
            # Run main.py using subprocess
            subprocess.run(['python', 'main.py'], check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to run main.py: {e}")

    def run_another(self):
        try:
            # Run another Python file using subprocess
            subprocess.run(['python', 'loginmain.py'], check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to run another.py: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())