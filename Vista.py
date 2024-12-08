import sys
from PyQt5.QtWidgets import QApplication,QMainWindow, QDialog,QMessageBox,QFileDialog
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
        # self.ingres_boton.clicked.connect(self.Verificar_cred)
        self.ingres_boton.clicked.connect(self.Abrir_menu)
        self.bot_cuenta.clicked.connect(self.Abrir_nuev_cuenta)
    # def Verificar_cred(self):
    #     cusuario=self.usu_input.text()
    #     ccontrasena=self.contra_input.text()
    #     self._ventana_pprincipal.Recibir_cred(cusuario,ccontrasena)
    def Abrir_menu(self):
        ventana_menu=menu(self)
        self.hide()
        ventana_menu.show()
    def Abrir_nuev_cuenta(self):
        ventana_cuenta=nueva_cuenta(self)
        self.hide()
        ventana_cuenta.show()
    def Recibir_nuev_cuenta(self, nomb,id,telef,email,usua,contras):
        self.__mi_controlador.Recibir_nueva_cuenta(self, nomb,id,telef,email,usua,contras)
    def Recibir_cred(self,usu,con):
        self.__mi_controlador.Recibir_cred(usu,con)
    def Asignar_cont(self,c):
        self.__mi_controlador=c
class nueva_cuenta(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('nueva_cuenta.ui',self)
        self._ventana_pprincipal=parent
        self.setup()
    def setup(self):
        self.nomb_input.setValidator(QRegExpValidator(QRegExp("[a-zA-Z ]+")))
        self.id_input.setValidator(QIntValidator())
        self.telef_input.setValidator(QIntValidator())
        self.usua_input.setValidator(QRegExpValidator(QRegExp("[a-zA-Z ]+")))
        self.contra_input.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9 ]+")))
        self.acept_boton.clicked.connect(self.opc_aceptar)
        self.volver_boton.clicked.connect(self.opc_volver)
    def opc_aceptar(self):
        nomb =  self.nomb_input.text()
        id = self.id_input.text()
        telef= self.telef_input.text() ### Consulatr metodo ver 
        email= self.email_input.text()
        usua = self.usua_input.text()
        contras = self.contra_input.text()
        self._ventana_pprincipal.Recibir_nuev_cuenta(nomb,id,telef,email,usua,contras)
        self._ventana_pprincipal.show()
        self.hide()
    def opc_volver(self):
        self.hide()
        self._ventana_pprincipal.show()

class menu(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('Menu.ui',self)
        self._ventana_pprincipal=parent
        self.setup()
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
        ventana_ppg.show()

    def Abrir_ecg(self):
        ventana_ecg=ecg(self)
        self.hide()
        ventana_ecg.show()

    def Abrir_rx(self):
        ventana_rx=rx(self)
        self.hide()
        ventana_rx.show()

class rx(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        loadUi('rx.ui',self)
        self._ventana_menu=parent
        self.setup()
    def setup(self):
        self.volver_bot.clicked.connect(self.opcion_volver)
        self.subir_arc.clicked.connect(self.Abrir_archivo)
    def opcion_volver(self):
        self.hide()
        self._ventana_menu.show()
    def Abrir_archivo(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Abrir archivo", "", "Todos los archivos (*)")
        if archivo:
            msm=f"Archivo seleccionado: {archivo}"
            self.archivo_enc.setText(msm)
        else:
            msm="No se seleccionó ningún archivo"
            self.archivo_enc.setText(msm)
        


class ecg(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('ECG.ui',self)
        self._ventana_menu=parent
        self.setup()
    def setup(self):
        self.volver_bot.clicked.connect(self.opcion_volver)
        self.subir_arc.clicked.connect(self.Abrir_archivo)
    def opcion_volver(self):
        self.hide()
        self._ventana_menu.show()
    def Abrir_archivo(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Abrir archivo", "", "Todos los archivos (*)")
        if archivo:
            msm=f"Archivo seleccionado: {archivo}"
            self.archivo_enc.setText(msm)
        else:
            msm="No se seleccionó ningún archivo"
            self.archivo_enc.setText(msm)

         
class ppg(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('PPG.ui',self)
        self._ventana_menu=parent
        self.setup()
    def setup(self):
        self.volver_bot.clicked.connect(self.opcion_volver)
        self.subir_arc.clicked.connect(self.Abrir_archivo)
    def opcion_volver(self):
        self.hide()
        self._ventana_menu.show()
    def Abrir_archivo(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Abrir archivo", "", "Todos los archivos (*)")
        if archivo:
            msm=f"Archivo seleccionado: {archivo}"
            self.archivo_enc.setText(msm)
        else:
            msm="No se seleccionó ningún archivo"
            self.archivo_enc.setText(msm)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana=pprincipal()
    ventana.show()
    sys.exit(app.exec_())