# DraftGeniousIQ

DraftGeniousIQ es una aplicación de asistencia multiventana manejada por hilos, desarrollada en Python con una interfaz simple construida con PyQt6. La principal meta de esta herramienta es ofrecer recomendaciones fundamentadas en predicciones precisas para mejorar el rendimiento del usuario al jugar al Fantasy de Mundo Deportivo.

## Objetivo

El objetivo principal de DraftGeniousIQ es asistir al usuario en la toma de decisiones relacionadas con la alineación de su equipo en la próxima jornada del Fantasy de Mundo Deportivo. Esto incluye sugerencias para el once titular, recomendaciones sobre jugadores para mantener en el banquillo, información sobre jugadores en el mercado, y consejos sobre compras y ventas basadas en proyecciones de valor y rendimiento.

## Pequeña vista de la interfaz

![Captura de pantalla 2024-01-21 130204](https://github.com/guti10x/DraftGeniusIQ/assets/82153822/ea8879e0-7a34-4bfa-a32b-82a7e95ecd14)

![Captura de pantalla 2024-01-21 133358](https://github.com/guti10x/DraftGeniusIQ/assets/82153822/8d246d9d-c286-4a29-8e17-d8ca80c31f75)

## Funcionalidades

#### Scraping de Estadísticas

- Scraping de estadísticas de jugadores en partidos específicos de LaLiga.
- Scraping de estadísticas de jugadores en la web de Mister Fantasy Mundo Deportivo.

#### Preprocesamiento y Análisis Exploratorio de Datos

- Realización de preprocesamiento y análisis exploratorio de datos.

#### Generación de Datasets

- Generación de datasets para predicción y entrenamiento.

#### Entrenamiento de Modelos de Predicción

- Entrenamiento de modelos de predicción utilizando algoritmos de machine learning como Linear Regression, KNN o Gradient Boosted Tree.

#### Predicciones

- Realización de predicciones sobre el valor de mercado de un jugador de LaLiga.
- Predicciones sobre el rendimiento de un jugador en el próximo partido de la jornada y sus puntos asociados.

#### Recomendaciones de Alineación


- Recomendaciones para la alineación del once titular.
- Consejos sobre jugadores para mantener en el banquillo.

#### Información de Jugadores en el Mercado

- Información sobre jugadores en el mercado.
- Sugerencias de compras basadas en proyecciones de aumento de valor.
- Sugerencias de ventas anticipadas basadas en pronósticos de devaluación.

#### Puntuación Esperada

- Puntuación esperada de cada jugador para la próxima jornada.

## Instalación

### Paso 1: Preparar el Entorno

Asegúrate de tener Python instalado en tu sistema. Puedes descargar la última versión de Python desde [python.org](https://www.python.org).

### Paso 2: Instalar Dependencias

Para instalar las dependencias del proyecto, utiliza el archivo `requirements.txt`. Ejecuta el siguiente comando en la terminal del directorio del proyecto. Esto instalará automáticamente todas las dependencias especificadas en el archivo.

```bash
pip install -r requirements.txt
```

### Paso 3: Ejecutar script
#### Para Python 2
```bash
python script.py
```
#### Para Python 3
```bash
python3 script.py
```

