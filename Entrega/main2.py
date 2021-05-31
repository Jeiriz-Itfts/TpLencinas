from clases2 import Disparo, Concurso
from db_setup import crearBase, crear_motor, crear_tablas

concurso = Concurso()

fin = 0
print('''
-------------------------------------------------------------------------------------     
             Bienvenidos al campeonato nacional de tiro con arco y flecha.
-------------------------------------------------------------------------------------
         A continuación vas a agregar a los participantes de la competencia
_____________________________________________________________________________________
''')

while fin != 999:
    id = int(input("\nIngrese número del participante: "))
    nombre = input("Ingrese el nombre: ")
    apellido = input("Ingrese el apellido: ")
    edad = int(input("Ingrese la edad: "))
    sexo = input("Ingrese el sexo (m/f): ")
    participante = Disparo(id, nombre, apellido, edad, sexo, disparos=[]
                           , mejorD=0, promedio=0)  # creo objeto participante sin disparos
    participante.disparo()  # obtengo disparos
    participante = Disparo(id, nombre, apellido, edad, sexo, participante.disparos,
                           participante.mejorD,
                           participante.promedio)  # piso objeto participante con disparos hechos
    concurso.agregarP(participante)  # agrego participantes a la lista
    fin = int(input("\nSi desea finalizar de ingresar participantes ingrese <999>,"
                    " si no, cualquier numero: \n"))


def enter(texto):  # Funcion para imprimir texto
    print("\n")
    enter = input(texto)
    print("\n")


def menu():
    eleccion = int(input('''
  ======================================================================
  ======================Elija la opción deseada=========================
  ======================================================================
  ==  1  -->  Visualizar los registros                                ==
  ==  2  -->  Visualizar el podio                                     ==
  ==  3  -->  Visualizar último participante                          ==
  ==  4  -->  Visualicar cantidad de participantes                    ==
  ==  5  -->  Visualizar registros ordenados por edad                 ==
  ==  6  -->  Visualizar promedios de todos los disparos              ==
  ==  7  -->  Guardar los registros en un archivo csv                 ==
  ==  8  -->  Visualizar quien es el ganador y que premio obtuvo      ==
  ==  9  -->  Crear, guardar datos en una DB y visualizarlos          ==
  ==  0  -->  Salir                                                   ==
  ======================================================================
    '''))
    return eleccion


eleccion = menu()

while eleccion != 0:
    if eleccion == 1:
        concurso.mostrarReg()

    elif eleccion == 2:
        concurso.podio()

    elif eleccion == 3:
        concurso.ultimo()

    elif eleccion == 4:
        concurso.cantidad()

    elif eleccion == 5:
        concurso.registrosXedad()

    elif eleccion == 6:
        concurso.mostrarProm()

    elif eleccion == 7:
        concurso.csv(concurso.orden())  # ordeno x mejor puntaje porque estaba por edad

    elif eleccion == 8:
        ganadorDict = concurso.ganador(concurso.orden())
        concurso.apiPremio(ganadorDict)

    elif eleccion == 9:
        Base = crearBase()
        Participantes = crear_tablas(Base)
        session = crear_motor(Base)
        concurso.guardarDB(Participantes, session)
        concurso.visualizarDB(session, Participantes)

    eleccion = menu()
