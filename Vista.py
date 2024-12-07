import sys
from PyQt5.QtWidgets import QApplication,QMainWindow, QDialog,QMessageBox
from PyQt5.QtGui import QDoubleValidator, QRegExpValidator,QIntValidator
from PyQt5.QtCore import Qt,QRegExp
from PyQt5.uic import loadUi
import masc_rc
import cuenta_rc
import masc2_rc
import rx_rc
import ecg_rc
import ppg_rc

#Ventana de Usuario y contraseña.
class pprincipal(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('pprincipal.ui',self)
        self.setup()
    def setup(self):
        self.ingres_boton.clicked.connect(self.Abrir_menu)
        self.bot_cuenta.clicked.connect(sel.Abrir_nuev_cuent)
    def Abrir_menu(self):
        ventana_menu=menu(self)
        self.hide()
        ventana_menu.show()
    def Abrir_nuev_cuenta(self):
        ventana_cuenta=nueva_cuenta(self)
        self.hide()
        ventana_cuenta.show()
#Ventana de creación de nueva cuenta.
class nueva_cuenta(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('nueva_cuenta.ui',self)
        self._ventana_pprincipal=parent
        self.setup()
    def setup(self):
        self.nomb_input.setValidator(QRegExpValidator(QRegExp("[a-zA-Z ]+")))
        self.id_input.setValidator(QIntValidator())
        self.telef_input.setValidator(QRegExpValidator(QRegExp("[a-zA-Z ]+")))
        self.usua_input.setValidator(QRegExpValidator(QRegExp("[a-zA-Z ]+")))

class menu(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('Menu.ui',self)
        self._ventana_pprincipal=parent
        # self.setup()
    def setup(self):
        self.rx_bot.clicked.connect(self.Abrir_rx)
        self.ecg_bot.clicked.connect(self.Abrir_ecg)
        self.ppg_bot.clicked.connect(self.Abrir_ppg)
        self.bot_cerrar_ses.clicked.connect(self.Cerrar_ses)
    def Cerrar_ses(self):
        self._ventana_pprincipal.show()
        self.hide()
    def Abrir_ppg(self):
        ventana_ppg=ppg(self)
        self.hide()
        ventana_ppg.show

    def Abrir_ecg(self):
        ventana_ecg=ecg(self)
        self.hide()
        ventana_ecg.show

    def Abrir_rx(self):
        ventana_rx=rx(self)
        self.hide()
        ventana_rx.show

class rx(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('rx.ui',self)
        self.setup()
    def setup(self):

class ecg(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('ECG.ui',self)
        self.setup()
    def setup(self):
         
class ppg(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('',self)
        self.setup()
    def setup(self):
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana=pprincipal()
    ventana.show()
    sys.exit(app.exec_())