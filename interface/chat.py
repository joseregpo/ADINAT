from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget
from IHM import Ui_Form


class listQt(QWidget, Ui_Form):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.on_clic)
        self.lineEdit.setFocus(True)
    
    def on_clic(self):
        self.textEdit.setText(self.textEdit.toPlainText()+self.lineEdit.text()+"\n")
        self.lineEdit.setText("")

    def keyPressEvent(self, e):
        if e.key() == 16777220:
            self.on_clic()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = listQt()
    win.show()
    sys.exit(app.exec_())