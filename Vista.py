import sys
from PyQt5.QtWidgets import QMainWindow, QDialog,QMessageBox,QFileDialog,QGraphicsScene,QGraphicsPixmapItem, QApplication
from PyQt5.QtGui import QDoubleValidator, QRegExpValidator,QIntValidator,QPixmap,QPainter
from PyQt5.QtCore import Qt,QRegExp
from PyQt5.uic import loadUi
from Controlador import *
from Procesador_RX import *
import masc_rc
import cuenta_rc
import masc2_rc
import rx_rc
import ppg_rc
import ecg_rc


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
    def Verificar_cred(self):
        cusuario=self.usu_input.text()
        ccontrasena=self.contra_input.text()
        self._ventana_pprincipal.Recibir_cred(cusuario,ccontrasena)
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
        self.escena = QGraphicsScene(self)
        self.imag_sub.setScene(self.escena)
        self.escena2 = QGraphicsScene(self)
        self.mostrar_imagen.setScene(self.escena2)
        self.setup()
    def setup(self):
        self.volver_bot.clicked.connect(self.opcion_volver)
        self.subir_arc.clicked.connect(self.Abrir_archivo)
        self.aceptar_bot.clicked.connect(self.Aceptar_opciones)
        self.guardar_img_proc.clicked.connect(self.guardar_imagen_perm)
        # b=self.brillo_lev.value()
        # c=self.contra_lev.value()
        # tam=self.tamano_lev.value()
        # ang=self.angulo.value()
        # filt=self.filtro_opc.currentText() 
        self.subir_arc_2.clicked.connect(self.Abrir_archivo2)
        # return b,c,tam,ang,filt
    def Abrir_archivo2(self):
        archivo2, _ = QFileDialog.getOpenFileName(self, "Abrir archivo", "", "Todos los archivos (*)")
        if archivo2:
            msm=f"Archivo seleccionado: {archivo2}"
            self.archivo_enc_2.setText(msm)
        else:
            msm="No se seleccionó ningún archivo"
        self.archivo_enc.setText(msm)
        return archivo2

        
    def Abrir_archivo(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Abrir archivo", "", "Todos los archivos (*)")
        if archivo:
            msm=f"Archivo seleccionado: {archivo}"
            self.archivo_enc.setText(msm)
            pixmap = QPixmap(archivo)
            pixmap_item = QGraphicsPixmapItem(pixmap)
            self.escena.addItem(pixmap_item)
            view_width = self.imag_sub.width()
            view_height = self.imag_sub.height()

            # Obtener las dimensiones de la imagen
            pixmap_width = pixmap.width()
            pixmap_height = pixmap.height()

            # Calcular la escala necesaria para ajustar la imagen dentro del QGraphicsView
            scale_x = view_width / pixmap_width
            scale_y = view_height / pixmap_height
            scale = min(scale_x, scale_y)  # Selecciona la menor escala para que la imagen no se deforme

            # Crear un QGraphicsPixmapItem y aplicar la escala
            pixmap_item = QGraphicsPixmapItem(pixmap)
            pixmap_item.setScale(scale)

            # Agregar el QGraphicsPixmapItem a la escena
            self.escena.addItem(pixmap_item)

            # Ajustar el área visible de la escena al tamaño de la imagen escalada
            self.escena.setSceneRect(0, 0, pixmap_width * scale, pixmap_height * scale)
        else:
            msm="No se seleccionó ningún archivo"
            self.archivo_enc.setText(msm)
            
        return archivo
    def Aceptar_opciones(self):
        opciones_activadas=False
        
        archivo = self.archivo_enc.toPlainText().replace("Archivo seleccionado: ", "").strip()
        archivo2 = self.archivo_enc_2.toPlainText().replace("Archivo seleccionado: ", "").strip()
        # arch=self.carg_arch(archivo)
        b = self.brillo_lev.value()
        c = self.contra_lev.value()
        tam = self.tamano_lev.value()
        ang = self.angulo.value()
        filt = self.filtro_opc.currentText()
        try:
            self.arch = self.carg_arch(archivo)
        except ValueError as e:
            self.archivo_enc.setText("Por favor, cargue un archivo válido antes de continuar.")
            self.hide()  # Ocultar la ventana actual
            self._ventana_menu.show()  # Mostrar la ventana del menú
            return
        # Verificar si se cargó el archivo
        # if not archivo:
        #     self.archivo_enc.setText("Por favor, cargue un archivo antes de continuar.")

        # Verificar cuáles CheckButtons están seleccionados
        if self.graf_histo.isChecked():
            self.histograma(self.arch)
            opciones_activadas = True
        if self.brillo.isChecked():
            self.pbrillo(self.arch,b,c)
            opciones_activadas = True
        if self.filtro.isChecked():
            opciones_activadas = True
            self.pfiltro(self.arch,filt)
        if self.tamano.isChecked():
            self.atamano(self.arch,tam)
            opciones_activadas = True
        if self.rotar.isChecked():
            self.rotari(self.arch,ang)
            opciones_activadas = True
        if self.sobreponer.isChecked():
            opciones_activadas = True
            self.sobreponeri(self.arch,archivo2)
        if not opciones_activadas:
            self.hide()
            self._ventana_menu.show()
        if not opciones_activadas and not archivo:
            self.hide()
            self._ventana_menu.show()
            
        self.mostrar_imagfinal(self.arch)
        return self.arch

    
    def carg_arch(self,archivo):
        arch=ProcesadorDeImagen(archivo)
        return arch
    def pbrillo(self,arch,b,c):
        arch.cambiarBC(b,c)
    def histograma(self,arch):
        arch.histograma()
    def pfiltro(self,arch,filt):
        arch.aplicar_filtro(filt)
    def atamano(self,arch,tam):
        arch.cambiar_tamano(tam)
    def rotari(self,arch,ang):
        arch.rotar(ang)
    def sobreponeri(self,arch,archivo2):
        arch.sobreponer(archivo2)
    def mostrar_imagfinal(self,arch):
        ruta_temporal="imagen_procesada.png"
        arch.guardar_imagen(ruta_temporal)
        pixmap2 = QPixmap(ruta_temporal)
        self.escena2.clear() 
        pixmap_item2 = QGraphicsPixmapItem(pixmap2)
        self.escena2.addItem(pixmap_item2)
       
        # Obtener las dimensiones de la imagen
        pixmap_width = pixmap2.width()
        pixmap_height = pixmap2.height()

        # Ajustar el área visible de la escena al tamaño de la imagen escalada
        self.escena2.setSceneRect(0, 0, pixmap_width, pixmap_height)
    def guardar_imagen_perm(self, arch):
        if self.arch is None:
            print("No se ha cargado ninguna imagen")
    # Abrir un cuadro de diálogo para que el usuario seleccione la ruta de guardado
        opciones_guardado = QFileDialog.Options()
        ruta_guardado, _ = QFileDialog.getSaveFileName(self, "Guardar imagen procesada", "", "Archivos PNG (*.png);;Archivos JPEG (*.jpg *.jpeg);;Todos los archivos (*)", options=opciones_guardado)

        # Verificar si se seleccionó una ruta válida
        if ruta_guardado:
            # Llamar al método para guardar la imagen en la ruta seleccionada
            self.arch.guardar_imagen(ruta_guardado)
            print(f"Imagen guardada en: {ruta_guardado}")
        else:
            print("No se seleccionó ninguna ruta.")


    def opcion_volver(self):
        self.hide()
        self._ventana_menu.show()
          
    def Mover_archivo_rx(self,archivo):
        self.__mi_controlador.Mover_archivo_rx(archivo)


    def Asignar_cont(self,c):
        self.__mi_controlador=c
        
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