import sqlite3
import os

# Define o caminho do banco de dados na raiz do projeto para não se perder
DIRETORIO_DB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_DB = os.path.join(DIRETORIO_DB, "hospital.db")

def obter_conexao():
    """
    Cria e retorna uma conexão ativa com o banco de dados SQLite.
    Garante o tratamento de exceções caso o arquivo esteja bloqueado.
    """
    try:
        conexao = sqlite3.connect(CAMINHO_DB)
        # Ativa o suporte a chaves estrangeiras (Foreign Keys) no SQLite
        conexao.execute("PRAGMA foreign_keys = ON;")
        return conexao
    except sqlite3.Error as e:
        print(f"[ERRO DE CONEXÃO]: Não foi possível ligar à Base de Dados: {e}")
        return None