import sqlite3
from database.conexao import obter_conexao

def inicializar_base_de_dados():
    conn = obter_conexao()
    if conn is None:
        return
        
    cursor = conn.cursor()
    
    # 1. Tabela de Utilizadores (Segurança e Controle de Acesso)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            cargo TEXT NOT NULL
        )
    """)
    
    # 2. Tabela de Pacientes Triados (Cadastro Inicial + Triagem Unificada)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes_triados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL,
            documento TEXT,
            temperatura REAL NOT NULL,
            sintomas TEXT NOT NULL,          -- Guardado como string separada por virgulas
            seccao_encaminhada TEXT NOT NULL, -- Pediatria, Banco de Urgencia Infantil, etc.
            nivel_urgencia TEXT NOT NULL,
            cor_protocolo TEXT NOT NULL,
            status TEXT DEFAULT 'Aguardando Consulta'
        )
    """)
    
    # 3. Tabela de Consultas Clínicas (Histórico Médico)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            medico_id INTEGER NOT NULL,
            diagnostico_ia TEXT,
            diagnostico_final TEXT NOT NULL,
            medicamentos TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes_triados(id),
            FOREIGN KEY (medico_id) REFERENCES usuarios(id)
        )
    """)
    
    # Inserir o administrador padrão se não existir
    cursor.execute("INSERT OR IGNORE INTO usuarios (username, senha, cargo) VALUES ('admin', 'admin123', 'ADMIN')")
    
    conn.commit()
    conn.close()
    print("[BD] Base de dados inicializada com sucesso!")