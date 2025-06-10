
from sevici import *

def lee_archivos_test():
    
    resultado = datos
    print("primeras 3 estaciones: ",resultado[:3])



def test_estaciones_bicis_libres(datos):
    resultado = estaciones_bicis_libres(datos)
    k_values = [5, 10, 1]
    for k in k_values:
        
            resultado = estaciones_bicis_libres(datos,k)
            print(f"Hay {len(resultado)} estaciones con {k} o mas bicis libre y las 5 primeras son:", resultado[:5])
            
def test_estaciones_cercanas(datos):
     k = 5
     res = estaciones_cercanas(datos,(37.357659, -5.9863),k)
     print(f"Las {k} estaciones mas cercanas son: ", res[:5])




if __name__ == "__main__":
    datos = lee_estaciones("data/estaciones.csv")
    
    #lee_archivos_test()
    #test_estaciones_bicis_libres(datos)
    test_estaciones_cercanas(datos)

    mapa_estaciones = crea_mapa_estaciones(datos, color_azul)
guarda_mapa(mapa_estaciones, "./out/azul.html")