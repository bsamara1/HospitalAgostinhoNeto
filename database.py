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
def criar_admin():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO utilizadores
    (nome, username, senha, perfil)
    VALUES (?, ?, ?, ?)
    """, (
        "Administrador",
        "admin",
        "1234",
        "Administrador"
    ))

    conn.commit()
    conn.close()

def consultas_hoje():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.nome,
            m.nome,
            c.hora,
            c.prioridade,
            c.estado
        FROM consultas c
        JOIN pacientes p
            ON c.paciente = p.id
        JOIN medicos m
            ON c.medico = m.id
        WHERE c.data = date('now')
        ORDER BY c.hora
    """)

    dados = cursor.fetchall()

    conn.close()

    return dados

def consultar_prioridade():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT prioridade,
COUNT(*)
FROM consultas
WHERE data=date('now')
GROUP BY prioridade
    """)

    dados = cursor.fetchall()

    conn.close()

    return dados
def consultar_agenda_medicos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
nome,
especialidade,
horario
FROM medicos;
    """)

    dados = cursor.fetchall()

    conn.close()

    return dados