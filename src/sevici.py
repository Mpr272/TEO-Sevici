import csv
import math 
import folium
import webbrowser
import os
from collections import namedtuple

# Creación de un tipo de namedtuple para las coordenadas
# type: Coordenadas(float, float)
Coordenadas = namedtuple('Coordenadas', 'latitud, longitud')
# Creación de un tipo de namedtuple para las estaciones
# type: Estacion(str, int, int, int, Coordenadas(float, float))
Estacion = namedtuple('Estacion', 'nombre, bornetas, bornetas_vacias, bicis_disponibles, coordenadas')

def lee_estaciones(fichero):
    res = []
    with open(fichero,encoding="utf-8") as f:
        lector = csv.reader(f)
        next(lector)
        for nombre, bornetas, bornetas_vacias, bicis_disponibles, latitud, longitud in lector:
            bornetas = int(bornetas)
            bornetas_vacias = int(bornetas_vacias)
            bicis_disponibles = int(bicis_disponibles)
            coordenadas = Coordenadas(float(latitud),float(longitud))
            tupla = Estacion(nombre, bornetas, bornetas_vacias, bicis_disponibles, coordenadas)
            res.append(tupla)
        return res

def estaciones_bicis_libres(estaciones:list[Estacion], k=5):
    res = []
    for r in estaciones:
        if r.bicis_disponibles >= k:
            res.append((r.bicis_disponibles,r.nombre))
    return res


def calcula_distancia(coordenadas1, coordenadas2):
    distancia = math.sqrt((coordenadas2[0]-coordenadas1[0])**2 + (coordenadas2[1]-coordenadas1[1])**2)
    return distancia

def estaciones_cercanas(estaciones:list[Estacion], coordenadas, k=5):
    res = []
    for r in estaciones:
        res.append(((calcula_distancia(coordenadas,r.coordenadas)),r.nombre,r.bicis_disponibles))
    
    res.sort(key=lambda x:x[0])
    return res

def crea_mapa(latitud, longitud, zoom=9):
    mapa = folium.Map(location=[latitud, longitud], zoom_start=zoom)
    return mapa  

def crea_marcador (latitud, longitud, etiqueta, color):
    marcador = folium.Marker([latitud,longitud], popup=etiqueta, icon=folium.Icon(color=color, icon='info-sign')) 
    return marcador

def media_coordenadas(estaciones:list[Estacion]):
    res = []
    latitud = 0
    longitud = 0
    n = len(estaciones)
    for r in estaciones:
        latitud += r.coordenadas.latitud
        longitud += r.coordenadas.longitud
    res2 = Coordenadas(latitud/n,longitud/n)
    return res2

def crea_mapa_estaciones(estaciones:list[Estacion],funcion_color):

    #Calculamos la media de las coordenadas de las estaciones, para poder centrar el 
    #mapa
    centro_mapa = media_coordenadas(estaciones)
    # creamos el mapa con folium
    mapa = crea_mapa(centro_mapa.latitud, centro_mapa.longitud, 13)

    for estacion in estaciones:
        etiqueta = estacion.nombre
        color = funcion_color(estacion)
        marcador = crea_marcador (estacion.coordenadas.latitud, estacion.coordenadas.longitud, etiqueta, color)
        marcador.add_to(mapa)
    
    return mapa

def guarda_mapa(mapa, ruta_fichero):
    '''Guard un mapa como archivo html

    :param mapa: Mapa a guardar
    :type mapa: folium.Map
    :param ruta_fichero: Nombre y ruta del fichero
    :type ruta_fichero: str
    '''
    mapa.save(ruta_fichero)
    # Abre el fichero creado en un navegador web
    webbrowser.open("file://" + os.path.realpath(ruta_fichero))

def color_azul(estacion):
   '''Función que devuelve siempre azul
   ENTRADA
      :param estacion: Estación para la que quiero averiguar el color
      :type estacion: Estacion(str, int, int, int, Coordenadas(float, float))
   SALIDA
      :return: El color azul
      :rtype: str
   '''
   return "blue"



