import sqlite3
import random

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
        nome TEXT UNIQUE,
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

    # ==========================================
    # POPULAR AUTOMATICAMENTE COM 30 MÉDICOS
    # ==========================================
    cursor.execute("SELECT COUNT(*) FROM medicos")
    total_medicos = cursor.fetchone()[0]

    if total_medicos < 30:
        nomes = ["Carlos", "Ana", "João", "Maria", "Pedro", "Cláudia", "Manuel", "Sofia", "Rui", "Beatriz", 
                 "António", "Isabel", "Francisco", "Mariana", "José", "Cátia", "Fernando", "Sara", "Ricardo", "Diana"]
        apelidos = ["Silva", "Santos", "Ferreira", "Pereira", "Oliveira", "Costa", "Rodrigues", "Martins", 
                    "Jesus", "Almeida", "Ribeiro", "Carvalho", "Teixeira", "Gomes", "Correia", "Mendes"]
        especialidades = ["Cardiologia", "Pediatria", "Ortopedia", "Neurologia", "Medicina Geral", "Ginecologia"]

        medicos_gerados = set()
        while len(medicos_gerados) < 30:
            nome_completo = f"Dr. {random.choice(nomes)} {random.choice(apelidos)}"
            # Tratamento para nomes femininos
            if any(fem in nome_completo for fem in ["Ana", "Maria", "Cláudia", "Sofia", "Beatriz", "Isabel", "Mariana", "Cátia", "Sara", "Diana"]):
                nome_completo = nome_completo.replace("Dr.", "Dra.")
            
            # Escolhe uma especialidade aleatória e define um horário padrão de teste
            esp = random.choice(especialidades)
            horario = "08:00 - 16:00"
            
            medicos_gerados.add((nome_completo, esp, horario))

        # Insere apenas os que faltam ou todos se estiver zerado
        for nome, esp, hor in medicos_gerados:
            cursor.execute("""
                INSERT INTO medicos (nome, especialidade, horario) 
                VALUES (?, ?, ?)
            """, (nome, esp, hor))
        
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
        SELECT prioridade, COUNT(*)
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
        SELECT nome, especialidade, horario
        FROM medicos;
    """)

    dados = cursor.fetchall()
    conn.close()
    return dados