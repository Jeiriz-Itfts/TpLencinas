from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .db_setup import Base, Participantes


engine = create_engine('sqlite:///concurso.db')

# trabajar con esa db
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()  # conrtol de db objeto

# agregar valor objeto/registro
participante = Participantes(
nro=nro,
nombre=nombre,
apellido=apellido,
edad=edad,
sexo=sexo,
disparo1=disparos[0],
disparo2=disparos[1],
disparo3=disparos[2],
mejorDisparo=mejorD,
promedio=promedio)

session.add(participante)
session.commit()