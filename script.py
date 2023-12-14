# Dependencias
from PyQt6.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QLineEdit, QSpinBox, QPushButton, QFileDialog, QWidget, QTextEdit, QProgressBar, QVBoxLayout, QTextEdit, QMainWindow, QStackedWidget, QHBoxLayout
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

#Credenciales ususario
usuario=None
contrasena=None

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
        self.ventana3 = PlayerScraperWindowMF("Players Scraper")
        self.ventana4 = PlayerScraperWindowSC()
        self.ventana5 = dataset_creator()
        self.ventana6 = trainWindow()
        self.ventana7 = predictWindowPoints()
        self.ventana8 = predictWindowPrice()
        self.ventana9 = login()

        self.stacked_widget.addWidget(self.ventana1)
        self.stacked_widget.addWidget(self.ventana2)
        self.stacked_widget.addWidget(self.ventana3)
        self.stacked_widget.addWidget(self.ventana4)
        self.stacked_widget.addWidget(self.ventana5)
        self.stacked_widget.addWidget(self.ventana6)
        self.stacked_widget.addWidget(self.ventana7)
        self.stacked_widget.addWidget(self.ventana8)
        self.stacked_widget.addWidget(self.ventana9)

        self.btn_ventana1 = QPushButton("Mi plantilla")
        self.btn_ventana1.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        self.btn_ventana2 = QPushButton("Mercado")
        self.btn_ventana2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        self.btn_ventana3 = QPushButton("Scraper jugadores MF")
        self.btn_ventana3.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

        self.btn_ventana4 = QPushButton("Scraper jugadores SF")
        self.btn_ventana4.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))

        self.btn_ventana5 = QPushButton("Crear dataset")
        self.btn_ventana5.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))

        self.btn_ventana6 = QPushButton("Entrenar modelo")
        self.btn_ventana6.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))

        self.btn_ventana7 = QPushButton("Predecir Puntuación")
        self.btn_ventana7.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(6))

        self.btn_ventana8 = QPushButton("Predecir Valor")
        self.btn_ventana8.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(7))

        self.btn_ventana9 = QPushButton("Mi perfil")
        self.btn_ventana9.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(8))

        self.layout.addWidget(self.btn_ventana1, 0, 0)
        self.layout.addWidget(self.btn_ventana2, 0, 1)
        self.layout.addWidget(self.btn_ventana3, 0, 2)
        self.layout.addWidget(self.btn_ventana4, 0, 3)
        self.layout.addWidget(self.btn_ventana5, 0, 4)
        self.layout.addWidget(self.btn_ventana6, 0, 5)
        self.layout.addWidget(self.btn_ventana7, 0, 6)
        self.layout.addWidget(self.btn_ventana8, 0, 7)
        self.layout.addWidget(self.btn_ventana9, 0, 8)

        self.layout.addWidget(self.stacked_widget, 1, 0, 1, 9)


class squadWindow(QWidget):
    def __init__(self):
        super().__init__()

        #Varaible para guardar la plantilla scrapeada
        self.nombres_jugadores=[]

        # Crear un diseño principal usando QVBoxLayout
        layout = QVBoxLayout()

        # Crear un diseño de cuadrícula dentro del QVBoxLayout
        grid_layout = QGridLayout(self)

        # BOTÓN PARA INICIAR LA OBTENCIÓN DE MI PLANTILLA ###########################################################
        # LABEL DE TEXTO
        label_text = QLabel("Obtener mi plantilla")
        grid_layout.addWidget(label_text, 1, 0)

        # Crear un botón
        self.scrape_button = QPushButton("Scrapear mi plantilla")

        # Conectar la señal clicked del botón a la función iniciar_scrapear_thread e iniciar la barra de progreso
        self.scrape_button.clicked.connect(self.iniciar_scrapear_thread)

        # Alineación y estilos
        grid_layout.addWidget(self.scrape_button, 1, 1)
        self.scrape_button.setMaximumWidth(150)

        # VENTANA OUTPUT SCRAPER #####################################################################################
        # Crear un QTextEdit para la salida
        self.output_textedit = QTextEdit(self)
        grid_layout.addWidget(self.output_textedit, 2, 0, 2, 2)  # row, column, rowSpan, columnSpan

        # SELECCIONAR RUTA DONDE GUARDAR EL EXCEL OUTPUT DEL SCRAPER ##################################################
        # LABEL DE TEXTO
        label_text = QLabel("Guardar plantilla:")
        grid_layout.addWidget(label_text, 4, 0)

        # INPUT DE TEXTO
        self.text_input = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input, 4, 1)

        # BOTÓN PARA SELECCIONAR CARPETA
        select_folder_button = QPushButton("Seleccionar Carpeta")
        select_folder_button.clicked.connect(self.select_folder)
        # Alineación
        grid_layout.addWidget(select_folder_button, 5, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos
        select_folder_button.setMinimumWidth(140)

        # BOTÓN PARA GUARDAR MI PLANTILLA ###########################################################################
        # Crear un botón
        self.save_button = QPushButton("Guardar plantilla")

        # Conectar la señal clicked del botón a la función iniciar_scrapear_thread e iniciar la barra de progreso
        self.save_button.clicked.connect(self.guardar_excell)

        # Alineación
        grid_layout.addWidget(self.save_button, 6, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos
        self.save_button.setMinimumWidth(100)
        self.save_button.setMaximumWidth(150)


        # Agregar el diseño de cuadrícula al diseño principal
        layout.addLayout(grid_layout)

        # Agregar el diseño principal al widget
        self.setLayout(layout)

    def select_folder(self):
        # Obtener el directorio del script de Python
        script_directory = os.path.dirname(__file__)
        
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta", script_directory)
        if folder_path:
            # Actualizar las variables de clase con la carpeta y la ruta seleccionadas
            self.selected_folder = folder_path
            self.selected_path = folder_path

            # Actualizar el QLineEdit con la ruta seleccionada
            self.text_input.setText(self.selected_path)

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
       
        try:

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
            inputgmail.send_keys("m31_grupo6@outlook.com")

            # Localiza el elemento del input gmail
            inputpsw = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[2]/input')

            # Borra cualquier contenido existente en la caja de texto (opcional)
            inputpsw.clear()

            # Ingresa texto en la caja de texto
            inputpsw.send_keys("Chocoflakes2")

            # Encuentra el botón de "sing con gmail" 
            button = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[3]/button')
            button.click()

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

        # LABEL DE TEXTO
        label_text = QLabel("Obtener jugadores en el mercado")
        grid_layout.addWidget(label_text, 1, 0)

        # BOTÓN PARA INICIAR LA OBTENCIÓN DE MI PLANTILLA ###########################################################
        # Crear un botón
        self.scrape_button = QPushButton("Scrapear mercado")

        # Conectar la señal clicked del botón a la función iniciar_scrapear_thread e iniciar la barra de progreso
        self.scrape_button.clicked.connect(self.iniciar_scrapear_thread)

        # Alineación y estilos
        grid_layout.addWidget(self.scrape_button, 1, 1)
        self.scrape_button.setMaximumWidth(150)

        # VENTANA OUTPUT SCRAPER #####################################################################################
        # Crear un QTextEdit para la salida
        self.output_textedit = QTextEdit(self)
        grid_layout.addWidget(self.output_textedit, 2, 0, 2, 2)  # row, column, rowSpan, columnSpan

        # SELECCIONAR RUTA DONDE GUARDAR EL EXCEL OUTPUT DEL SCRAPER ##################################################
        # LABEL DE TEXTO
        label_text = QLabel("Guardar jugadores en mi plantilla:")
        grid_layout.addWidget(label_text, 4, 0)

        # INPUT DE TEXTO
        self.text_input = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input, 4, 1)

        # BOTÓN PARA SELECCIONAR CARPETA
        select_folder_button = QPushButton("Seleccionar Carpeta")
        select_folder_button.clicked.connect(self.select_folder)
        # Alineación
        grid_layout.addWidget(select_folder_button, 5, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos
        select_folder_button.setMinimumWidth(140)

        # BOTÓN PARA GUARDAR MI PLANTILLA ###########################################################################
        # Crear un botón
        self.save_button = QPushButton("Guardar plantilla")

        # Conectar la señal clicked del botón a la función iniciar_scrapear_thread e iniciar la barra de progreso
        self.save_button.clicked.connect(self.guardar_excell)

        # Alineación
        grid_layout.addWidget(self.save_button, 6, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos
        self.save_button.setMinimumWidth(100)
        self.save_button.setMaximumWidth(150)


        # Agregar el diseño de cuadrícula al diseño principal
        layout.addLayout(grid_layout)

        # Agregar el diseño principal al widget
        self.setLayout(layout)

    def select_folder(self):
        # Obtener el directorio del script de Python
        script_directory = os.path.dirname(__file__)
        
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta", script_directory)
        if folder_path:
            # Actualizar las variables de clase con la carpeta y la ruta seleccionadas
            self.selected_folder = folder_path
            self.selected_path = folder_path

            # Actualizar el QLineEdit con la ruta seleccionada
            self.text_input.setText(self.selected_path)

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
       
        try:

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
            inputgmail.send_keys("m31_grupo6@outlook.com")

            # Localiza el elemento del input gmail
            inputpsw = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[2]/input')

            # Borra cualquier contenido existente en la caja de texto (opcional)
            inputpsw.clear()

            # Ingresa texto en la caja de texto
            inputpsw.send_keys("Chocoflakes2")

            # Encuentra el botón de "sing con gmail" 
            button = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[3]/button')
            button.click()

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


class dataset_creator(QWidget):
    def __init__(self):
        super().__init__()
        # Crear un diseño principal usando QVBoxLayout
        layout = QVBoxLayout()

        # Crear un diseño de cuadrícula dentro del QVBoxLayout
        grid_layout = QGridLayout(self)

        ### SELECCIONAR RUTA DATASET DE ENTRADA SOFAESCORE ##################################################
        # LABEL DE TEXTO
        label_text = QLabel("Selecionar ruta del datset de entrada de Sofaescore: ")
        grid_layout.addWidget(label_text, 1, 0)

        # INPUT DE TEXTO
        self.text_input1 = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input1, 1, 1)

        # BOTÓN PARA SELECCIONAR CARPETA
        select_folder_button = QPushButton("Seleccionar Carpeta")
        select_folder_button.clicked.connect(self.select_folder)
        # Alineación
        grid_layout.addWidget(select_folder_button, 2, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos
        select_folder_button.setMinimumWidth(140)

        ### SELECCIONAR RUTA DATASET DE ENTRADA MISTER FANTASY ##################################################
        # LABEL DE TEXTO
        label_text = QLabel("Selecionar carperta de la jornada de todos los partidos de Sofaescore scrapeados: ")
        grid_layout.addWidget(label_text, 3, 0)

        # INPUT DE TEXTO
        self.text_input2 = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input2, 3, 1)

        # BOTÓN PARA SELECCIONAR ARCHIVO
        select_file_button = QPushButton("Seleccionar archivo de la jornada de Misterfantasy srapeado: ")
        #select_file_button.clicked.connect(self.select_file)

        # Alineación
        grid_layout.addWidget(select_file_button, 4, 1, alignment=Qt.AlignmentFlag.AlignRight)

        # Estilos
        select_file_button.setMinimumWidth(140)

        ### BOTÓN PARA EJECUTAR FUNCIÓN PARA FUSIONAR EXCELLS ###########################################################
        # LABEL DE TEXTO
        label_text = QLabel("Obtener dataset de entrenamiento")
        grid_layout.addWidget(label_text, 5, 0)

        # Crear un botón
        self.save_button = QPushButton("Generar dataset")

        # Conectar la señal clicked del botón a la función iniciar_scrapear_thread e iniciar la barra de progreso
        self.save_button.clicked.connect(self.json_a_excel)

        # Alineación
        grid_layout.addWidget(self.save_button, 5, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos
        self.save_button.setMinimumWidth(100)
        self.save_button.setMaximumWidth(150)

        # VENTANA OUTPUT SCRAPER #####################################################################################
        # Crear un QTextEdit para la salida
        self.output_textedit = QTextEdit(self)
        grid_layout.addWidget(self.output_textedit,6, 0, 2, 2)  # row, column, rowSpan, columnSpan
    
    def select_folder(self):
        # Obtener el directorio del script de Python
        script_directory = os.path.dirname(__file__)
        
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta", script_directory)
        if folder_path:
            # Actualizar las variables de clase con la carpeta y la ruta seleccionadas
            self.selected_folder = folder_path
            self.selected_path = folder_path

            # Actualizar el QLineEdit con la ruta seleccionada
            self.text_input1.setText(self.selected_path)


    def json_a_excel(self):
        
        # Rutas globales
        carpeta_json = self.text_input1.text()
        carpeta_xlsx = self.text_input1.text()
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

        self.output_textedit.insertPlainText(f"Archivo Excel guardado en: {ruta_excel}")


class login(QWidget):
    def __init__(self):
        super().__init__()
        # Crear un diseño principal usando QVBoxLayout
        layout = QVBoxLayout()

        # Crear un diseño de cuadrícula dentro del QVBoxLayout
        grid_layout = QGridLayout(self)

        # LABEL DE TEXTO
        #label_text1 = QLabel("Introduce tu cuenta de Mister Fantasy Mundo Deportivo para conectarla con la aplicación: ")
        #grid_layout.addWidget(label_text1, 1, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)

        # LABEL DE TEXTO
        label_text2 = QLabel("Usuario: ")
        grid_layout.addWidget(label_text2, 2, 0, alignment=Qt.AlignmentFlag.AlignTop)

        # INPUT DE TEXTO
        self.text_input1 = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input1, 2, 1)

        ### SELECCIONAR PSW ##################################################
        # LABEL DE TEXTO
        label_text = QLabel("Contraseña: ")
        grid_layout.addWidget(label_text, 3, 0)

        # INPUT DE TEXTO
        self.text_input2 = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input2, 3, 1)

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
        grid_layout.addWidget(self.output_textedit, 6, 0, 2, 0)  # row, column, rowSpan, columnSpan

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
            

class trainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Crear un diseño principal usando QVBoxLayout
        layout = QVBoxLayout()

        # Crear un diseño de cuadrícula dentro del QVBoxLayout
        grid_layout = QGridLayout(self)

        ### SELECCIONAR RUTA DATASET DE ENTRADA ##################################################
        # LABEL DE TEXTO
        label_text = QLabel("Selecionar dataset de entrada: ")
        grid_layout.addWidget(label_text, 1, 0)

        # INPUT DE TEXTO
        self.text_input = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input, 1, 1)

        # BOTÓN PARA SELECCIONAR ARCHIVO
        select_file_button = QPushButton("Seleccionar Archivo")
        select_file_button.clicked.connect(self.select_file)
        # Alineación
        grid_layout.addWidget(select_file_button, 2, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos
        select_file_button.setMinimumWidth(140)

        ### SELECCIONAR ALGORITMO ##################################################
        # LABEL DE TEXTO
        label_text = QLabel("Selecionar algoritmo de entrenamiento: ")
        grid_layout.addWidget(label_text, 3, 0)

        ### BOTÓN PARA EMPEZAR ENTRENAMIENTO ###########################################################
        # LABEL DE TEXTO
        label_text = QLabel("Entrenar modeleo")
        grid_layout.addWidget(label_text, 4, 0)

        # Crear un botón
        self.scrape_button = QPushButton("Iniciar entrenamiento")

        # Conectar la señal clicked del botón a la función iniciar_scrapear_thread e iniciar la barra de progreso
        #self.scrape_button.clicked.connect(self.iniciar_scrapear_thread)

        # Alineación y estilos
        grid_layout.addWidget(self.scrape_button, 4, 1)
        self.scrape_button.setMaximumWidth(150)


        ### DEFINIR NOMBRE DEL MODELO ##################################################
        # LABEL DE TEXTO
        label_text = QLabel("Nombre del modelo: ")
        grid_layout.addWidget(label_text, 5, 0)

        # INPUT DE TEXTO
        self.text_input = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input, 5, 1)


        ###  SELECCIONAR RUTA DONDE GUARDAR EL MODELO  ###################################
        # LABEL TEXTO 
        label_text = QLabel("Ruta donde guardar el modelo:")
        grid_layout.addWidget(label_text, 6, 0)

        # INPUT TEXTO (QLineEdit en lugar de QSpinBox)
        text_input = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(text_input, 6, 1)
        # Estilos 
        self.text_input.setMinimumWidth(350)

        # BOTÓN PARA SELECCIONAR CARPETA
        select_folder_button = QPushButton("Seleccionar Carpeta")
        select_folder_button.clicked.connect(self.select_folder)
        # Alineación
        grid_layout.addWidget(select_folder_button, 7, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos
        select_folder_button.setMinimumWidth(140)

        ### BOTÓN PARA GUARDAR MODLEO ###########################################################

        # Crear un botón
        self.scrape_button = QPushButton("Guardar modelo")

        # Conectar la señal clicked del botón a la función iniciar_scrapear_thread e iniciar la barra de progreso
        #self.scrape_button.clicked.connect(self.iniciar_scrapear_thread)

        # Alineación y estilos
        grid_layout.addWidget(self.scrape_button, 8, 1, alignment=Qt.AlignmentFlag.AlignRight)
        self.scrape_button.setMaximumWidth(150)

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
            self.text_input.setText(self.selected_path)

    def select_folder(self):
        # Obtener el directorio del script de Python
        script_directory = os.path.dirname(__file__)
        
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta", script_directory)
        if folder_path:
            # Actualizar las variables de clase con la carpeta y la ruta seleccionadas
            self.selected_folder = folder_path
            self.selected_path = folder_path

            # Actualizar el QLineEdit con la ruta seleccionada
            self.text_input.setText(self.selected_path)


class predictWindowPoints(QWidget):
    def __init__(self):
        super().__init__()

        # Crear un diseño principal usando QVBoxLayout
        layout = QVBoxLayout()

        # Crear un diseño de cuadrícula dentro del QVBoxLayout
        grid_layout = QGridLayout(self)

        ### SELECCIONAR RUTA DATASET DE ENTRADA ##################################################
        # LABEL DE TEXTO
        label_text = QLabel("Selecionar ruta de los futbolitas a predecir su puntuación: ")
        grid_layout.addWidget(label_text, 1, 0)

        # INPUT DE TEXTO
        self.text_input = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input, 1, 1)

        # BOTÓN PARA SELECCIONAR ARCHIVO
        select_file_button = QPushButton("Seleccionar Archivo")
        select_file_button.clicked.connect(self.select_file)

        # Alineación
        grid_layout.addWidget(select_file_button, 2, 1, alignment=Qt.AlignmentFlag.AlignRight)

        # Estilos
        select_file_button.setMinimumWidth(140)


        ### SELECCIONAR RUTA MODELO A USAR #################################################################
        # LABEL DE TEXTO
        label_text = QLabel("Selecionar ruta del modelo que se desea utilzar para predecir: ")
        grid_layout.addWidget(label_text, 3, 0)

        # INPUT DE TEXTO
        self.text_input = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input, 3, 1)

        # BOTÓN PARA SELECCIONAR ARCHIVO
        select_file_button = QPushButton("Seleccionar Archivo")
        select_file_button.clicked.connect(self.select_file)
        # Alineación
        grid_layout.addWidget(select_file_button, 4, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos
        select_file_button.setMinimumWidth(140)

        ### BOTÓN PARA EMPEZAR ENTRENAMIENTO ###########################################################
        # LABEL DE TEXTO
        label_text = QLabel("Predecir valores")
        grid_layout.addWidget(label_text, 5, 0)

        # Crear un botón
        self.scrape_button = QPushButton("Predecir puntuación")

        # Conectar la señal clicked del botón a la función iniciar_scrapear_thread e iniciar la barra de progreso
        #self.scrape_button.clicked.connect(self.iniciar_scrapear_thread)

        # Alineación y estilos
        grid_layout.addWidget(self.scrape_button, 5, 1)
        self.scrape_button.setMaximumWidth(150)

        ###  SELECCIONAR RUTA DONDE GUARDAR EL EXCEL OUTPUT DEL SCRAPER  ###################################
        # LABEL TEXTO 
        label_text = QLabel("Ruta output donde guardar estadisticas del modelo:")
        grid_layout.addWidget(label_text, 6, 0)

        # INPUT TEXTO (QLineEdit en lugar de QSpinBox)
        text_input = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(text_input, 6, 1)
        # Estilos 
        self.text_input.setMinimumWidth(350)

        # BOTÓN PARA SELECCIONAR CARPETA
        select_folder_button = QPushButton("Seleccionar Carpeta")
        select_folder_button.clicked.connect(self.select_folder)
        # Alineación
        grid_layout.addWidget(select_folder_button, 7, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos
        select_folder_button.setMinimumWidth(140)

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
            self.text_input.setText(self.selected_path)

    def select_folder(self):
        # Obtener el directorio del script de Python
        script_directory = os.path.dirname(__file__)
        
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta", script_directory)
        if folder_path:
            # Actualizar las variables de clase con la carpeta y la ruta seleccionadas
            self.selected_folder = folder_path
            self.selected_path = folder_path

            # Actualizar el QLineEdit con la ruta seleccionada
            self.text_input.setText(self.selected_path)


class predictWindowPrice(QWidget):
    def __init__(self):
        super().__init__()

        # Crear un diseño principal usando QVBoxLayout
        layout = QVBoxLayout()

        # Crear un diseño de cuadrícula dentro del QVBoxLayout
        grid_layout = QGridLayout(self)

        ### SELECCIONAR RUTA DATASET DE ENTRADA ##################################################
        # LABEL DE TEXTO
        label_text = QLabel("Selecionar ruta de los futbolitas a predecir el valor: ")
        grid_layout.addWidget(label_text, 1, 0)

        # INPUT DE TEXTO
        self.text_input = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input, 1, 1)

        # BOTÓN PARA SELECCIONAR ARCHIVO
        select_file_button = QPushButton("Seleccionar Archivo")
        select_file_button.clicked.connect(self.select_file)

        # Alineación
        grid_layout.addWidget(select_file_button, 2, 1, alignment=Qt.AlignmentFlag.AlignRight)

        # Estilos
        select_file_button.setMinimumWidth(140)


        ### SELECCIONAR RUTA MODELO A USAR #################################################################
        # LABEL DE TEXTO
        label_text = QLabel("Selecionar ruta del modelo que se desea utilzar para predecir: ")
        grid_layout.addWidget(label_text, 3, 0)

        # INPUT DE TEXTO
        self.text_input = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(self.text_input, 3, 1)

        # BOTÓN PARA SELECCIONAR ARCHIVO
        select_file_button = QPushButton("Seleccionar Archivo")
        select_file_button.clicked.connect(self.select_file)
        # Alineación
        grid_layout.addWidget(select_file_button, 4, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos
        select_file_button.setMinimumWidth(140)

        ### BOTÓN PARA EMPEZAR ENTRENAMIENTO ###########################################################
        # LABEL DE TEXTO
        label_text = QLabel("Predecir valores")
        grid_layout.addWidget(label_text, 5, 0)

        # Crear un botón
        self.scrape_button = QPushButton("Predecir valor")

        # Conectar la señal clicked del botón a la función iniciar_scrapear_thread e iniciar la barra de progreso
        #self.scrape_button.clicked.connect(self.iniciar_scrapear_thread)

        # Alineación y estilos
        grid_layout.addWidget(self.scrape_button, 5, 1)
        self.scrape_button.setMaximumWidth(150)


        ###  SELECCIONAR RUTA DONDE GUARDAR EL EXCEL OUTPUT DEL SCRAPER  ###################################
        # LABEL TEXTO 
        label_text = QLabel("Ruta output donde guardar estadisticas del modelo:")
        grid_layout.addWidget(label_text, 6, 0)

        # INPUT TEXTO (QLineEdit en lugar de QSpinBox)
        text_input = QLineEdit(self)
        # Alineación
        grid_layout.addWidget(text_input, 6, 1)
        # Estilos 
        self.text_input.setMinimumWidth(350)

        # BOTÓN PARA SELECCIONAR CARPETA
        select_folder_button = QPushButton("Seleccionar Carpeta")
        select_folder_button.clicked.connect(self.select_folder)
        # Alineación
        grid_layout.addWidget(select_folder_button, 7, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos
        select_folder_button.setMinimumWidth(140)

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
            self.text_input.setText(self.selected_path)

    def select_folder(self):
        # Obtener el directorio del script de Python
        script_directory = os.path.dirname(__file__)
        
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta", script_directory)
        if folder_path:
            # Actualizar las variables de clase con la carpeta y la ruta seleccionadas
            self.selected_folder = folder_path
            self.selected_path = folder_path

            # Actualizar el QLineEdit con la ruta seleccionada
            self.text_input.setText(self.selected_path)


class PlayerScraperWindowSC(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Contenido de la Ventana 4")
        layout.addWidget(label)
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

        ### SELECCIONAR JORNADA INPUT ####################################################
        # INPUT NÚMERO JORNADA 
        label_number = QLabel("Jornada a scrapear:")
        layout.addWidget(label_number, 0, 0)
        # Estilos 
        self.number_input = QSpinBox(self)
        self.number_input.setMinimum(11)  # Establecer el valor mínimo (jornada 1)
        self.number_input.setMaximum(38)  # Establecer el valor máximo (Jornada 36)
        self.number_input.setSingleStep(2)  # Establecer el paso
        self.number_input.setMaximumSize(38, 20)
        self.number_input.setMinimumSize(38, 20)
        # Aliniación
        layout.addWidget(self.number_input, 0, 1)
        

        #------- GAP vacio -----------------------------------------
        empty_widget = QWidget()
        empty_widget.setFixedHeight(10)  # Tamaño del gap (10 px)
        layout.addWidget(empty_widget, 4, 0)
        #-----------------------------------------------------------


        ###  SELECCIONAR RUTA DONDE GUARDAR EL EXCEL OUTPUT DEL SCRAPER  #################
        # LABEL TEXTO 
        label_text = QLabel("Ruta output scraper:")
        layout.addWidget(label_text, 2, 0)

        # INPUT TEXTO (QLineEdit en lugar de QSpinBox)
        self.text_input = QLineEdit(self)
        # Alineación
        layout.addWidget(self.text_input, 2, 1)
        # Estilos 
        self.text_input.setMinimumWidth(350)
        

        # BOTÓN PARA SELECCIONAR CARPETA
        select_folder_button = QPushButton("Seleccionar Carpeta")
        select_folder_button.clicked.connect(self.select_folder)
        # Alineación  
        layout.addWidget(select_folder_button, 3, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # Estilos 
        select_folder_button.setMinimumWidth(140)

        #------- GAP vacio -----------------------------------------
        empty_widget = QWidget()
        empty_widget.setFixedHeight(10)  # Tamaño del gap (10 px)
        layout.addWidget(empty_widget, 4, 0)
        #-----------------------------------------------------------


        ###  BOTÓN PARA INICIAR SCRAPER  ################################################
        # Crear un botón llamado "Scrapear"
        scrape_button = QPushButton("Scrapear")

        # Conectar la señal clicked del botón a la función iniciar_scrapear_thread e iniciar barra progreso
        scrape_button.clicked.connect(self.iniciar_scrapear_thread)
        scrape_button.clicked.connect(self.start_progress)

        # Alineación 
        layout.addWidget(scrape_button, 5, 0)
        # Estilos
        self.number_input.setMaximumSize(38, 20)


        ###  BARRA DE PROGRESO  ################################################
        # Crear Barra de progreso
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)


        ###  VENTANA OUTPUT SCRAPER  ####################################################
        # Crear un QTextEdit para la salida
        self.output_textedit = QTextEdit(self)
        layout.addWidget(self.output_textedit, 6, 0, 2, 0)  # row, column, rowSpan, columnSpan


        ###  ESTABLECER DISEÑO DE LA VENTANA  ###########################################
        self.setMinimumSize(500, 500) # Configurar el tamaño mínimo de la ventana
        # Configurar el diseño para la ventana
        self.setLayout(layout)

        # Configurar el título de la ventana
        self.setWindowTitle("Mister Fantasy Mundo Deportivo Scraper")

        # Evento cerrar ventana 
        self.destroyed.connect(self.cleanup)

    def select_folder(self):
        # Obtener el directorio del script de Python
        script_directory = os.path.dirname(__file__)
        
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta", script_directory)
        if folder_path:
            # Actualizar las variables de clase con la carpeta y la ruta seleccionadas
            self.selected_folder = folder_path
            self.selected_path = folder_path

            # Actualizar el QLineEdit con la ruta seleccionada
            self.text_input.setText(self.selected_path)

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
        inputgmail.send_keys(usuario)

        # Localiza el elemento del input gmail
        inputpsw = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[2]/input')

        # Borra cualquier contenido existente en la caja de texto (opcional)
        inputpsw.clear()

        # Ingresa texto en la caja de texto
        inputpsw.send_keys(contrasena)

        # Encuentra el botón de "sing con gmail" 
        button = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/form/div[3]/button')
        button.click()

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


def main():
    app = QApplication(sys.argv)
    ventana_principal = VentanaPrincipal()
    ventana_principal.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()