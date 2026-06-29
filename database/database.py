import sqlite3
import os

# Define o caminho absoluto para o ficheiro da base de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(BASE_DIR, exist_ok=True)
DATABASE = os.path.join(BASE_DIR, "hospital.db")

def conectar():
    """Estabelece a conexão com o banco de dados SQLite."""
    return sqlite3.connect(DATABASE)


def criar_tabelas():
    """Cria todas as tabelas do sistema caso não existam e aplica migrações de colunas."""
    conn = conectar()
    cursor = conn.cursor()

    # 1. Tabela de Utilizadores (com os campos email e telefone integrados)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS utilizadores(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        username TEXT UNIQUE,
        senha TEXT,
        perfil TEXT,
        email TEXT,
        telefone TEXT
    )
    """)

    # Garante que as colunas novas existem mesmo se o ficheiro .db antigo não tiver sido apagado
    try:
        cursor.execute("ALTER TABLE utilizadores ADD COLUMN email TEXT")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE utilizadores ADD COLUMN telefone TEXT")
    except sqlite3.OperationalError:
        pass

    # 2. Tabela de Médicos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT,
        especialidade TEXT,
        telefone TEXT,
        estado TEXT
    )
    """)

    # 3. Tabela de Pacientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pacientes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        sexo TEXT,
        idade INTEGER,
        telefone TEXT,
        bi TEXT,
        nascimento TEXT,
        morada TEXT
    )
    """)

    # 4. Tabela de Consultas / Fila de Espera
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
    """Insere o utilizador administrador padrão do sistema."""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO utilizadores
    (nome, username, senha, perfil, email, telefone)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "Administrador",
        "admin",
        "1234",
        "Administrador",
        "admin@han.cv",
        "+238 999 99 99"
    ))

    conn.commit()
    conn.close()


# ==========================================
# FUNÇÕES DE CONSULTA E LISTAGEM
# ==========================================

def consultas_hoje():
    """Lista as consultas agendadas para o dia atual."""
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
        JOIN pacientes p ON c.paciente = p.id
        JOIN medicos m ON c.medico = m.id
        WHERE c.data = date('now')
        ORDER BY c.hora
    """)

    dados = cursor.fetchall()
    conn.close()
    return dados


def consultar_prioridade():
    """Conta a quantidade de consultas por prioridade para o dia de hoje."""
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
    """Lista todos os médicos cadastrados e os seus horários."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nome, especialidade, horario
        FROM medicos;
    """)

    dados = cursor.fetchall()
    conn.close()
    return dados


def listar_pacientes():
    """Lista todos os pacientes registados no hospital por ordem de inserção."""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, sexo, idade, telefone, bi, morada
        FROM pacientes
        ORDER BY id DESC
    """)

    dados = cursor.fetchall()
    conn.close()
    return dados


<<<<<<< HEAD
# ==========================================
# GESTÃO DA FILA DE PRIORIDADES
# ==========================================

def listar_prioridades(filtro_prioridade="Todos"):
    """
    Retorna as consultas ordenadas por gravidade clínica:
    Urgente -> Alta -> Média -> Baixa.
    """
    conn = conectar()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            c.id,
            p.nome AS paciente,
            c.prioridade,
            c.hora AS hora_chegada,
            m.nome AS medico
        FROM consultas c
        JOIN pacientes p ON c.paciente = p.id
        JOIN medicos m ON c.medico = m.id
    """
    
    parametros = []
    if filtro_prioridade != "Todos":
        query += " WHERE c.prioridade = ?"
        parametros.append(filtro_prioridade)
        
    # Regra customizada CASE para forçar a ordem clínica correta no banco
    query += """
        ORDER BY 
            CASE c.prioridade
                WHEN 'Urgente' THEN 1
                WHEN 'Alta' THEN 2
                WHEN 'Média' THEN 3
                WHEN 'Baixa' THEN 4
                ELSE 5
            END, c.hora ASC
    """
    
    cursor.execute(query, parametros)
    dados = cursor.fetchall()
    conn.close()
    return dados


def atualizar_prioridade_consulta(consulta_id, nova_prioridade):
    """Atualiza a prioridade de uma consulta específica via ID."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE consultas 
        SET prioridade = ? 
        WHERE id = ?
    """, (nova_prioridade, consulta_id))
    conn.commit()
    conn.close()
=======
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
>>>>>>> ca37562200f9d4a2ef9d31735ffb00e513f6def2
