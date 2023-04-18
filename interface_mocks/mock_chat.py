from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget
import sys 
from IHM import Ui_DISCUSSIT

chatrooms = {"general" : ["blabla", "bonjour", "finito"], "louis" : ["louis : couocu", "jose : yooo, ça va?"] }
users = ["general", "louis", "raph", "jose", "marion"]
class MainWindow(QWidget, Ui_DISCUSSIT):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.send_message.clicked.connect(self.on_clic)
        self.users_lists.itemClicked.connect(self.change_chatroom)
        self.chats.addItems(chatrooms["general"])
        self.users_lists.addItems(users)

    def change_chatroom(self, item):
        for k, v in chatrooms.items():
            if k == item.text():
                self.chats.clear()
                self.chats.addItems(v)

    def on_clic(self):
        # self.textEdit.setText(self.textEdit.toPlainText()+self.lineEdit.text()+"\n")
        self.chats.addItem(self.message.text())
        self.message.setText("")

    def keyPressEvent(self, e):
        if e.key() == 16777220:
            self.on_clic()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())