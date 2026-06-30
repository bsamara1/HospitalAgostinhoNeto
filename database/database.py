import sqlite3
import os
import random

# =========================
# CONFIGURAÇÃO
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(BASE_DIR, exist_ok=True)

DATABASE = os.path.join(BASE_DIR, "hospital.db")


def conectar():
    return sqlite3.connect(DATABASE)


# =========================
# CRIAÇÃO DAS TABELAS
# =========================

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # UTILIZADORES (LOGIN)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS utilizadores(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        username TEXT UNIQUE,
        senha TEXT,
        perfil TEXT,
        email TEXT UNIQUE,
        telefone TEXT
    )
    """)

    # MÉDICOS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT UNIQUE,
        especialidade TEXT,
        telefone TEXT,
        estado TEXT
    )
    """)

    # PACIENTES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pacientes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        sexo TEXT,
        idade INTEGER,
        telefone TEXT,
        bi TEXT,
        nascimento TEXT,
        morada TEXT,
        estado TEXT
    )
    """)

    # CONSULTAS
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

    # TRIAGEM
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS triagem(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        consulta_id INTEGER UNIQUE,
        temperatura TEXT,
        pressao TEXT,
        freq_cardiaca TEXT,
        saturacao TEXT,
        freq_respiratoria TEXT,
        glicemia TEXT,
        notas TEXT,
        triada_em TEXT,
        FOREIGN KEY(consulta_id) REFERENCES consultas(id)
    )
    """)

    # NOTIFICAÇÕES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notificacoes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente INTEGER,
        titulo TEXT,
        mensagem TEXT,
        data TEXT,
        lida INTEGER DEFAULT 0,
        FOREIGN KEY(paciente) REFERENCES pacientes(id)
    )
    """)

    # HISTÓRICO
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historico_consultas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_nome TEXT,
        tipo_acao TEXT,
        data_antiga TEXT,
        data_nova TEXT,
        motivo TEXT
    )
    """)

    # PRIORIDADES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prioridades(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER,
        nivel TEXT,
        medico TEXT,
        hora_chegada TEXT,
        FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
    )
    """)

    conn.commit()
    conn.close()


# =========================
# ADMIN
# =========================

def criar_admin():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO utilizadores
    (nome, username, senha, perfil)
    VALUES (?, ?, ?, ?)
    """, ("Administrador", "admin", "1234", "Administrador"))

    conn.commit()
    conn.close()


# =========================
# UTILIZADORES (LOGIN)
# =========================

def username_existe(username):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM utilizadores WHERE username = ?", (username,))
    existe = cursor.fetchone() is not None

    conn.close()
    return existe


def gerar_username(email):
    base = email.split("@")[0].lower()
    username = base
    contador = 1

    while username_existe(username):
        username = f"{base}{contador}"
        contador += 1

    return username


def recuperar_credenciais(email):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username, senha
        FROM utilizadores
        WHERE email = ?
    """, (email,))

    dados = cursor.fetchone()
    conn.close()

    return dados


# =========================
# MÉDICOS + LOGIN AUTOMÁTICO
# =========================

def email_existe(email):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1 FROM utilizadores WHERE email = ?
    """, (email,))

    existe = cursor.fetchone() is not None
    conn.close()
    return existe


def criar_medico_com_login(nome, email, especialidade, telefone, estado):
    conn = conectar()
    cursor = conn.cursor()

    # evita duplicação de email
    if email_existe(email):
        conn.close()
        return None, None

    # 1. médico
    cursor.execute("""
        INSERT INTO medicos(nome, email, especialidade, telefone, estado)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, email, especialidade, telefone, estado))

    # 2. login automático
    username = gerar_username(email)
    senha = str(random.randint(1000, 9999))

    cursor.execute("""
        INSERT INTO utilizadores(nome, username, senha, perfil, email, telefone)
        VALUES (?, ?, ?, 'Medico', ?, ?)
    """, (nome, username, senha, email, telefone))

    conn.commit()
    conn.close()

    return username, senha


def inserir_medico(nome, email, especialidade, telefone, estado):
    return criar_medico_com_login(nome, email, especialidade, telefone, estado)


# =========================
# CONSULTAS
# =========================

def consultas_hoje():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.nome, m.nome, c.hora, c.prioridade, c.estado
        FROM consultas c
        JOIN pacientes p ON c.paciente = p.id
        JOIN medicos m ON c.medico = m.id
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
        WHERE data = date('now')
        GROUP BY prioridade
    """)

    dados = cursor.fetchall()
    conn.close()
    return dados


def consultar_agenda_medicos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nome, especialidade, estado FROM medicos
    """)

    dados = cursor.fetchall()
    conn.close()
    return dados


# =========================
# LISTAR MÉDICOS
# =========================

def listar_medicos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, email, especialidade, telefone, estado
        FROM medicos
        ORDER BY id DESC
    """)

    dados = cursor.fetchall()
    conn.close()
    return dados