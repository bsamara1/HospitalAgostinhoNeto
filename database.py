import sqlite3

DATABASE = "database/hospital.db"

def conectar():
    return sqlite3.connect(DATABASE)


def criar_tabelas():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS utilizadores(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        username TEXT UNIQUE,
        senha TEXT,
        perfil TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        especialidade TEXT,
        horario TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pacientes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        telefone TEXT,
        nascimento TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consultas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente INTEGER,
        medico INTEGER,
        data TEXT,
        hora TEXT,
        prioridade TEXT,
        estado TEXT,
        FOREIGN KEY(paciente) REFERENCES pacientes(id),
        FOREIGN KEY(medico) REFERENCES medicos(id)
    )
    """)

    conn.commit()
    conn.close()