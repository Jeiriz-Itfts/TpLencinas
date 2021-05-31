from sqlalchemy import Column, Integer, String, create_engine, Float
from sqlalchemy.ext.declarative import declarative_base

# declarar db
from sqlalchemy.orm import sessionmaker

def crearBase():
    Base = declarative_base()
    return Base

def crear_tablas(Base):
    class Participantes(Base):
        __tablename__ = 'participantes'
        id = Column(Integer, primary_key=True)
        nro = Column(Integer, nullable=False)
        nombre = Column(String(30), nullable=False)
        apellido = Column(String(30), nullable=False)
        edad = Column(Integer, nullable=False)
        sexo = Column(String(30), nullable=False)
        disparo1 = Column(Integer, nullable=False)
        disparo2 = Column(Integer, nullable=False)
        disparo3 = Column(Integer, nullable=False)
        mejorDisparo = Column(Float, nullable=False)
        promedio = Column(Float, nullable=False)
    return Participantes

def crear_motor(Base):
    engine = create_engine('sqlite:///concurso.db')
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session
