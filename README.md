# dpreview.com scraping
Scraper de datos sobre cámaras digitales de dpreview.com

Práctica 1 de la asignatura *"Tipología y ciclo de vida de los datos"* del [Máster en Ciencia de Datos de la UOC](https://estudios.uoc.edu/es/masters-universitarios/data-science/presentacion)

# Autores

* Pablo Benito
* Miquel Rived 

# Contexto
Esta práctica se ha realizado bajo el contexto de la asignatura Tipología y ciclo de vida de los datos, perteneciente al Máster en Ciencia de Datos de la Universitat Oberta de Catalunya. En ella, se aplican técnicas de web scraping mediante el lenguaje de programación Python para extraer así datos de la web dpreview.com y generar un dataset.

Digital Photography Review (dpreview.com) es un sitio web sobre cámaras digitales y fotografía digital en el que se pueden encontrar análisis de cámaras digitales, guías de compra, opiniones de usuarios y foros muy activos. Es uno de los 1.500 sitios web más visitados en Internet, además de ser actualmente el sitio de fotografía difital con mayor audiencia. 

Además de lo comentado, lo que ha hecho decantarse por esta dirección para realizar el web scrapping es su amplia base de datos con información sobre cámaras dígitales.

# Definir un título para el dataset
Características y evaluación de cámaras fotográficas digitales

# Descripción del dataset
El `dataset` obtenido mediante el scraper contiene los datos de la base de datos de cámaras digitales recopiladas por [dpreview.com](dpreview.com).

El dataset contiene tanto características de las propias cámaras, como de ls valoración otorgada por los expertos de la propia página y de los usuarios de su comunidad.

# Representación gráfica

Presentar esquema o diagrama que identifique el dataset visualmente y el proyecto elegido

![alt text](representation.png "Representación gráfica del dataset")
# Contenido

Se podrían separar los campos extraídos en cuatro áreas, la primera (list) con breves características de la cámara, la segunda (overview) en la que se profundiza en la valoración dada por los expertos y se extraen otras características como la marca, la tercera (specifications) en la que se extraen la mayor cantidad de especificaciones de la cámara, y la última (user-review) de la que se extraen las valoraciones otorgadas por los usuarios.

Referente a lo que se extrae de la pantalla list, extraemos el nombre y una imagen de la cámara, la fecha del anuncio, especificaciones rápidas, el link de las reviews, así como el valor de las valoraciones de los especialistas. 

En la pantalla overview se extrae la marca de la cámara y su familia, las personas que la tienen, la han tenido o la querrían tener, además una valoración del 0 al 100 referente a los siguientes aspectos: calidad de construcción, ergonomía y manejo, características, precisión de medición y enfoque, calidad de imagen (raw), calidad de imagen (jpeg), rendimiento con poca luz, valoración del visor, modo de vídeo, conectividad y el valor, además de la media de la valoración de los usuarios.

En cuanto a las características de las cámaras se ha extraído una gran cantidad de campos, destacando el precio, los píxeles del sensor, la máxima resolución, el tamaño de la pantalla, el tipo de cuerpo o el MSPR entre muchos otros.

Por lo que se refiere a la pantalla de user-reviews, se ha extraído información de la valoración media de los usuarios y cuantas valoraciones se han hecho en cada cámara.


# Agradecimientos

**dpreview.com** es el sitio web de referencia en lo que a cámaras fotográficas digitales se refiere.

Lleva activo desde 1999 y cuenta con una gran comunidad de usuarios muy activos, sus reviews destacan por su calidad, incorporando muestras fotográficas de un gran número de cámaras digitales. Además, dpreview pertenece al grupo IMDB, famoso por su base de datos de valoraciones de películas y actores.

En el análisis hecho por [fongfan999](https://github.com/fongfan999/dpreview_analyzer) se estudiaron las reseñas en Amazon desde Dpreview.com.

Por otro lado, en el análisis  realizado por [nmounika](https://github.com/nmounika/dpreview_webscrape/blob/master/camera%20webscrape%20dpreview.py) se analizaron las especificaciones de distintas cámaras.



# Inspiración

Lo más interesante del conjunto de datos extraído es la gran cantidad de especificaciones diferentes que se encuentran, así como el gran abanico de cámaras digitales que lo abarcan.

En primer lugar se quiere ver que especificaciones afectan más en el aumento de precio de una cámara digital.

Por otro lado, se quiere ver que cámaras son las más valoradas por los usuarios o los expertos, por lo que se pretenderá analizar las marcas más valoradas, si el precio influye en la valoración final, o que tipo de especificaciones son las que buscan los usuarios en una cámara digital para realizar una valoración alta.

Además de lo comentado con anterioridad, se pretenden responder preguntas como las siguientes:

- ¿Cuál es la cámara mejor valorada por los usuarios?
- ¿Cuál es la cámara más cara y más ergónomica?
- ¿Qué cámara es capaz de disparar más fotografías en modo ráfaga?
- ¿Cuál es la cámara con GPS más ligera y mayor autonomía de batería?

# Licencia
TODO: Seleccione una de estas licencias para su dataset y explique el motivo
de su selección:
- Released Under CC0: Public Domain License
- Released Under CC BY-NC-SA 4.0 License
- Released Under CC BY-SA 4.0 License
- Database released under Open Database License, individual contents
under Database Contents License
- Other (specified above)
- Unknown License

La licencia escogida para la publicación del dataset es Released Under CC BY-SA 4.0 ya que por los motivoss que se listan a continuación relacionados con sus cláusulas se cree que es la más idónea:
- En primer lugar, el hecho de tener que proveer el nombre del creador del conjunto de datos junto con los cambios realizados hace que se valore el trabajo de dpreview.com a la par que se exponen las aportaciones realizadas por nosotros en la extracción.
- Al permitirse su uso comercial hace que se puedan realizar trabajos a partir del dataset que nos reporten cierto reconocimiento.
- Toda contribución realizada a posteriori deberá distribuirse bajo la misma licencia, por lo que todo trabajo realizado sobre el que se está haciendo deberá seguir distribuyéndose bajo los términos planteados.
# Código

El scraper se ha desarrollado en Python utilizando las librerías `requests` y `beautifulsoup`. 

El script se puede consultar 
[aquí](app.py)


# Dataset
El dataset se encuentra publicado en Zenodo en el siguiente repositorio: https://zenodo.org/record/4660007

A continuación se muestra una captura del registro del dataset en Zenodo:
![alt text](zenodo.png "Dataset en Zenodo")
# 
