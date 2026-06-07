"""Modelos SQLAlchemy para persistência"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class PacienteDB(Base):
    __tablename__ = 'pacientes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(200), nullable=False)
    idade = Column(Integer, nullable=False)
    genero = Column(String(20))
    telefone = Column(String(20))
    endereco = Column(String(300))
    data_cadastro = Column(DateTime, default=datetime.now)


class MedicoDB(Base):
    __tablename__ = 'medicos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(200), nullable=False)
    idade = Column(Integer, nullable=False)
    crm = Column(String(20), unique=True, nullable=False)
    especialidade = Column(String(100), nullable=False)
    genero = Column(String(20))
    telefone = Column(String(20))


class UsuarioDB(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    senha_hash = Column(String(100), nullable=False)
    perfil = Column(String(20), nullable=False)  # super_admin, admin, enfermeiro, medico


class TriagemDB(Base):
    __tablename__ = 'triagens'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    sintomas = Column(Text, nullable=False)
    urgencia = Column(Integer, nullable=False)
    especialidade_sugerida = Column(String(100))
    data_hora = Column(DateTime, default=datetime.now)


class ConsultaDB(Base):
    __tablename__ = 'consultas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    medico_id = Column(Integer, ForeignKey('medicos.id'), nullable=False)
    data_hora = Column(DateTime, nullable=False)
    status = Column(String(20), default='agendada')
    diagnostico = Column(Text)
    doenca_real = Column(String(100))
    prescricao = Column(Text)
    observacoes = Column(Text)