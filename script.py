# Dependencias
from PyQt6.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QLineEdit, QSpinBox, QPushButton, QFileDialog, QWidget, QTextEdit, QProgressBar, QVBoxLayout, QTextEdit, QMainWindow, QStackedWidget, QHBoxLayout,QComboBox
from PyQt6.QtGui import QColor, QTextCharFormat
from PyQt6.QtCore import QMetaObject, Qt, pyqtSignal, Q_ARG
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from bs4 import BeautifulSoup
import requests
import openpyxl
import time
import os
import threading
import sys
from datetime import datetime
import json
import pandas as pd
from unidecode import unidecode
import Levenshtein
import glob

#Credenciales ususario
usuario=""
contrasena=""

def select_folder(self):
    # Obtener el directorio del script de Python
    script_directory = os.path.dirname(__file__) if __file__ else os.getcwd()

    folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta", script_directory)
    if folder_path:
        # Actualizar las variables de clase con la carpeta y la ruta seleccionadas
        selected_folder = folder_path
        selected_path = folder_path

        # Actualizar el QLineEdit con la ruta seleccionada
        self.text_input.setText(selected_path)

def select_folder2(self):
    # Obtener el directorio del script de Python
    script_directory = os.path.dirname(__file__) if __file__ else os.getcwd()

    folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta", script_directory)
    if folder_path:
        # Actualizar las variables de clase con la carpeta y la ruta seleccionadas
        selected_folder = folder_path
        selected_path = folder_path

        # Actualizar el QLineEdit con la ruta seleccionada
        self.text_input2.setText(selected_path)

def select_file(self):
    # Obtener el directorio del script de Python
    script_directory = os.path.dirname(__file__)

    # Abrir el cuadro de diálogo para seleccionar un archivo
    file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo", script_directory)

    if file_path:
        # Actualizar las variables de clase con el archivo y la ruta seleccionadas
        self.selected_file = os.path.basename(file_path)
        self.selected_path = file_path

        # Actualizar el QLineEdit con la ruta seleccionada
        self.text_file_input.setText(self.selected_path)

def select_file2(self):
    # Obtener el directorio del script de Python
    script_directory = os.path.dirname(__file__)

    # Abrir el cuadro de diálogo para seleccionar un archivo
    file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo", script_directory)

    if file_path:
        # Actualizar las variables de clase con el archivo y la ruta seleccionadas
        self.selected_file = os.path.basename(file_path)
        self.selected_path = file_path

        # Actualizar el QLineEdit con la ruta seleccionada
        self.text_file2_input.setText(self.selected_path)

def realizar_login(driver):

    driver.get("https://mister.mundodeportivo.com/new-onboarding/#market")
    driver.implicitly_wait(15)

    # Consentir
    consent_button = driver.find_element(By.XPATH, '//*[@id="didomi-notice-agree-button"]')
    consent_button.click()

    # Click en "Siguiente"
    siguiente_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/button')
    for _ in range(4):  # Haz clic 4 veces
        siguiente_button.click()

    # Click en "Sign in with gmail"
    gmail_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/button[3]')
    gmail_button.click()

    # Ingresar usuario
    input_gmail = driver.find_element(By.XPATH, '//*[@id="email"]')
    input_gmail.clear()
    input_gmail.send_keys(usuario)

    # Ingresar contraseña
    input_psw = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[2]/input')
    input_psw.clear()
    input_psw.send_keys(contrasena)

    # Click en "Sign in with gmail"
    login_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[3]/button')
    login_button.click()

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DraftGeniousIQ")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QGridLayout(self.central_widget)

        self.stacked_widget = QStackedWidget()

        self.ventana1 = squadWindow()
        self.ventana2 = marketWindow()
        self.ventana3 = scrapear_datos()
        self.ventana4 = dataset_creator()
        self.ventana5 = trainWindow()
        self.ventana6 = predictWindow()
        self.ventana7 = login()

        self.stacked_widget.addWidget(self.ventana1)
        self.stacked_widget.addWidget(self.ventana2)
        self.stacked_widget.addWidget(self.ventana3)
        self.stacked_widget.addWidget(self.ventana4)
        self.stacked_widget.addWidget(self.ventana5)
        self.stacked_widget.addWidget(self.ventana6)
        self.stacked_widget.addWidget(self.ventana7)

        self.btn_ventana1 = QPushButton("Mi plantilla")
        self.btn_ventana1.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        self.btn_ventana2 = QPushButton("Mercado")
        self.btn_ventana2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        self.btn_ventana3 = QPushButton("Obtener datos de futbolistas")
        self.btn_ventana3.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

        self.btn_ventana4 = QPushButton("Crear dataset")
        self.btn_ventana4.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))

        self.btn_ventana5 = QPushButton("Entrenar modelo")
        self.btn_ventana5.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))

        self.btn_ventana6 = QPushButton("Predecir")
        self.btn_ventana6.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))

        self.btn_ventana7 = QPushButton("Mi perfil")
        self.btn_ventana7.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(6))

        self.layout.addWidget(self.btn_ventana1, 0, 0)
        self.layout.addWidget(self.btn_ventana2, 0, 1)
        self.layout.addWidget(self.btn_ventana3, 0, 2)
        self.layout.addWidget(self.btn_ventana4, 0, 3)
        self.layout.addWidget(self.btn_ventana5, 0, 4)
        self.layout.addWidget(self.btn_ventana6, 0, 5)
        self.layout.addWidget(self.btn_ventana7, 0, 6)


        self.layout.addWidget(self.stacked_widget, 1, 0, 1, 7)


class squadWindow(QWidget):
    def __init__(self):
        super().__init__()

        #Varaible para guardar la plantilla scrapeada
        self.nombres_jugadores=[]

        # Crear un diseño principal usando QVBoxLayout
        layout = QVBoxLayout()

        # Crear un diseño de cuadrícula dentro del QVBoxLayout
        grid_layout = QGridLayout(self)

        # TITULO VENTANA  ###########################################################################################
        # LABEL TÍTULO
        label_text = QLabel("MI PLANTILLA")
        # Aplicar estilos para destacar el texto
        label_text.setStyleSheet("font-weight: bold; color: black; font-size: 20px;")
        grid_layout.addWidget(label_text, 0, 0)

        # LABEL SUBTÍTULO
        label_subtext = QLabel("Obten el listado de todos los jugaodres en mi plantilla de Mister Fantasy MD")
        grid_layout.addWidget(label_subtext, 1, 0, 1, 2)

        # BOTÓN PARA INICIAR LA OBTENCIÓN DE MI PLANTILLA ###########################################################
        # Crear un botón
        self.scrape_button = QPushButton("Obtener mi plantilla")

        # Conectar la señal clicked del botón a la función iniciar_scrapear_thread e iniciar la barra de progreso
        self.scrape_button.clicked.connect(self.iniciar_scrapear_thread)

        # Alineación y estilos
        grid_layout.addWidget(self.scrape_button, 2, 0)
        self.scrape_button.setMaximumWidth(150)

        # VENTANA OUTPUT SCRAPER ####################################################################################
        # Crear un QTextEdit para la salida
        self.output_textedit = QTextEdit(self)
        grid_layout.addWidget(self.output_textedit, 3, 0, 10, 2)  # row, column, rowSpan, columnSpan

        # SELECCIONAR RUTA DONDE GUARDAR EL EXCEL OUTPUT DEL SCRAPER #################################################
        # LABEL DE TEXTO
        label_text = QLabel("Guardar mi plantilla:")
        grid_layout.addWidget(label_text, 13, 0)

        # INPUT DE TEXTO
        self.text_input = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input, 13, 1)

        # BOTÓN PARA SELECCIONAR CARPETA
        select_folder_button = QPushButton("Seleccionar Carpeta")
        select_folder_button.clicked.connect(lambda: select_folder(self))
        # Alineación
        grid_layout.addWidget(select_folder_button, 14, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos
        select_folder_button.setMinimumWidth(140)

        # BOTÓN PARA GUARDAR MI PLANTILLA ###########################################################################
        # Crear un botón
        self.save_button = QPushButton("Guardar plantilla")

        # Conectar la señal clicked del botón a la función iniciar_scrapear_thread e iniciar la barra de progreso
        self.save_button.clicked.connect(self.guardar_excell)

        # Alineación
        grid_layout.addWidget(self.save_button, 15, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos
        self.save_button.setMinimumWidth(100)
        self.save_button.setMaximumWidth(150)
    

        # Agregar el diseño de cuadrícula al diseño principal
        layout.addLayout(grid_layout)

        # Agregar el diseño principal al widget
        self.setLayout(layout)

    def guardar_excell(self):
        self.output_textedit.append(f"________________________________________________________________________________________")
        output_textedit = self.output_textedit
        color_azul = QColor(0, 0, 255)  # Valores RGB para azul
        formato_azul = QTextCharFormat()
        formato_azul.setForeground(color_azul)
        output_textedit.mergeCurrentCharFormat(formato_azul)
        output_textedit.insertPlainText("\nGuardando plantilla...\n")
        formato_negro = QTextCharFormat()
        formato_negro.setForeground(QColor(0, 0, 0))
        output_textedit.mergeCurrentCharFormat(formato_negro)

        if len(self.nombres_jugadores) > 0:
            # Obtener la fecha actual
            fecha_actual = datetime.now()

            # Formatear la fecha como una cadena (opcional)
            fecha_actual_str = fecha_actual.strftime("%Y-%m-%d--%H-%M-S")

            ruta_output = self.text_input.text()
            excel_file_path= ruta_output +"/mi_plantilla"+fecha_actual_str+".xlsx"
            
            # Crear un nuevo libro de Excel
            workbook = openpyxl.Workbook()

            # Seleccionar la hoja activa (por defecto, es la primera hoja)
            sheet = workbook.active

            # Iterar sobre la lista y almacenar cada elemento en una nueva fila
            for index, nombre in enumerate(self.nombres_jugadores, start=1):
                sheet.cell(row=index, column=1, value=nombre)

            # Guardar el libro de Excel
            workbook.save(excel_file_path)
            self.output_textedit.append(f"Plantilla guardada en {excel_file_path}")
        else:
            output_textedit = self.output_textedit
            color_rojo = QColor(255, 0, 0)  # Valores RGB para rojo
            formato_rojo = QTextCharFormat()
            formato_rojo.setForeground(color_rojo)
            output_textedit.mergeCurrentCharFormat(formato_rojo)
            output_textedit.insertPlainText("\n¡La plantilla no se puede guardar porque no esta inicializada")
            formato_negro = QTextCharFormat()
            formato_negro.setForeground(QColor(0, 0, 0))
            output_textedit.mergeCurrentCharFormat(formato_negro)

    def iniciar_scrapear_thread(self):
        # Crear un hilo y ejecutar la función en segundo plano
        thread = threading.Thread(target=self.scrapear_funcion)
        thread.start()

    def click_mas(self):
        # Pinchar en el botón del menu "Más"
        masMenu = self.driver.find_element(By.XPATH, '//*[@id="content"]/header/div[2]/ul/li[3]/a')

        try:
            masMenu.click()
        except (ElementNotInteractableException, NoSuchElementException):
            # Maneja la excepción y espera antes de intentar nuevamente
            self.output_textedit.append("Anuncio detectado, reiniciando driver...")
            self.driver.refresh()
            time.sleep(3) 
            masMenu.click()

    def scrapear_funcion(self):
        self.output_textedit.append(f"________________________________________________________________________________________")
        output_textedit = self.output_textedit
        color_azul = QColor(0, 0, 255)  # Valores RGB para azul
        formato_azul = QTextCharFormat()
        formato_azul.setForeground(color_azul)
        output_textedit.mergeCurrentCharFormat(formato_azul)
        output_textedit.insertPlainText("\nObteniendo plantilla...\n")
        formato_negro = QTextCharFormat()
        formato_negro.setForeground(QColor(0, 0, 0))
        output_textedit.mergeCurrentCharFormat(formato_negro)
       
        if usuario!="":
            try:
                self.driver = webdriver.Chrome()
                realizar_login(self.driver)
                time.sleep(5)

                # Espera a que se cargue la página
                self.driver.implicitly_wait(10)

                #Hacer click en el btn Jugadores con la función click_mas() para manejar errores generados por anuncios intrusiovos
                self.click_mas()

                # Encontrar el elemento div con la clase "team__squad"
                team_squad_div = self.driver.find_element(By.CLASS_NAME, 'team__squad')

                # Encontrar todos los elementos con la clase "name" dentro del div
                names_elements = team_squad_div.find_elements(By.CLASS_NAME, 'name')

                # Iterar sobre los elementos encontrados e imprimir el texto
                for name_element in names_elements:
                    self.output_textedit.append(name_element.text)
                    self.nombres_jugadores.append(name_element.text)

                self.driver.quit()

            except: 
                output_textedit = self.output_textedit
                color_rojo = QColor(255, 0, 0)  # Valores RGB para rojo
                formato_rojo = QTextCharFormat()
                formato_rojo.setForeground(color_rojo)
                output_textedit.mergeCurrentCharFormat(formato_rojo)
                output_textedit.insertPlainText('Algo salió mal, vuelve a intentarlo   :(\n')
                formato_negro = QTextCharFormat()
                formato_negro.setForeground(QColor(0, 0, 0))
                output_textedit.mergeCurrentCharFormat(formato_negro)
        else:
            output_textedit = self.output_textedit
            color_rojo = QColor(255, 0, 0)  # Valores RGB para rojo
            formato_rojo = QTextCharFormat()
            formato_rojo.setForeground(color_rojo)
            output_textedit.mergeCurrentCharFormat(formato_rojo)
            output_textedit.insertPlainText('No te has iniciado sesion en la aplicación. Loguearte con tus credenciales de Mister Fantasy MD en la ventana Perfil para acceder a tu plantilla.\n')
            formato_negro = QTextCharFormat()
            formato_negro.setForeground(QColor(0, 0, 0))
            output_textedit.mergeCurrentCharFormat(formato_negro)

class marketWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # Crear un diseño principal usando QVBoxLayout
        layout = QVBoxLayout()

        # Crear un diseño de cuadrícula dentro del QVBoxLayout
        grid_layout = QGridLayout(self)

        #Varaible para guardar la plantilla scrapeada
        self.nombres_jugadores=[]
        
        # TITULO VENTANA  ###########################################################################################
        # LABEL TÍTULO
        label_text = QLabel("MERCADO")
        # Aplicar estilos para destacar el texto
        label_text.setStyleSheet("font-weight: bold; color: black; font-size: 20px;")
        grid_layout.addWidget(label_text, 0, 0)

        # LABEL SUBTÍTULO
        label_subtext = QLabel("Obten el listado de todos los jugaodres en venta en el mercado de Mister Fantasy MD")
        grid_layout.addWidget(label_subtext, 1, 0, 1, 2)

        # BOTÓN PARA INICIAR LA OBTENCIÓN DE MI PLANTILLA ###########################################################
        # Crear un botón
        self.scrape_button = QPushButton("Obtener jugaodres en venta")

        # Conectar la señal clicked del botón a la función iniciar_scrapear_thread e iniciar la barra de progreso
        self.scrape_button.clicked.connect(self.iniciar_scrapear_thread)

        # Alineación y estilos
        grid_layout.addWidget(self.scrape_button, 2, 0)
        self.scrape_button.setMaximumWidth(190)

        # VENTANA OUTPUT SCRAPER #####################################################################################
        # Crear un QTextEdit para la salida
        self.output_textedit = QTextEdit(self)
        grid_layout.addWidget(self.output_textedit, 3, 0, 11, 2)  # row, column, rowSpan, columnSpan

        # SELECCIONAR RUTA DONDE GUARDAR EL EXCEL OUTPUT DEL SCRAPER ##################################################
        # LABEL DE TEXTO
        label_text = QLabel("Guardar jugadores en venta:")
        grid_layout.addWidget(label_text, 15, 0)

        # INPUT DE TEXTO
        self.text_input = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input, 15, 1)

        # BOTÓN PARA SELECCIONAR CARPETA
        select_folder_button = QPushButton("Seleccionar Carpeta")
        select_folder_button.clicked.connect(lambda: select_folder(self))
        # Alineación
        grid_layout.addWidget(select_folder_button, 16, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos
        select_folder_button.setMinimumWidth(140)

        # BOTÓN PARA GUARDAR MI PLANTILLA ###########################################################################
        # Crear un botón
        self.save_button = QPushButton("Guardar jugadores")

        # Conectar la señal clicked del botón a la función iniciar_scrapear_thread e iniciar la barra de progreso
        self.save_button.clicked.connect(self.guardar_excell)

        # Alineación
        grid_layout.addWidget(self.save_button, 17, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos
        self.save_button.setMinimumWidth(100)
        self.save_button.setMaximumWidth(150)

        # Agregar el diseño de cuadrícula al diseño principal
        layout.addLayout(grid_layout)

        # Agregar el diseño principal al widget
        self.setLayout(layout)


    def guardar_excell(self):
        self.output_textedit.append(f"________________________________________________________________________________________")
        output_textedit = self.output_textedit
        color_azul = QColor(0, 0, 255)  # Valores RGB para azul
        formato_azul = QTextCharFormat()
        formato_azul.setForeground(color_azul)
        output_textedit.mergeCurrentCharFormat(formato_azul)
        output_textedit.insertPlainText("\nGuardando plantilla...\n")
        formato_negro = QTextCharFormat()
        formato_negro.setForeground(QColor(0, 0, 0))
        output_textedit.mergeCurrentCharFormat(formato_negro)

        if len(self.nombres_jugadores) > 0:
            # Obtener la fecha actual
            fecha_actual = datetime.now()

            # Formatear la fecha como una cadena (opcional)
            fecha_actual_str = fecha_actual.strftime("%Y-%m-%d--%H-%M-S")

            ruta_output = self.text_input.text()
            excel_file_path= ruta_output +"/mercado"+fecha_actual_str+".xlsx"
            
            # Crear un nuevo libro de Excel
            workbook = openpyxl.Workbook()

            # Seleccionar la hoja activa (por defecto, es la primera hoja)
            sheet = workbook.active

            # Iterar sobre la lista y almacenar cada elemento en una nueva fila
            for index, nombre in enumerate(self.nombres_jugadores, start=1):
                sheet.cell(row=index, column=1, value=nombre)

            # Guardar el libro de Excel
            workbook.save(excel_file_path)
            self.output_textedit.append(f"Plantilla guardada en {excel_file_path}")
        else:
            output_textedit = self.output_textedit
            color_rojo = QColor(255, 0, 0)  # Valores RGB para rojo
            formato_rojo = QTextCharFormat()
            formato_rojo.setForeground(color_rojo)
            output_textedit.mergeCurrentCharFormat(formato_rojo)
            output_textedit.insertPlainText("\n¡La plantilla no se puede guardar porque no esta inicializada")
            formato_negro = QTextCharFormat()
            formato_negro.setForeground(QColor(0, 0, 0))
            output_textedit.mergeCurrentCharFormat(formato_negro)

    def click_mas(self):
        # Pinchar en el botón del menu "Más"
        masMenu = self.driver.find_element(By.XPATH, '//*[@id="content"]/header/div[2]/ul/li[2]/a')

        try:
            masMenu.click()
        except (ElementNotInteractableException, NoSuchElementException):
            # Maneja la excepción y espera antes de intentar nuevamente
            self.output_textedit.append("Anuncio detectado, reiniciando driver...")
            self.driver.refresh()
            time.sleep(3) 
            masMenu.click()

    def iniciar_scrapear_thread(self):
        # Crear un hilo y ejecutar la función en segundo plano
        thread = threading.Thread(target=self.scrapear_funcion)
        thread.start()

    def scrapear_funcion(self):
        self.output_textedit.append(f"________________________________________________________________________________________")
        output_textedit = self.output_textedit
        color_azul = QColor(0, 0, 255)  # Valores RGB para azul
        formato_azul = QTextCharFormat()
        formato_azul.setForeground(color_azul)
        output_textedit.mergeCurrentCharFormat(formato_azul)
        output_textedit.insertPlainText("\nObteniendo jugadores en el mercado...\n")
        formato_negro = QTextCharFormat()
        formato_negro.setForeground(QColor(0, 0, 0))
        output_textedit.mergeCurrentCharFormat(formato_negro)

        if usuario!="":
            try:
                self.driver = webdriver.Chrome()
                realizar_login(self.driver)
                time.sleep(5)

                # Espera a que se cargue la página
                self.driver.implicitly_wait(10)

                #Hacer click en el btn Jugadores con la función click_mas() para manejar errores generados por anuncios intrusiovos
                self.click_mas()

                # Encuentra el elemento <ul> con el id "list-on-sale"
                ul_element = self.driver.find_element(By.ID, "list-on-sale")

                # Encuentra los elementos <div> con la clase "name" dentro del elemento <ul>
                div_elements = ul_element.find_elements(By.CSS_SELECTOR, "div.name")

                # Itera sobre los elementos <div> encontrados e imprime el nombre del jugador
                for div_element in div_elements:
                    # Obtener el contenido del elemento <div>
                    name_element = div_element.text.strip()  # Utiliza strip() para eliminar espacios en blanco adicionales
                    output_textedit.insertPlainText(f"{name_element}\n")
                    self.nombres_jugadores.append(name_element)
            except:
                output_textedit = self.output_textedit
                color_rojo = QColor(255, 0, 0)  # Valores RGB para rojo
                formato_rojo = QTextCharFormat()
                formato_rojo.setForeground(color_rojo)
                output_textedit.mergeCurrentCharFormat(formato_rojo)
                output_textedit.insertPlainText('Algo salió mal, vuelve a intentarlo   :(\n')
                formato_negro = QTextCharFormat()
                formato_negro.setForeground(QColor(0, 0, 0))
                output_textedit.mergeCurrentCharFormat(formato_negro)

            self.driver.quit()
        else:
            output_textedit = self.output_textedit
            color_rojo = QColor(255, 0, 0)  # Valores RGB para rojo
            formato_rojo = QTextCharFormat()
            formato_rojo.setForeground(color_rojo)
            output_textedit.mergeCurrentCharFormat(formato_rojo)
            output_textedit.insertPlainText('No te has iniciado sesion en la aplicación. Loguearte con tus credenciales de Mister Fantasy MD en la ventana Perfil para acceder al mercado de jugaodes.\n')
            formato_negro = QTextCharFormat()
            formato_negro.setForeground(QColor(0, 0, 0))
            output_textedit.mergeCurrentCharFormat(formato_negro)


class dataset_creator(QWidget):
  def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)

        self.stacked_widget = QStackedWidget()

        self.ventana1 = dataset_entrenamiento()
        self.ventana2 = dataset_predecir()

        self.stacked_widget.addWidget(self.ventana1)
        self.stacked_widget.addWidget(self.ventana2)

        button_layout = QHBoxLayout()  

        self.btn_ventana1 = QPushButton("Generar dataset para entrenar modelos")
        self.btn_ventana1.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        self.btn_ventana2 = QPushButton("Generar dataset para predecir valores")
        self.btn_ventana2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        button_layout.addWidget(self.btn_ventana1)
        button_layout.addWidget(self.btn_ventana2)

        main_layout.addLayout(button_layout)  
        main_layout.addWidget(self.stacked_widget)

class dataset_entrenamiento(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.jugadoresS_noencontrados = ["Marc-André ter Stegen", "Adria Miquel Bosch Sanchis", "Sergio Ruiz Alonso", "Abderrahman Rebbach", "Kaiky", "Alejandro Pozo", "Lázaro", "Luis Javier Suárez", "Abdessamad Ezzalzouli", "Iván Cuéllar", "Djené", "Maximiliano Gómez", "Mamadou Mbaye", "Fali", "Anthony Lozano", "José María Giménez", "Sandro Ramírez", "Reinildo Isnard Mandava", "Chimy Ávila", "Pablo Ibáñez Lumbreras", "Portu", "Juan Carlos", "José Manuel Arnáiz", "Federico Valverde", "Alfonso Espino", "Ismaila Ciss", "Josep Chavarría", "José Pozo", "Imanol García de Albéniz", "Peru Nolaskoain Esnal", "Malcom Ares"] 
        self.jugadoresMD_noencontrados = ["Ter Stegen", "Miki Bosch", "Sergio Ruiz", "Abde Rebbach", "Kaiky Fernandes", "Álex Pozo", "Lázaro Vinicius", "Luis Suárez", "Abde Ezzalzouli", "Pichu Cuéllar", "Dakonam Djené", "Maxi Gómez", "Momo Mbaye", "Fali Giménez", "Choco Lozano", "José Giménez", "Sandro", "Reinildo Mandava", "Ezequiel Ávila", "Pablo Ibáñez", "Cristian Portu", "Juan Carlos Martín", "José Arnaiz", "Fede Valverde", "Pacha Espino", "Pathé Ciss", "Pep Chavarría", "José Ángel Pozo", "Imanol García", "Peru Nolaskoain", "Malcom Adu Ares"]

        # Crear un diseño de cuadrícula dentro del QVBoxLayout
        grid_layout = QGridLayout(self)
       
        # TITULO VENTANA  ###########################################################################################
        # LABEL TÍTULO
        label_text = QLabel("Crear dataset para una jornada de LaLiga")
        # Aplicar estilos para destacar el texto
        label_text.setStyleSheet("font-weight: bold; color: black; font-size: 20px;")
        grid_layout.addWidget(label_text, 0, 0)

        # LABEL SUBTÍTULO
        label_subtext = QLabel("Crea un dataset para entrenar un modelo de predicción")
        grid_layout.addWidget(label_subtext, 1, 0, 1, 2)

        ### SELECCIONAR JORNADA INPUT ####################################################
        # INPUT NÚMERO JORNADA 
        label_number = QLabel("Jornada a scrapear:")
        grid_layout.addWidget(label_number, 2, 0)
        # Estilos 
        self.number_input = QSpinBox(self)
        self.number_input.setMinimum(1)  # Establecer el valor mínimo (jornada 1)
        self.number_input.setMaximum(38)  # Establecer el valor máximo (Jornada 36)
        self.number_input.setSingleStep(2)  # Establecer el paso
        self.number_input.setMaximumSize(38, 20)
        self.number_input.setMinimumSize(38, 20)
        # Aliniación
        grid_layout.addWidget(self.number_input, 3, 0)

        ### SELECCIONAR RUTA DATASET DE ENTRADA SOFAESCORE #########################################################################
        # LABEL DE TEXTO
        label_text = QLabel("Selecionar carpeta donde se almacenaron tododos los partidos scrapeados de la jornada de la web de Sofaescore: ")
        grid_layout.addWidget(label_text, 4, 0)

        # INPUT DE TEXTO
        self.text_input = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input, 5, 0)

        # BOTÓN PARA SELECCIONAR CARPETA
        select_folder_button = QPushButton("Seleccionar Carpeta")
        select_folder_button.clicked.connect(lambda: select_folder(self))
        # Alineación
        grid_layout.addWidget(select_folder_button, 6, 0, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos
        select_folder_button.setMinimumWidth(140)

        ### SELECCIONAR RUTA DATASET DE ENTRADA MISTER FANTASY #####################################################################
        # LABEL DE TEXTO
        label_text = QLabel("Selecionar archivo resultante del scrapeo de la jornada de la web de Mister Fantasy Mundo Deportivo: ")
        grid_layout.addWidget(label_text, 7, 0)

        # INPUT DE TEXTO
        self.text_file_input= QLineEdit(self)  
        # Alineación
        grid_layout.addWidget(self.text_file_input, 8, 0)

        # BOTÓN PARA SELECCIONAR ARCHIVO
        select_file_button = QPushButton("Seleccionar archivo")
        select_file_button.clicked.connect(lambda: select_file(self))

        # Alineación
        grid_layout.addWidget(select_file_button, 9, 0, alignment=Qt.AlignmentFlag.AlignRight)

        # Estilos
        select_file_button.setMinimumWidth(140)

        ### SELECCIONAR RUTA DONDE GUARDAR DATASET RESULTANTE #####################################################################
        # LABEL DE TEXTO
        label_text = QLabel("Selecionar ruta donde guardar el dataset generado de la jornada: ")
        grid_layout.addWidget(label_text, 10, 0)

        # INPUT DE TEXTO
        self.text_input2 = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input2, 11, 0)

        # BOTÓN PARA SELECCIONAR ARCHIVO
        select_folder_button = QPushButton("Seleccionar carpeta")
        select_folder_button.clicked.connect(lambda: select_folder2(self))

        # Alineación
        grid_layout.addWidget(select_folder_button, 12, 0, alignment=Qt.AlignmentFlag.AlignRight)

        # Estilos
        select_file_button.setMinimumWidth(140)

        ### BOTÓN PARA EJECUTAR FUNCIÓN PARA FUSIONAR EXCELLS ######################################################################
        # Crear un botón
        self.generate_button = QPushButton("Generar dataset")

        # Conectar la señal clicked del botón a la función iniciar_scrapear_thread e iniciar la barra de progreso
        self.generate_button.clicked.connect(self.iniciar_thread_function)

        # Alineación
        grid_layout.addWidget(self.generate_button, 13, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        # Estilos
        self.generate_button.setMinimumWidth(100)
        self.generate_button.setMaximumWidth(150)

        # VENTANA OUTPUT SCRAPER #####################################################################################
        # Crear un QTextEdit para la salida
        self.output_textedit = QTextEdit(self)
        grid_layout.addWidget(self.output_textedit,14, 0, 2, 2)  # row, column, rowSpan, columnSpan
    
    def iniciar_thread_function(self):  
        # Crear un hilo y ejecutar la función en segundo plano
        thread = threading.Thread(target=self.json_a_excel)
        thread.start()

    def json_a_excel(self):

        def guardar_en_excell():

            output = self.text_input2.text()
            numero_jornada = str(self.number_input.value())
            output_archivo=output+"/dataset_completo_jornada"+numero_jornada+".xlsx"

            # Obtener las listas de las filas
            fila_excel1 = df1.iloc[index_df1, :].tolist()
            fila_excel2 = df2.iloc[index_df2, :].tolist()

            # Concatenar las listas
            fila_concatenada = fila_excel2 + fila_excel1

            # Crear un DataFrame de pandas con una sola fila y múltiples columnas
            df_nueva_fila = pd.DataFrame([fila_concatenada])

            # Leer el archivo Excel existente
            df_existente = pd.read_excel(output_archivo, header=None)

            # Concatenar el DataFrame existente con la nueva fila
            df_final = pd.concat([df_existente, df_nueva_fila], ignore_index=True)

            # Escribir el DataFrame final en el archivo Excel
            df_final.to_excel(output_archivo, index=False, header=False)

        # Parte 1: fusionar todos los jsons de todos los partidos scrapeados de la jornada ##############################################
        # Rutas globales
        carpeta_json = self.text_input.text()
        carpeta_xlsx = self.text_input.text()
        nombre_archivo_excel = 'todos_los_partidos_de_la_jornada.xlsx'

        # Lista para almacenar los DataFrames de cada archivo JSON
        dfs = []

        # Iterar sobre cada archivo en la carpeta
        for archivo_json in os.listdir(carpeta_json):
            if archivo_json.endswith(".json"):
                with open(os.path.join(carpeta_json, archivo_json), "r") as file:
                    data = json.load(file)

                # Crear un DataFrame vacío para cada archivo JSON
                df = pd.DataFrame()

                # Iterar sobre los elementos del JSON y agregarlos al DataFrame
                for jugador, estadisticas in data.items():
                    df = pd.concat([df, pd.DataFrame([[jugador, estadisticas["puntuacion"]] + [stat[key] for stat in estadisticas["estadisticas"] for key in stat.keys()]], columns=["Nombre", "Puntuación"] + [key for stat in estadisticas["estadisticas"] for key in stat.keys()])], ignore_index=True)

                # Agregar el DataFrame a la lista
                dfs.append(df)

        # Concatenar todos los DataFrames en uno solo
        df_final = pd.concat(dfs, ignore_index=True)

        # Guardar el DataFrame en un archivo Excel
        ruta_excel = os.path.join(carpeta_xlsx, nombre_archivo_excel)
        df_final.to_excel(ruta_excel, index=False)

        self.output_textedit.insertPlainText(f"Archivo Excel con todos los partidos scrpaeados de la jornada fusionado y guardado correctamente en: {ruta_excel}\n")

        # Parte 2: Fusionar MD con SC por nombre ########################################################################################
        # Rutas de los archivos Excel
        excel1_path = ruta_excel
        excel2_path = self.text_file_input.text()
        output = self.text_input2.text()
        numero_jornada = str(self.number_input.value())
        output_archivo=output+"/dataset_completo_jornada"+numero_jornada+".xlsx"
        
        # Leer los datos de los archivos Excel
        df1 = pd.read_excel(excel1_path, header=None)
        df2 = pd.read_excel(excel2_path, header=None)
        
        # Obtener todas las celdas de la fila 1 (que ahora es la segunda fila después de desactivar el encabezado)
        fila_excel1 = df1.iloc[0, :].dropna().tolist()
        fila_excel2 = df2.iloc[0, :].dropna().tolist()

        # Concatenar las listas
        fila_concatenada =  fila_excel2 + fila_excel1

        # Crear un DataFrame de pandas con una sola fila y múltiples columnas
        df = pd.DataFrame([fila_concatenada])


        # Escribir el DataFrame en un archivo Excel
        df.to_excel(output_archivo, index=False, header=False)

        # Inicializar el conjunto de valores encontrados
        valores_encontrados = set()
        df_fusionado = pd.DataFrame()
        encabezado=0
        contador_coincidencias=0
        contador_manual=0
        contador_global=0
        
        self.output_textedit.insertPlainText("_____________________________________________________________________________________________________\n")   
        self.output_textedit.insertPlainText("Buscando coincidencia entre jugadores...\n")
        
        # Iterar sobre las filas de df1 y comparar con las filas de df2
        for index_df1, row_df1 in df1.iterrows():
            value_to_compare1o =row_df1.iloc[0] 
            value_to_compare1 =value_to_compare1o.lower()
            value_to_compare1 =unidecode(value_to_compare1)
            value_to_compare1 =unidecode(value_to_compare1)
            value_to_compare1=value_to_compare1.replace(" ", "")
            
            coincidencia_encontrada = False
            contador_global+=1
            # Iterar sobre las filas de df2
            for index_df2, row_df2 in df2.iterrows():
                #print("-----",value_to_compare1,"-----",value_to_compare2,"-----")
                value_to_compare2o =row_df2.iloc[0]
                value_to_compare2 =value_to_compare2o.lower()
                value_to_compare2 =unidecode(value_to_compare2)
                value_to_compare2 = unidecode(value_to_compare2)
                value_to_compare2=value_to_compare2.replace(" ", "")
                
                # Calcular la distancia de Levenshtein
                distancia = Levenshtein.distance(value_to_compare1, value_to_compare2)
                # Establecer un umbral para considerar coincidencias
                umbral = 2  

                if distancia <= umbral:
                    self.output_textedit.insertPlainText(f"Coincidencia encontrada: excell1-fila-{index_df1} <-> excell2-fila.{index_df2} , {value_to_compare1} == {value_to_compare2}\n")
                    valores_encontrados.add(value_to_compare1) 

                    guardar_en_excell()

                    contador_coincidencias +=1
                    coincidencia_encontrada = True
                    time.sleep(0.02)

            # Imprimir si no se encontró ninguna coincidencia
            if not coincidencia_encontrada:
                if value_to_compare1!="nombre":
                    self.output_textedit.insertPlainText("------------------------------------------------------------------------------------------------\n")
                    self.output_textedit.insertPlainText(f"Coincidencia NO encontrada: excell1-fila-{index_df1} en {value_to_compare1}\n")
                    self.output_textedit.insertPlainText("------------------------------------------------------------------------------------------------\n")
        
        #Estadisticas de la fusion de los datasets
        self.output_textedit.insertPlainText("_____________________________________________________________________________________________________\n")       
        self.output_textedit.insertPlainText("Buscando jugaodres manualmente que no hicieron match...\n")
        for jugadorS, jugadorMD in zip(self.jugadoresS_noencontrados, self.jugadoresMD_noencontrados):
            for index_df1, row_df1 in df1.iterrows():
                value_to_compare1o = row_df1.iloc[0]
                for index_df2, row_df2 in df2.iterrows():
                    value_to_compare2o = row_df2.iloc[0]

                    if value_to_compare1o == jugadorS and value_to_compare2o == jugadorMD:
                        self.output_textedit.insertPlainText(f"Coincidencia encontrada: {jugadorS}\n")
                        guardar_en_excell()
                        contador_manual+=1
            
        #Resultados de la fusión de datasets
        self.output_textedit.insertPlainText("\n_____________________________________________________________________________________________________\n")
        self.output_textedit.insertPlainText(f"Total coincidencias: {contador_coincidencias} / {contador_global-1}\n")
        self.output_textedit.insertPlainText(f"Añadidos manualmente: {contador_manual}\n")
        self.output_textedit.insertPlainText(f"Jugadores no disponibles en MisterFantasy: {((contador_global-1)-(contador_coincidencias+contador_manual))}\n")
        self.output_textedit.insertPlainText(f"Precisión: {(((contador_coincidencias+contador_manual)/(contador_global-1))*100)} %\n")
        self.output_textedit.insertPlainText("Dataset generado correctamente\n")

class dataset_predecir(QWidget):
    
    def __init__(self):
        super().__init__()

        # Crear un diseño de cuadrícula dentro del QVBoxLayout
        grid_layout = QGridLayout(self)
       
        # TITULO VENTANA  ###########################################################################################
        # LABEL TÍTULO
        label_text = QLabel("Crear dataset sobre el que realizar prediciones")
        # Aplicar estilos para destacar el texto
        label_text.setStyleSheet("font-weight: bold; color: black; font-size: 20px;")
        grid_layout.addWidget(label_text, 0, 0)

        # LABEL SUBTÍTULO
        label_subtext = QLabel("Crea un dataset con los jugaodores en mi plantilla / en el mercado para realizar prediciones sobre su puntuación / valor de mercado en la prócima jornada")
        grid_layout.addWidget(label_subtext, 1, 0, 1, 2)


        ### SELECCIONAR RUTA DATASET DE ENTRADA SOFAESCORE #########################################################################
        # LABEL DE TEXTO
        label_text = QLabel("Selecionar fichero con los jugaodres en el mercado/ en mi plantilla : ")
        grid_layout.addWidget(label_text, 2, 0)

        # INPUT DE TEXTO
        self.text_input = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input, 3, 0)

        # BOTÓN PARA SELECCIONAR CARPETA
        select_folder_button = QPushButton("Seleccionar Carpeta")
        select_folder_button.clicked.connect(lambda: select_file(self))
        # Alineación
        grid_layout.addWidget(select_folder_button, 4, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        # Estilos
        select_folder_button.setMinimumWidth(140)


class scrapear_datos(QWidget):
  def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)

        self.stacked_widget = QStackedWidget()

        self.ventana1 = PlayerScraperWindowMF("Players Scraper")
        self.ventana2 = PlayerScraperWindowSC()

        self.stacked_widget.addWidget(self.ventana1)
        self.stacked_widget.addWidget(self.ventana2)

        button_layout = QHBoxLayout()  

        self.btn_ventana1 = QPushButton("Extraer datos de Mister Fantasy Mundo Deportivo")
        self.btn_ventana1.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        self.btn_ventana2 = QPushButton("Extraer datos de Sofaescore")
        self.btn_ventana2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        button_layout.addWidget(self.btn_ventana1)
        button_layout.addWidget(self.btn_ventana2)

        main_layout.addLayout(button_layout)  
        main_layout.addWidget(self.stacked_widget)

class PlayerScraperWindowSC(QWidget):
    def __init__(self):
        super().__init__()
        # Crear un diseño de cuadrícula
        layout = QGridLayout(self)

        # TITULO VENTANA  ###########################################################################################
        # LABEL TÍTULO
        label_text = QLabel("Sofaescore Scraper")
        # Aplicar estilos para destacar el texto
        label_text.setStyleSheet("font-weight: bold; color: black; font-size: 20px;")
        layout.addWidget(label_text, 0, 0,1, 2)

        # LABEL SUBTÍTULO
        label_subtext = QLabel("Obtener el listado de todos los jugaodres titulares, suplentes y no vonvocados y sus estadisticas de juego asociadas.")
        layout.addWidget(label_subtext, 1, 0, 1, 2)

        # Configurar el diseño para la ventana
        self.setLayout(layout)

class PlayerScraperWindowMF(QDialog, QWidget):
    def __init__(self, window_title):
        super().__init__()
        self.setWindowTitle(window_title)

        self.teams_data = {
        "Real Madrid": "https://cdn.gomister.com/file/cdn-common/teams/15.png?version=20231117",
        "Real Sociedad": "https://cdn.gomister.com/file/cdn-common/teams/16.png?version=20231117",
        "Atlético de Madrid": "https://cdn.gomister.com/file/cdn-common/teams/2.png?version=20231117",
        "Girona": "https://cdn.gomister.com/file/cdn-common/teams/222.png?version=20231117",
        "Osasuna": "https://cdn.gomister.com/file/cdn-common/teams/50.png?version=20231117",
        "Athletic Club": "https://cdn.gomister.com/file/cdn-common/teams/1.png?version=20231117",
        "Valencia": "https://cdn.gomister.com/file/cdn-common/teams/19.png?version=20231117",
        "Granada": "https://cdn.gomister.com/file/cdn-common/teams/10.png?version=20231117",
        "Getafe": "https://cdn.gomister.com/file/cdn-common/teams/9.png?version=20231117",
        "Villarreal": "https://cdn.gomister.com/file/cdn-common/teams/20.png?version=20231117",
        "Las Palmas": "https://cdn.gomister.com/file/cdn-common/teams/11.png?version=20231117",
        "Mallorca": "https://cdn.gomister.com/file/cdn-common/teams/408.png?version=20231117",
        "Rayo Vallecano": "https://cdn.gomister.com/file/cdn-common/teams/14.png?version=20231117",
        "Barcelona": "https://cdn.gomister.com/file/cdn-common/teams/3.png?version=20231117",
        "Celta de Vigo": "https://cdn.gomister.com/file/cdn-common/teams/5.png?version=20231117",
        "Cádiz": "https://cdn.gomister.com/file/cdn-common/teams/499.png?version=20231117",
        "Alavés": "https://cdn.gomister.com/file/cdn-common/teams/48.png?version=20231117",
        "Almería": "https://cdn.gomister.com/file/cdn-common/teams/21.png?version=20231117",
        "Sevilla": "https://cdn.gomister.com/file/cdn-common/teams/17.png?version=20231117",
        "Betis": "https://cdn.gomister.com/file/cdn-common/teams/4.png?version=20231117",
        }

        self.progress = 0

        # Crear un diseño de cuadrícula
        layout = QGridLayout(self)
        # Establecer el tamaño máximo de la segunda columna
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)

        # Variables para almacenar la carpeta y la ruta seleccionadas
        self.selected_folder = ""
        self.selected_path = ""
        
        self.driver = None

        # TITULO VENTANA  ###########################################################################################
        # LABEL TÍTULO
        label_text = QLabel("Mister Fantasy Scraper")
        # Aplicar estilos para destacar el texto
        label_text.setStyleSheet("font-weight: bold; color: black; font-size: 20px;")
        layout.addWidget(label_text, 0, 0,1, 2)

        # LABEL SUBTÍTULO
        label_subtext = QLabel("Obtener el listado de todos los jugaodres disponibles en la web de Mister Fantasy MD y toda su informaciónm y estadísticas asociada.")
        layout.addWidget(label_subtext, 1, 0, 1, 2)


        ### SELECCIONAR JORNADA INPUT ####################################################
        # INPUT NÚMERO JORNADA 
        label_number = QLabel("Jornada a scrapear:")
        layout.addWidget(label_number, 2, 0)
        # Estilos 
        self.number_input = QSpinBox(self)
        self.number_input.setMinimum(11)  # Establecer el valor mínimo (jornada 1)
        self.number_input.setMaximum(38)  # Establecer el valor máximo (Jornada 36)
        self.number_input.setSingleStep(2)  # Establecer el paso
        self.number_input.setMaximumSize(38, 20)
        self.number_input.setMinimumSize(38, 20)
        # Aliniación
        layout.addWidget(self.number_input, 2, 1)
        

        #------- GAP vacio -----------------------------------------
        empty_widget = QWidget()
        empty_widget.setFixedHeight(10)  # Tamaño del gap (10 px)
        layout.addWidget(empty_widget, 3, 0)
        #-----------------------------------------------------------


        ###  SELECCIONAR RUTA DONDE GUARDAR EL EXCEL OUTPUT DEL SCRAPER  #################
        # LABEL TEXTO 
        label_text = QLabel("Ruta output scraper:")
        layout.addWidget(label_text, 4, 0)

        # INPUT TEXTO (QLineEdit en lugar de QSpinBox)
        self.text_input = QLineEdit(self)
        # Alineación
        layout.addWidget(self.text_input, 4, 1)
        # Estilos 
        self.text_input.setMinimumWidth(750)
        

        # BOTÓN PARA SELECCIONAR CARPETA
        select_folder_button = QPushButton("Seleccionar Carpeta")
        select_folder_button.clicked.connect(lambda: select_folder(self))
        # Alineación  
        layout.addWidget(select_folder_button, 5, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos 
        select_folder_button.setMinimumWidth(140)

        #------- GAP vacio -----------------------------------------
        empty_widget = QWidget()
        empty_widget.setFixedHeight(10)  # Tamaño del gap (10 px)
        layout.addWidget(empty_widget, 6, 0)
        #-----------------------------------------------------------


        ###  BOTÓN PARA INICIAR SCRAPER  ################################################
        # Crear un botón llamado "Scrapear"
        scrape_button = QPushButton("Scrapear")

        # Conectar la señal clicked del botón a la función iniciar_scrapear_thread e iniciar barra progreso
        scrape_button.clicked.connect(self.iniciar_scrapear_thread)
        scrape_button.clicked.connect(self.start_progress)

        # Alineación 
        layout.addWidget(scrape_button, 7, 0)
        # Estilos
        self.number_input.setMaximumSize(38, 20)


        ###  BARRA DE PROGRESO  ################################################
        # Crear Barra de progreso
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)


        ###  VENTANA OUTPUT SCRAPER  ####################################################
        # Crear un QTextEdit para la salida
        self.output_textedit = QTextEdit(self)
        layout.addWidget(self.output_textedit, 8, 0, 9, 0)  # row, column, rowSpan, columnSpan


        ###  ESTABLECER DISEÑO DE LA VENTANA  ###########################################
        self.setMinimumSize(500, 500) # Configurar el tamaño mínimo de la ventana
        # Configurar el diseño para la ventana
        self.setLayout(layout)

        # Configurar el título de la ventana
        self.setWindowTitle("Mister Fantasy Mundo Deportivo Scraper")

        # Evento cerrar ventana 
        self.destroyed.connect(self.cleanup)

    def cleanup(self):
        # Realizar cualquier limpieza necesaria aquí
        QApplication.quit()

    def start_progress(self):
        # Establecer el rango de la barra de progreso según tus necesidades
        self.progress_bar.setRange(0, 511)

        ruta_output = self.text_input.text()
        if ruta_output!="":
            self.progress_bar.setValue(0)
    
    def click_mas(self):
        # Pinchar en el botón del menu "Más"
        masMenu = self.driver.find_element(By.XPATH, '//*[@id="content"]/header/div[2]/ul/li[5]/a')

        try:
            masMenu.click()
        except (ElementNotInteractableException, NoSuchElementException):
            # Maneja la excepción y espera antes de intentar nuevamente
            print("Anuncio detectado, reiniciando driver...")
            self.driver.refresh()
            time.sleep(3) 
            masMenu.click()

    def actualizar_version(self,version):
      for equipo, url in self.teams_data.items():
        # Dividir la URL en base al signo de interrogación
        partes = url.split('?')
        
        # Verificar si hay una parte después del signo de interrogación y actualizar la versión
        if len(partes) > 1:
            partes[1] = f"version={version}"
            
            # Volver a unir las partes para formar la URL actualizada
            nueva_url = '?'.join(partes)
            
            # Actualizar la URL en el diccionario
            self.teams_data[equipo] = nueva_url

        #print(version)
        #print("nuevaaaa url-->  ",nueva_url)

    def obtener_valor_por_etiqueta(self,label_deseado):
        # Función para obtener el valor basado en la etiqueta
        elemento = self.driver.find_element(By.XPATH, f"//div[@class='item']//div[@class='label' and text()='{label_deseado}']/following-sibling::div[@class='value']")
        valor = elemento.text
        return valor

    def extraer_info_jugador(self,jornada_absolute,jornada_a_scrapear):
        
        nombre = self.driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div[1]/div/div[1]/div[2]")
        apellido = self.driver.find_element(By.XPATH, " /html/body/div[6]/div[3]/div[2]/div[1]/div/div[1]/div[3]")
        valorS= self.driver.find_element(By.XPATH,'/html/body/div[6]/div[3]/div[2]/div[2]/div/div/div[1]/div[2]')
        valor=valorS.text

        media_puntos_local = self.obtener_valor_por_etiqueta("Media en casa")
        media_puntos_visitante = self.obtener_valor_por_etiqueta("Media fuera")
        try:
            edad = self.obtener_valor_por_etiqueta("Edad")
            altura = self.obtener_valor_por_etiqueta("Altura")
            peso = self.obtener_valor_por_etiqueta("Peso")
        except:
            edad = None
            altura = None
            peso = None
                
        if peso == "kg":
            peso = None

            
        #### OBTENER EQUIPO JUGADOR ####

        # Obtener src del equipo
        team_logo_element = self.driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div[1]/div/div[1]/div[1]/a/img")
        image_url = team_logo_element.get_attribute("src")

        # Comparar la URL de la imagen con las URLs en teams_data
        equipo = None
        proximo_rival=None
        local= False
        for equipo_nombre, equipo_url in self.teams_data.items():
            if image_url == equipo_url:
                equipo = equipo_nombre
                
                #### OBTENER RESULTADO ÚLTIMO PARTIDO ####
                try:
                    divpartido = self.driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[3]/div[1]/div[3]/div")
                except:
                    divpartido = self.driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[3]/div/div[2]/div")
                
                # Encuentra el div del partido
                item_elements = divpartido.find_elements(By.CLASS_NAME, 'item')
            
                # Encuentra las imágenes dentro del div partido
                img_elements = item_elements[0].find_elements(By.CLASS_NAME, 'team-logo')

                # Guarda las src de las imágenes en variables
                if len(img_elements) >= 2:
                    src_img1 = img_elements[0].get_attribute('src')
                    src_img2 = img_elements[1].get_attribute('src')
                    if src_img1 == image_url:
                        local = True
                        for equipo_nombre, equipo_url in self.teams_data.items():
                            if src_img2 == equipo_url:
                                proximo_rival=equipo_nombre
                    else:
                        local=False
                        for equipo_nombre, equipo_url in self.teams_data.items():
                            if src_img1 == equipo_url:
                                proximo_rival=equipo_nombre
                else:
                    print("No se encontro el próximo partido")
                

        #### OBTENER POSICIÓN DEL JUGADOR ####
        elemento = self.driver.find_element(By.XPATH, '//i[contains(@class, "pos-")]')
        # Obtener el valor del atributo class
        clases = elemento.get_attribute("class").split()

        # Determinar la posición
        posicion = None
        for clase in clases:
            if clase.startswith("pos-") and "pos-big" in clases:
                if clase == "pos-1":
                    posicion = "PT"
                elif clase == "pos-2":
                    posicion = "DF"
                elif clase == "pos-3":
                    posicion = "MC"
                elif clase == "pos-4":
                    posicion = "DL"
                break

            
        #### OBTENER PUNTOS DEL JUGADOR ####
        # Encontrar jornada 
        elementos_principales = self.driver.find_elements(By.CLASS_NAME, 'btn-player-gw')

        # Iterar sobre cada elemento encontrado
        subelemento_gw=None
        jornada_name=None
        for elemento_principal in elementos_principales:
            # Encontrar subelemento con la clase 'gw' dentro de cada elemento principal
            subelemento_gw = elemento_principal.find_element(By.CLASS_NAME, 'gw')

            # Verificar si el texto coincide con el de la jornada
            if subelemento_gw.text == jornada_a_scrapear:
                jornada_name = subelemento_gw.text
                break             
        
        if jornada_name ==jornada_absolute:
            # Encontrar jornada en la web con otro elemennto como referencia
            localizador = self.driver.find_element(By.XPATH, "//h4[text()='Valor']")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", localizador)   
            
            time.sleep(1)
            
            try:
                subelemento_gw.click()
            except:
                elemento_principal.click()
            
            time.sleep(2)
            
            try:
                # PUNTOS MISTER FANTASY
                main_provider = self.driver.find_element(By.CLASS_NAME, 'main-provider')
                points_element = main_provider.find_element(By.CLASS_NAME, 'points')
                final_points = points_element.get_attribute('data-points')

                # PUNTOS AS, MARCA Y MUNDO DEPORTIVO 
                providers_div = self.driver.find_element(By.CLASS_NAME, "providers")
                li_elements = providers_div.find_elements(By.TAG_NAME, "li")

                points_array = []

                for li_element in li_elements:

                    points_div = li_element.find_element(By.CLASS_NAME, "points")
                    points_value = points_div.text
                    points_array.append(points_value)

                as_points=points_array[0]
                marca_points=points_array[1]
                mundo_deportivo_points=points_array[2]
                
                #### OBTENER PARTIDO ANTERIOR ####
                # Encontrar el div principal con la clase "player-match"
                player_match_div = self.driver.find_element(By.CLASS_NAME, "player-match")

                # Encontrar los subelementos dentro del div principal
                team_1 = player_match_div.find_element(By.CLASS_NAME, "left").find_element(By.CLASS_NAME, "team").text
                goals_team_1 = [int(goal.text) for goal in player_match_div.find_elements(By.CLASS_NAME, "goals")][0]  
                goals_team_2 = [int(goal.text) for goal in player_match_div.find_elements(By.CLASS_NAME, "goals")][1]  
                team_2 = player_match_div.find_element(By.CLASS_NAME, "right").find_element(By.CLASS_NAME, "team").text

                if team_1 == equipo:
                    ultimo_rival=team_2

                    if goals_team_1 > goals_team_2:
                        result = "Win"
                    elif goals_team_1 < goals_team_2:  
                        result = "Loss"
                    else:
                        result = "Draw"
                else:
                    ultimo_rival=team_1

                    if goals_team_1 > goals_team_2:
                        result = "Loss"
                    elif goals_team_1 < goals_team_2:  
                        result = "Win"
                    else:
                        result = "Draw"

                self.driver.back()
                
            except:
                final_points=None
                as_points=None
                marca_points=None
                mundo_deportivo_points=None
                ultimo_rival=None
                result=None
                
        else:
            final_points="NA"
            as_points="NA"
            marca_points="NA"
            mundo_deportivo_points="NA"
            ultimo_rival="NA"
            result="NA"
        

        #### IMPRIMIR TODOS LOS DATOS ####
        self.output_textedit.append("_____________________________________________")
        self.output_textedit.append(f"-{self.progress+1}. {nombre.text}, {apellido.text}")
        self.output_textedit.append(f"Valor: {valor}")
        self.output_textedit.append(f"Posición: {posicion}")
        self.output_textedit.append(f"Equipo: {equipo}")
            
        self.output_textedit.append("- - - - - - - - - - - - - - - - - - - - - - - - - -")

        self.output_textedit.append(f"Puntuación Fantasy: {final_points}")
        self.output_textedit.append(f"Puntuación Fantasy: {as_points}")
        self.output_textedit.append(f"Puntuación Marca: {marca_points}")
        self.output_textedit.append(f"Puntuación Mundo Deportivo: {mundo_deportivo_points}")
        
        self.output_textedit.append("- - - - - - - - - - - - - - - - - - - - - - - - - -")
            
        self.output_textedit.append(f"Último rival: {ultimo_rival}")
        self.output_textedit.append(f"Resultado del partido: {result}")

        self.output_textedit.append(f"Próximo rival: {proximo_rival}")
        self.output_textedit.append(f"Próximo partido es local: {local}")
        self.output_textedit.append(f"Media en casa: {media_puntos_local}")
        self.output_textedit.append(f"Media fuera: {media_puntos_visitante}")
        self.output_textedit.append(f"Edad: {edad}")
        self.output_textedit.append(f"Altura: {altura}")
        self.output_textedit.append(f"Peso: {peso}")

        self.progress += 1
        self.invocar_actualizacion(self.progress)

        #Definir ruta donde guardar el output del scraper
        ruta_output = self.text_input.text()
        save_as=f"{ruta_output}/"+jornada_absolute+".xlsx"
        self.output_textedit.append(save_as)
        jugador = nombre.text + " " + apellido.text

        try:
            wb = openpyxl.load_workbook(save_as)
        except FileNotFoundError:
            # Crear un nuevo libro de trabajo y una hoja
            wb = openpyxl.Workbook()
            sheet = wb.active
            encabezado = ["Jugador", "Valor", "Posición", "Equipo", "Puntuación Fantasy", "Puntuación AS", "Puntuación Marca", "Puntuación Mundo Deportivo", "Último rival", "Resultado del partido", "Próximo rival", "Próximo partido es local", "Media en casa", "Media fuera", "Edad", "Altura", "Peso"]
            sheet.append(encabezado)
            # Guardar el archivo Excel
            wb.save(save_as)

        # Seleccionar la hoja activa
        sheet = wb.active

        # Lista de variables a almacenar
        nueva_fila = [jugador, valor, posicion, equipo, final_points, as_points, marca_points, mundo_deportivo_points, ultimo_rival, result, proximo_rival, local, media_puntos_local, media_puntos_visitante, edad, altura, peso]

        # Escribir la nueva fila en la hoja de cálculo
        sheet.append(nueva_fila)

        # Guardar el archivo Excel
        wb.save(save_as)
        
    def iniciar_scrapear_thread(self):  
        # Crear un hilo y ejecutar la función en segundo plano
        thread = threading.Thread(target=self.scrapear_funcion)
        thread.start()

    def invocar_actualizacion(self, nuevo_valor):
        QMetaObject.invokeMethod(self.progress_bar, "setValue", Qt.ConnectionType.QueuedConnection, Q_ARG(int, nuevo_valor))

    def scrapear_funcion(self):
        self.output_textedit.append("Starting scraper...")

        # GESTIÓN DEL INPUT DEL USUARIO
        # Obtener el valor de la jornada desde el QSpinBox
        numero_jornada = str(self.number_input.value())

        # Concatena 'J' delante del número
        jornada_a_scrapear = 'J' + numero_jornada

        # Mostrar el valor en el QTextEdit
        self.output_textedit.append(f"Jornada seleccionada: {jornada_a_scrapear}")

        ruta_output = self.text_input.text()
        self.output_textedit.append(f"Ruta para la salida del scraper selecionada: {ruta_output}")
        self.output_textedit.append(f"________________________________________________________________________________________")

        if ruta_output=="":
            output_textedit = self.output_textedit
            color_rojo = QColor(255, 0, 0)  # Valores RGB para rojo
            formato_rojo = QTextCharFormat()
            formato_rojo.setForeground(color_rojo)
            output_textedit.mergeCurrentCharFormat(formato_rojo)
            output_textedit.insertPlainText("\n¡La jornada no está inicializada!, Configúrala antes de empezar a scrapear")
            formato_negro = QTextCharFormat()
            formato_negro.setForeground(QColor(0, 0, 0))
            output_textedit.mergeCurrentCharFormat(formato_negro)
            self.output_textedit.append(f"________________________________________________________________________________________")
            return
        
        rutaDel=f"{ruta_output}/"+jornada_a_scrapear+".xlsx"
        if os.path.exists(rutaDel):
             os.remove(rutaDel)

        self.driver = webdriver.Chrome()
        realizar_login(self.driver)
        time.sleep(5)

        # Espera a que se cargue la página
        self.driver.implicitly_wait(10)

        #Hacer click en el btn Jugadores con la función click_mas() para manejar errores generados por anuncios intrusivos
        self.click_mas()

        # Pinchar en el botón "Jugaodres" para acceder al listado de jugadores 
        jugadoresbtn = self.driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/button[2]')

        try:
            jugadoresbtn.click()
        except (ElementNotInteractableException, NoSuchElementException):
            # Maneja la excepción y espera antes de intentar nuevamente
            output_textedit = self.output_textedit
            color_rojo = QColor(255, 0, 0)  # Valores RGB para rojo
            formato_rojo = QTextCharFormat()
            formato_rojo.setForeground(color_rojo)
            output_textedit.mergeCurrentCharFormat(formato_rojo)
            output_textedit.insertPlainText("\nAnuncio detectado, reiniciando driver...")
            formato_negro = QTextCharFormat()
            formato_negro.setForeground(QColor(0, 0, 0))
            output_textedit.mergeCurrentCharFormat(formato_negro)
            self.driver.refresh()
            time.sleep(3)
            self.click_mas()
            time.sleep(3)
            try:
                jugadoresbtn = self.driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/button[2]')
                jugadoresbtn.click()
            except: 
                self.output_textedit.append("Reinicia el script :(")
                sys.exit()

        pag=2
        index=0
        absolute=1
        jornada_absolute=""
        while True:

            # Encontrar todos los elementos li
            elementos_lis = self.driver.find_elements(By.XPATH, "/html/body/div[6]/div[3]/div[3]/ul/li")

            # Longitud de la lista de elementos encontrados
            length=len(elementos_lis)

            while index < length:
                # Encontrar todos los elementos li
                elementos_li = self.driver.find_elements(By.XPATH, "/html/body/div[6]/div[3]/div[3]/ul/li")
                elementos_li[index].click()

                time.sleep(1)
                
                try:
                    team_logo_element = self.driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div[1]/div/div[1]/div[1]/a/img")
                except:
                    try:
                        team_logo_element = self.driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[3]/div/div[3]/div/div[1]/div[2]/img[1]")
                    except:
                        team_logo_element = self.driver.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[3]/div/div[3]/div/div[1]/div[2]/img[2]")
                
                image_url = team_logo_element.get_attribute("src")
                # Dividir la URL utilizando el signo de igual como delimitador
                parts = image_url.split('=')
                # El valor de version está en la segunda parte después del =
                version = parts[1]
                self.actualizar_version(version)
                
                if absolute == 1:
                    # Encontrar jornada 
                    elementos_principales = self.driver.find_elements(By.CLASS_NAME, 'btn-player-gw')

                    # Iterar sobre cada elemento encontrado
                    subelemento_gw=None
                    for elemento_principal in elementos_principales:
                        # Encontrar subelemento con la clase 'gw' dentro de cada elemento principal
                        subelemento_gw = elemento_principal.find_element(By.CLASS_NAME, 'gw')
                        
                        # Verificar si el texto coincide con el de la jornada
                        if subelemento_gw.text == jornada_a_scrapear:
                            jornada_absolute = subelemento_gw.text
                            break   
                absolute = 2
                
                self.extraer_info_jugador(jornada_absolute,jornada_a_scrapear)
                
                #Retroceder página
                self.driver.back()
                time.sleep(1)
                elementos_li = self.driver.find_elements(By.XPATH, "/html/body/div[6]/div[3]/div[3]/ul/li")
                if index == 0:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", elementos_li[index])
                else:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", elementos_li[index-1])
                time.sleep(1)
                index += 1

            #Pulsar Ver más
            try:
                ver_mas = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[3]/div[1]/button')
                ver_mas.click()
                time.sleep(4)
            except:
                break

            #Jugador cambio de pagina
            elementos_li = self.driver.find_elements(By.XPATH, "/html/body/div[6]/div[3]/div[3]/ul/li")
            elementos_li[index].click()
            time.sleep(2)
            self.extraer_info_jugador(jornada_absolute,jornada_a_scrapear)
            self.driver.back()
            
            self.output_textedit.append("____________________________________")
            self.output_textedit.append("------------------------------------")
            self.output_textedit.append(f"Siguiente página... ({pag})")
            self.output_textedit.append("------------------------------------")
            
            index=1
            pag+=1

        self.driver.quit()    
        self.output_textedit.append("Todos los jugadores scrapeados")


class trainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Crear un diseño principal usando QVBoxLayout
        layout = QVBoxLayout()

        # Crear un diseño de cuadrícula dentro del QVBoxLayout
        grid_layout = QGridLayout(self)

        # TITULO VENTANA  ###########################################################################################
        # LABEL TÍTULO
        label_text = QLabel("ENTRENAR MODELEO")
        # Aplicar estilos para destacar el texto
        label_text.setStyleSheet("font-weight: bold; color: black; font-size: 20px;")
        grid_layout.addWidget(label_text, 0, 0)

        # LABEL SUBTÍTULO 1
        label_subtext1 = QLabel("Pruba con los diferentes algoritmos disponibles a entrenar varios modelo y conparar entre ellos su desenpeño para selecionar el que mejores predicciones realice. ")
        grid_layout.addWidget(label_subtext1, 1, 0, 1, 2)

        ### SELECCIONAR RUTA DATASET DE ENTRADA ##################################################
        # LABEL DE TEXTO
        label_text = QLabel("Selecionar ruta de la carpeta de los datasets de entrada de cada jornada: ")
        grid_layout.addWidget(label_text, 2, 0, 1, 2)

        # INPUT DE TEXTO
        self.text_input = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input, 3, 0, 1, 2)

        # BOTÓN PARA SELECCIONAR ARCHIVO
        select_folder_button = QPushButton("Seleccionar carpeta")
        select_folder_button.clicked.connect(lambda: select_folder(self))
        # Alineación
        grid_layout.addWidget(select_folder_button, 4, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos
        select_folder_button.setMinimumWidth(140)

        ### SELECCIONAR ALGORITMO ##################################################
        # LABEL DE TEXTO
        label_text = QLabel("Seleciona un algoritmo de entrenamiento: ")
        grid_layout.addWidget(label_text, 5, 0)
        combo_box = QComboBox()
        combo_box.addItem("Gradient Boosted Tree model")
        combo_box.addItem("Random Forest model")
        combo_box.addItem("K-NN model")
        combo_box.addItem("Linear Regresion model")
        combo_box.addItem("Neural Net model")
        # Establecer el ancho máximo para la QComboBox
        combo_box.setMaximumWidth(185)
        grid_layout.addWidget(combo_box, 5, 1)


        label_choice = QLabel("Seleccionar atributo del jugador predecir:")
        grid_layout.addWidget(label_choice, 6, 0)

        combo_box = QComboBox()
        combo_box.addItem("Entrenar para predecir valor de mercado que alcanzará un jugaodr en la próxima jornada")
        combo_box.addItem("Entrenar para predecir puntos que obtendrá un jugaodr en la próxima jornada")
        
        # Establecer el ancho máximo para la QComboBox
        combo_box.setMaximumWidth(500)
        grid_layout.addWidget(combo_box, 6, 1)

        ### BOTÓN PARA EMPEZAR ENTRENAMIENTO ###########################################################
        # Crear un botón
        self.scrape_button = QPushButton("Iniciar entrenamiento")

        # Conectar la señal clicked del botón a la función iniciar_scrapear_thread e iniciar la barra de progreso
        self.scrape_button.clicked.connect(self.iniciar_thread)

        # Alineación y estilos
        grid_layout.addWidget(self.scrape_button, 7, 0)
        self.scrape_button.setMaximumWidth(150)

        ###  VENTANA OUTPUT SCRAPER  ####################################################################################
        # Crear un QTextEdit para la salida
        self.output_textedit = QTextEdit(self)
        grid_layout.addWidget(self.output_textedit, 8, 0, 2, 0)  # row, column, rowSpan, columnSpan

        ###  SELECCIONAR RUTA DONDE GUARDAR EL MODELO  ###################################
        # LABEL TEXTO 
        label_text = QLabel("Ruta donde guardar el modelo generado:")
        grid_layout.addWidget(label_text, 11, 0)

        # INPUT TEXTO (QLineEdit en lugar de QSpinBox)
        self.text_input2 = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input2, 11, 1)
        # Estilos 
        self.text_input2.setMinimumWidth(350)

        ###  SELECCIONAR NOMBRE MODELO  ###################################
        # LABEL TEXTO 
        label_text = QLabel("Nombre del modelo generado:")
        grid_layout.addWidget(label_text, 12, 0)

        # INPUT TEXTO (QLineEdit en lugar de QSpinBox)
        self.text_input2 = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input2, 12, 1)
        # Estilos 
        self.text_input2.setMinimumWidth(350)

        # BOTÓN PARA SELECCIONAR CARPETA
        select_folder_button = QPushButton("Seleccionar Carpeta")
        select_folder_button.clicked.connect(lambda: select_folder2(self))
        # Alineación
        grid_layout.addWidget(select_folder_button, 14, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos
        select_folder_button.setMinimumWidth(140)

        ### BOTÓN PARA GUARDAR MODLEO ###########################################################

        # Crear un botón
        self.scrape_button = QPushButton("Guardar modelo")

        # Conectar la señal clicked del botón a la función iniciar_scrapear_thread e iniciar la barra de progreso
        #self.scrape_button.clicked.connect(self.guardar_modeleo)

        # Alineación y estilos
        grid_layout.addWidget(self.scrape_button, 15, 1, alignment=Qt.AlignmentFlag.AlignRight)
        self.scrape_button.setMaximumWidth(150)

    def iniciar_thread(self):  
        # Crear un hilo y ejecutar la función en segundo plano
        thread = threading.Thread(target=self.train_function)
        thread.start()

    def train_function(self):
        # FASE 1: fusionar todos los dataset de entrada de cada jornada selecionados en uno solo #######################
        self.output_textedit.insertPlainText(f"Generand dataset de entrada...\n")
        carpeta_datasets = self.text_input.text()

        # Obtener la lista de archivos en la carpeta de entrada
        archivos_excel = [archivo for archivo in os.listdir(carpeta_datasets) if archivo.endswith('.xlsx')]

        # Comprobar si hay archivos Excel en la carpeta
        if not archivos_excel:
            self.output_textedit.insertPlainText("No hay archivos Excel (.xlsx) en la carpeta de entrada.\n")
        else:
            # Crear una lista para almacenar los DataFrames individuales
            lista_dataframes = []

            # Iterar sobre cada archivo Excel y almacenar los DataFrames en la lista
            for archivo in archivos_excel:
                ruta_archivo = os.path.join(carpeta_datasets, archivo)
                df = pd.read_excel(ruta_archivo)
                lista_dataframes.append(df)

            # Concatenar los DataFrames en uno solo
            df_combinado = pd.concat(lista_dataframes, ignore_index=True)
            
            # Guardar el DataFrame combinado en un nuevo archivo Excel
            archivo_salida = carpeta_datasets + "/dataset_training.xlsx"
            df_combinado.to_excel(archivo_salida, index=False)
            self.output_textedit.insertPlainText(f"Dataset de entrada fusionado exitosamente\n")

        # FASE 2: GEstión de MISSING VALUES ##########################################################################
        self.output_textedit.insertPlainText(f"Manejando Missing Values...\n")
        # Lee el archivo Excel
        df = pd.read_excel(archivo_salida)

        # Reemplaza los valores vacíos con 0
        df = df.fillna(0)
        df = df.replace('-', 0)

        # Reemplaza los valores iguales a 0 con un string en una columna específica
        columna = 'Ausencia'
        string_reemplazo = 'None'
        df[columna] = df[columna].apply(lambda x: string_reemplazo if x == 0 else x)

        # Guarda el DataFrame modificado en un nuevo archivo Excel
        archivo_salida = carpeta_datasets + "/dataset_training_without_missing_values.xlsx"
        df.to_excel(archivo_salida, index=False)

        self.output_textedit.insertPlainText(f"Gestión de Missing Values completada exitosamente\n")
        
    def guardar_modeleo(self):
        self.output_textedit.insertPlainText("future guardar modelo\n")

class predictWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Crear un diseño principal usando QVBoxLayout
        layout = QVBoxLayout()

        # Crear un diseño de cuadrícula dentro del QVBoxLayout
        grid_layout = QGridLayout(self)

        # TITULO VENTANA  ###########################################################################################
        # LABEL TÍTULO
        label_text = QLabel("PREDECIR")
        # Aplicar estilos para destacar el texto
        label_text.setStyleSheet("font-weight: bold; color: black; font-size: 20px;")
        grid_layout.addWidget(label_text, 0, 0)

        # LABEL SUBTÍTULO 1
        label_subtext1 = QLabel("predecir el valor de mercado o los puntos que obtendrá el jugaodr en la sigueinte jornada de la liga mediante el modelo generado en el entrenamiento. ")
        grid_layout.addWidget(label_subtext1, 1, 0, 1, 2)

        ### SELECCIONAR RUTA DATASET DE ENTRADA ##################################################
        # LABEL DE TEXTO
        label_text = QLabel("Selecionar ruta de los futbolitas a predecir su puntuación: ")
        grid_layout.addWidget(label_text, 2, 0)

        # INPUT DE TEXTO
        self.text_file_input = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_file_input, 2, 1)

        # BOTÓN PARA SELECCIONAR ARCHIVO
        select_file_button = QPushButton("Seleccionar Archivo")
        select_file_button.clicked.connect(lambda: select_file(self))

        # Alineación
        grid_layout.addWidget(select_file_button, 3, 1, alignment=Qt.AlignmentFlag.AlignRight)

        # Estilos
        select_file_button.setMinimumWidth(140)


        ### SELECCIONAR RUTA MODELO A USAR #################################################################
        # LABEL DE TEXTO
        label_text = QLabel("Selecionar ruta del modelo que se desea utilzar para predecir: ")
        grid_layout.addWidget(label_text, 4, 0)

        # INPUT DE TEXTO
        self.text_file2_input = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_file2_input, 4, 1)

        # BOTÓN PARA SELECCIONAR ARCHIVO
        select_file_button = QPushButton("Seleccionar Archivo")
        select_file_button.clicked.connect(lambda: select_file2(self))
        # Alineación
        grid_layout.addWidget(select_file_button, 5, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos
        select_file_button.setMinimumWidth(140)

        ### BOTÓN PARA EMPEZAR ENTRENAMIENTO ###########################################################
        # LABEL DE TEXTO
        label_text = QLabel("Predecir valores")
        grid_layout.addWidget(label_text, 6, 0)

        # Crear un botón
        self.scrape_button = QPushButton("Predecir puntuación")

        # Conectar la señal clicked del botón a la función iniciar_scrapear_thread e iniciar la barra de progreso
        #self.scrape_button.clicked.connect(self.iniciar_scrapear_thread)

        # Alineación y estilos
        grid_layout.addWidget(self.scrape_button, 6, 1)
        self.scrape_button.setMaximumWidth(150)

        ###  SELECCIONAR RUTA DONDE GUARDAR EL EXCEL OUTPUT DEL SCRAPER  ###################################
        # LABEL TEXTO 
        label_text = QLabel("Ruta output donde guardar estadisticas del modelo:")
        grid_layout.addWidget(label_text, 7, 0)

        # INPUT TEXTO (QLineEdit en lugar de QSpinBox)
        self.text_input = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input, 7, 1)
        # Estilos 
        #self.text_input.setMinimumWidth(350)

        # BOTÓN PARA SELECCIONAR CARPETA
        select_folder_button = QPushButton("Seleccionar Carpeta")
        select_folder_button.clicked.connect(lambda: select_folder(self))
        # Alineación
        grid_layout.addWidget(select_folder_button, 8, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos
        select_folder_button.setMinimumWidth(140)


class login(QWidget):
    def __init__(self):
        super().__init__()
        # Crear un diseño principal usando QVBoxLayout
        layout = QVBoxLayout()

        # Crear un diseño de cuadrícula dentro del QVBoxLayout
        grid_layout = QGridLayout(self)

        # TITULO VENTANA  ###########################################################################################
        # LABEL TÍTULO
        label_text = QLabel("MI PERFIL")
        # Aplicar estilos para destacar el texto
        label_text.setStyleSheet("font-weight: bold; color: black; font-size: 20px;")
        grid_layout.addWidget(label_text, 0, 0)

        # LABEL SUBTÍTULO 1
        label_subtext1 = QLabel("Danos acceso a tu cuenta de Mister Fantasy MD logueandote en el siguiente formulario para permitir a la aplicación obtener informacion de los jugadores de la liga. ")
        grid_layout.addWidget(label_subtext1, 1, 0, 1, 2)

        # LABEL SUBTÍTULO 2
        label_subtext2 = QLabel("* Tus credenciales nunca serán guardadas y se eliminaran autoamticamente al cerrar la aplicación. *")
        # Aplicar estilos para destacar el texto
        label_subtext2.setStyleSheet("color: red;")
        grid_layout.addWidget(label_subtext2, 2, 0, 1, 2)

        # INPUT CREDENCIALES  #########################################################################################
        # LABEL DE TEXTO
        label_text2 = QLabel("Usuario: ")
        grid_layout.addWidget(label_text2, 3, 0, alignment=Qt.AlignmentFlag.AlignTop)

        # INPUT DE TEXTO
        self.text_input1 = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input1, 3, 1)

        ### SELECCIONAR PSW ##################################################
        # LABEL DE TEXTO
        label_text = QLabel("Contraseña: ")
        grid_layout.addWidget(label_text, 4, 0)

        # INPUT DE TEXTO
        self.text_input2 = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input2, 4, 1)

        ### BOTÓN PARA EJECUTAR FUNCIÓN PARA FUSIONAR EXCELLS ###########################################################
        # Crear un botón
        self.save_button = QPushButton("Guardar credenciales")

        # Conectar la señal clicked del botón a la función iniciar_scrapear_thread e iniciar la barra de progreso
        self.save_button.clicked.connect(self.iniciar_scrapear_thread)

        # Alineación
        grid_layout.addWidget(self.save_button, 5, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos
        self.save_button.setMinimumWidth(100)
        self.save_button.setMaximumWidth(150)

        ###  VENTANA OUTPUT SCRAPER  ####################################################################################
        # Crear un QTextEdit para la salida
        self.output_textedit = QTextEdit(self)
        grid_layout.addWidget(self.output_textedit, 6, 0, 11, 0)  # row, column, rowSpan, columnSpan

    def iniciar_scrapear_thread(self):  
        # Crear un hilo y ejecutar la función en segundo plano
        thread = threading.Thread(target=self.guardar_credenciales)
        thread.start()

    def guardar_credenciales(self):
        self.output_textedit.insertPlainText('________________________________________________________________________________________\n')
        self.output_textedit.insertPlainText('Comprobando credenciales introducidas...\n')

        usuario_input = self.text_input1.text()
        contrasena_input = self.text_input2.text()

        if usuario_input!="" and contrasena_input!="":
            
            self.driver = webdriver.Chrome()

            # Navega a la página web que deseas hacer scraping
            self.driver.get("https://mister.mundodeportivo.com/new-onboarding/#market")

            # Espera a que se cargue la página
            self.driver.implicitly_wait(15)

            # Encuentra el botón de "Consentir" 
            button = self.driver.find_element(By.XPATH, '//*[@id="didomi-notice-agree-button"]')
            # Haz clic en el botón de "Consentir" 
            button.click()

            # Encuentra el botón de "Siguinete" 
            button = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/button')
            # Haz clic en el botón de "Siguiente" 
            button.click()
            button.click()
            button.click()
            button.click()

            # Encuentra el botón de "sing con gmail" 
            button = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/button[3]')
            button.click()

            # Localiza el elemento del input gmail
            inputgmail = self.driver.find_element(By.XPATH, '//*[@id="email"]')

            # Borra cualquier contenido existente en la caja de texto (opcional)
            inputgmail.clear()

            # Ingresa texto en la caja de texto
            inputgmail.send_keys(usuario_input)

            # Localiza el elemento del input gmail
            inputpsw = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[2]/input')

            # Borra cualquier contenido existente en la caja de texto (opcional)
            inputpsw.clear()

            # Ingresa texto en la caja de texto
            inputpsw.send_keys(contrasena_input)

            # Encuentra el botón de "sing con gmail" 
            button = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[3]/button')
            button.click()
            try:
                # Encuentra el botón para comprobar si se ha conseguido loguear en la web de Mister Fantasy
                button = self.driver.find_element(By.XPATH, '//*[@id="content"]/header/div[2]/ul/li[2]/a')
                
                # Haz clic en el botón
                button.click()

                self.driver.quit()

                self.output_textedit.insertPlainText('Usuario o contraseña correctos.\n')

                # Acceder a las variables globales desde la clase
                global usuario, contrasena
                usuario = usuario_input
                contrasena = contrasena_input

                return
            
            except NoSuchElementException:
                self.driver.quit()
                output_textedit = self.output_textedit
                color_rojo = QColor(255, 0, 0)  # Valores RGB para rojo
                formato_rojo = QTextCharFormat()
                formato_rojo.setForeground(color_rojo)
                output_textedit.mergeCurrentCharFormat(formato_rojo)
                output_textedit.insertPlainText('Usuario o contraseña incorrectos.\n')
                formato_negro = QTextCharFormat()
                formato_negro.setForeground(QColor(0, 0, 0))
                output_textedit.mergeCurrentCharFormat(formato_negro)
                return
        else:
            output_textedit = self.output_textedit
            color_rojo = QColor(255, 0, 0)  # Valores RGB para rojo
            formato_rojo = QTextCharFormat()
            formato_rojo.setForeground(color_rojo)
            output_textedit.mergeCurrentCharFormat(formato_rojo)
            output_textedit.insertPlainText("Credenciales no inicializadas.\n")
            formato_negro = QTextCharFormat()
            formato_negro.setForeground(QColor(0, 0, 0))
            output_textedit.mergeCurrentCharFormat(formato_negro)
            

def main():
    app = QApplication(sys.argv)
    ventana_principal = VentanaPrincipal()
    ventana_principal.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()