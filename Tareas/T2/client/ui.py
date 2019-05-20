import PyQt5.QtWidgets as wid
from PyQt5.QtCore import pyqtSlot
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from time import sleep

class First(QMainWindow):
    def __init__(self, parent=None):
        super(First, self).__init__(parent)

        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 400

        self.initUI()

    # onClick

    def on_pushButton_clicked(self):
        self.chatUI(self.mail_text.text(), self.password_text.text())
    
    def send_message(self):
        msg = self.message.text()
        if msg != "":
            pass

    # UI

    def initUI(self):
        self.setWindowTitle('Secure messaging')
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        layout = wid.QVBoxLayout()
        layout.addWidget(wid.QLabel("Welcome!"))

        self.mail_text = QLineEdit()
        self.mail_text.setPlaceholderText("mail...")

        self.password_text = QLineEdit()
        self.password_text.setEchoMode(wid.QLineEdit.Password)
        self.password_text.setPlaceholderText("password...")

        self.button = QPushButton('Connect!')
        self.button.clicked.connect(self.on_pushButton_clicked)

        layout.addWidget(self.mail_text)
        layout.addWidget(self.password_text)
        layout.addWidget(self.button)
        
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(layout)
        self.show()

    def chatUI(self, mail, password):
        self.setWindowTitle("Secure messaging: Chat")

        layout = wid.QVBoxLayout()

        self.chat = wid.QLabel("Chat is empty...")

        send_holder = wid.QHBoxLayout()

        self.message = wid.QLineEdit()
        self.message.setPlaceholderText("Message...")
        send = QPushButton("->")
        send.clicked.connect(self.send_message)

        send_holder.addWidget(self.message)
        send_holder.addWidget(send)

        layout.addWidget(self.chat)
        layout.addLayout(send_holder)

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(layout)
        self.show()



def main():
    app = QApplication(sys.argv)
    main = First()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()