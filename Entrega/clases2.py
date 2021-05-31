from math import sqrt
from decimal import Decimal
from prettytable import PrettyTable  # pip install -U prettytable
import requests, json
import csv




class Participante:

    def __init__(self, id, nombre, apellido, edad, sexo):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.sexo = sexo


class Disparo(Participante):

    def __init__(self, id, nombre, apellido, edad, sexo, disparos=[], mejorD=0, promedio=0):
        Participante.__init__(self, id, nombre, apellido, edad, sexo)
        self.disparos = disparos
        self.mejorD = mejorD
        self.promedio = promedio
        self.sum = 0

    def disparo(self):
        for i in range(1, 4):
            print("\nIngrese coordenadas del disparo: {}".format(i))
            x = float(input("Coordenada X: "))
            y = float(input("Coordenada Y: "))
            disparo = int(sqrt(x ** 2 + y ** 2))
            self.disparos.append(disparo)
            self.disparos.sort()
            self.mejorD = float(self.disparos[0])
        for p in self.disparos:  # [0,1,2]
            self.sum += p
            if self.sum == 0:
                self.promedio = 0
            else:
                self.promedio = Decimal(self.sum / 3)

    def __str__(self):
        return '''
                Id: {}
                Nombre: {}
                Apellido: {}
                Edad: {}
                Sexo: {}
                Mejor disparo: {}'''.format(self.id, self.nombre, self.apellido, self.edad, self.sexo, self.disparos,
                                            self.mejorD)


class Concurso:
    participantes = []
    ganadorDict = {}

    def agregarP(self, participante):
        self.participantes.append(participante)

    def mostrarReg(self):
        x = PrettyTable()
        x.field_names = ["ID", "NOMBRE", "APELLIDO", "EDAD", "SEXO", "DISPAROS", "MEJOR DISPARO", "PROMEDIO"]
        for p in self.participantes:
            x.add_row([p.id, p.nombre, p.apellido, p.edad, p.sexo, p.disparos, p.mejorD, round(p.promedio, 2)])
        print(x.get_string())

    def podio(self):
        v = self.participantes
        for i in range(len(v) - 1):
            for k in range(len(v) - 1 - i):
                if v[k].mejorD > v[k + 1].mejorD:
                    v[k], v[k + 1] = v[k + 1], v[k]  # [1, 'juan', apellido, edad, sexo,[0,1,2],mejorDis,Prom]
        c = 1
        print("Los ganadores son: ")
        for p in v:
            print('''
            {}°
             Nombre: {}
             Apellido: {}
             Mejor Disparo: {}'''.format(c, p.nombre, p.apellido, p.mejorD))
            c += 1
            if c == 4:
                break

    def ultimo(self):
        print("El ultimo participante es: ")
        print(self.participantes[-1])

    def cantidad(self):
        print("La cantidad de participantes es: {}".format(len(self.participantes)))

    def registrosXedad(self):
        print("Listado de participantes ordenados por edad: ")
        v = self.participantes
        for i in range(len(v) - 1):
            for k in range(len(v) - 1 - i):
                if v[k].edad > v[k + 1].edad:
                    v[k], v[k + 1] = v[k + 1], v[k]
        x = PrettyTable()
        x.field_names = ["ID", "NOMBRE", "APELLIDO", "EDAD", "SEXO", "DISPAROS", "MEJOR DISPARO", "PROMEDIO"]
        for p in v:
            x.add_row([p.id, p.nombre, p.apellido, p.edad, p.sexo, p.disparos, p.mejorD, round(p.promedio, 2)])
        print(x.get_string())

    def mostrarProm(self):
        c = 1
        for i in self.participantes:
            print("{}°\nPromedio: {} \n"
                  "Disparos: {} \n".format(c, round(i.promedio, 2), i.disparos))
            c += 1

    def orden(self):
        v = self.participantes
        for i in range(len(v) - 1):
            for k in range(len(v) - 1 - i):
                if v[k].mejorD > v[k + 1].mejorD:
                    v[k], v[k + 1] = v[k + 1], v[k]
        return v

    def csv(self, v):
        with open("participantes", 'w') as archivo:
            escribir = csv.writer(archivo, dialect='excel-tab')
            escribir.writerow(['ID', 'NOMBRE', 'APELLIDO', 'EDAD', 'SEXO', 'DISPAROS', 'MEJOR DISPARO', 'PROMEDIO'])
            for i in v:
                escribir.writerow(
                    [i.id, i.nombre, i.apellido, i.edad, i.sexo, i.disparos, i.mejorD, round(i.promedio, 2)])
        print("Andá a mirar el archivo CSV...")

    def ganador(self, v):
        c = 0
        for p in v:
            self.ganadorDict["Ganador"] = p.nombre
            self.ganadorDict["Disparo"] = p.mejorD
            c += 1
            if c == 1:
                break
        return self.ganadorDict

    def apiPremio(self, ganadorDict):
        url = "http://13.58.21.137/flask/api/v2/{}/{}".format(ganadorDict["Ganador"], ganadorDict["Disparo"])
        response = requests.request("GET", url)
        jsonDict = json.loads(response.text)
        print('''Felicidades {} por ganar el premio {} con el disparo {}'''.format(jsonDict["nombre"], jsonDict["premio"],ganadorDict["Disparo"]))

    def guardarDB(self,Participantes,session):
        for i in self.participantes:
            participante = Participantes \
                    (
                    nro=i.id,  # deberia ser nro para no confundir
                    nombre=i.nombre,
                    apellido=i.apellido,
                    edad=i.edad,
                    sexo=i.sexo,
                    disparo1=i.disparos[0],
                    disparo2=i.disparos[1],
                    disparo3=i.disparos[2],
                    mejorDisparo=round(i.mejorD, 2),
                    promedio=i.promedio
                )
            session.add(participante)
            session.commit()
        print('''
        La DB se creó correctamente.
        A continuación se podrán visualizar los registros....''')

    def visualizarDB(self,session,Participantes):
        x = PrettyTable()
        x.field_names = ["ID", "NOMBRE", "APELLIDO", "EDAD", "SEXO", "DISPARO 1","DISPARO 2", "DISPARO 3", "MEJOR DISPARO", "PROMEDIO"]
        listaUsuariosDb = session.query(Participantes).all()
        for p in listaUsuariosDb:
            x.add_row(
                [p.id, p.nombre, p.apellido, p.edad, p.sexo, p.disparo1,p.disparo2,p.disparo3, round(p.mejorDisparo, 2), round(p.promedio, 2)])
        print(x.get_string())
