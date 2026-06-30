import sqlite3
import os

# Use an absolute path for the database file (next to this module)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(BASE_DIR, exist_ok=True)
DATABASE = os.path.join(BASE_DIR, "hospital.db")


def conectar():
    """Estabelece a conexão com o banco de dados SQLite."""
    return sqlite3.connect(DATABASE)


def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # 1. Tabela de Utilizadores
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
    #Tabela triagem
    cursor.execute("""    CREATE TABLE IF NOT EXISTS triagem(
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
        FOREIGN KEY(consulta_id) REFERENCES consultas(id)    )    """)

    # Tabela de Consultas / Fila de Espera
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
    # GARANTE QUE ESTA TABELA ESTÁ AQUI ESCRITA EXATAMENTE ASSIM:
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
    # 5. NOVA TABELA: Prioridades
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
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, especialidade, estado FROM medicos")

    dados = cursor.fetchall()
    conn.close()
    return dados


def listar_pacientes():
    """Lista todos os pacientes registados no hospital por ordem de inserção."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome, sexo, idade, telefone, bi, morada
        FROM pacientes ORDER BY id DESC
    """)
    dados = cursor.fetchall()
    conn.close()
    return dados


def listar_medicos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome, email, especialidade, telefone, estado
        FROM medicos ORDER BY id DESC
    """)
    dados = cursor.fetchall()
    conn.close()
    return dados


def listar_prioridades(filtro_prioridade="Todos"):
    conn = conectar()
    cursor = conn.cursor()
    
    # Busca os dados de prioridade juntando com o nome vindo da tabela de pacientes
    query = """
        SELECT pr.id, p.nome, pr.nivel, pr.hora_chegada, pr.medico
        FROM prioridades pr
        JOIN pacientes p ON pr.paciente_id = p.id
    """
    parametros = []
    if filtro_prioridade != "Todos":
        query += " WHERE pr.nivel = ?"
        parametros.append(filtro_prioridade)
        
    query += """
        ORDER BY
            CASE pr.nivel
                WHEN 'Urgente' THEN 1
                WHEN 'Alta' THEN 2
                WHEN 'Média' THEN 3
                WHEN 'Baixa' THEN 4
                ELSE 5
            END, pr.hora_chegada ASC
    """
    cursor.execute(query, parametros)
    dados = cursor.fetchall()
    conn.close()
    return dados

def guardar_triagem(
    consulta_id,
    prioridade,
    temperatura,
    pressao,
    freq_cardiaca,
    saturacao,
    freq_respiratoria,
    glicemia,
    notas
):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO triagem (
            consulta_id,
            temperatura,
            pressao,
            freq_cardiaca,
            saturacao,
            freq_respiratoria,
            glicemia,
            notas,
            triada_em
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
    """, (
        consulta_id,
        temperatura,
        pressao,
        freq_cardiaca,
        saturacao,
        freq_respiratoria,
        glicemia,
        notas
    ))

    # Atualiza também a prioridade na consulta
    cursor.execute("""
        UPDATE consultas
        SET prioridade = ?
        WHERE id = ?
    """, (prioridade, consulta_id))

    conn.commit()
    conn.close()

def atualizar_prioridade_consulta(consulta_id, nova_prioridade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE consultas SET prioridade = ? WHERE id = ?",
                   (nova_prioridade, consulta_id))
    conn.commit()
    conn.close()
    
def listar_consultas_geral(filtro_estado="Todos"):
    """Lista as consultas trazendo os nomes dos pacientes e dos médicos para preencher as tabelas."""
    conn = conectar()
    cursor = conn.cursor()
    
    query = """
        SELECT c.id, p.nome, m.nome, c.data, c.hora, c.estado
        FROM consultas c
        JOIN pacientes p ON c.paciente = p.id
        JOIN medicos m ON c.medico = m.id
    """
    parametros = []
    if filtro_estado != "Todos":
        query += " WHERE c.estado = ?"
        parametros.append(filtro_estado)
        
    query += " ORDER BY c.id DESC"
    cursor.execute(query, parametros)
    dados = cursor.fetchall()
    conn.close()
    return dados


def eliminar_e_cancelar_paciente(paciente_id):
    """Busca o paciente, grava a ação no histórico e elimina-o da tabela de pacientes."""
    conn = conectar()
    cursor = conn.cursor()
    
    # 1. Busca os dados do paciente antes de eliminá-lo para salvar o nome no histórico
    cursor.execute("SELECT nome FROM pacientes WHERE id = ?", (paciente_id,))
    paciente = cursor.fetchone()
    
    if not paciente:
        conn.close()
        return False  # Paciente não encontrado
        
    nome_paciente = paciente[0]
    
    # 2. Opcional: Se quiser também remover as consultas pendentes desse paciente para evitar erros de chave estrangeira
    cursor.execute("DELETE FROM consultas WHERE paciente = ?", (paciente_id,))
    
    # 3. Elimina o paciente da tabela de pacientes
    cursor.execute("DELETE FROM pacientes WHERE id = ?", (paciente_id,))
    
    # 4. Adiciona o registo no histórico de consultas (ou tabela de cancelamentos) informando a exclusão
    cursor.execute("""
        INSERT INTO historico_consultas(paciente_nome, tipo_acao, data_antiga, data_nova, motivo)
        VALUES (?, 'Cancelamento', 'Ativo', 'Nenhum (Eliminado)', 'O paciente foi cancelado e removido do sistema')
    """, (nome_paciente,))
    
    conn.commit()
    conn.close()
    return True
    

def listar_historico_cancelamentos():
    """Procura no histórico todos os registos de cancelamento para exibir na tabela."""
    conn = conectar()
    cursor = conn.cursor()
    # Puxa o ID do histórico, o nome do paciente que foi apagado e a mensagem
    cursor.execute("""
        SELECT id, paciente_nome, tipo_acao, motivo 
        FROM historico_consultas 
        WHERE tipo_acao = 'Cancelamento' 
        ORDER BY id DESC
    """)
    dados = cursor.fetchall()
    conn.close()
    return dados

def reagendar_consulta_por_paciente(paciente_id, nova_data, nova_hora):
    """Procura a consulta ativa do paciente e altera a data e hora."""
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id FROM consultas 
        WHERE paciente = ? AND estado IN ('Em Espera', 'Reagendado')
        ORDER BY id DESC LIMIT 1
    """, (paciente_id,))
    consulta = cursor.fetchone()
    
    if not consulta:
        conn.close()
        return False
        
    cursor.execute("""
        UPDATE consultas 
        SET data = ?, hora = ?, estado = 'Reagendado' 
        WHERE id = ?
    """, (nova_data, nova_hora, consulta[0]))
    conn.commit()
    conn.close()
    return True

def limpar_todos_pacientes_e_id():
    conn = conectar()
    cursor = conn.cursor()
    
    # 1. Apaga os dados
    cursor.execute("DELETE FROM pacientes")
    
    # 2. Reseta o contador interno do SQLite para esta tabela
    cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'pacientes'")
    
    conn.commit()
    conn.close()
    return True

def eliminar_historico_cancelamentos():
    """Apaga TODOS os registos de cancelamento do histórico."""
    conn = conectar()
    cursor = conn.cursor()
    # Apaga as linhas onde o tipo_acao é 'Cancelado'
    cursor.execute("DELETE FROM historico_consultas WHERE tipo_acao = 'Cancelado'")
    conn.commit()
    conn.close()
    return True

def calcular_prioridade(dados):
    score = 0

    # Saturação
    spo2 = float(dados.get("spo2", 100))
    if spo2 < 90:
        score += 4
    elif spo2 < 95:
        score += 2

    # Temperatura
    temp = float(dados.get("temperatura", 36.5))
    if temp >= 39:
        score += 3
    elif temp >= 38:
        score += 2
    elif temp < 35:
        score += 3

    # Frequência cardíaca
    fc = int(dados.get("frequencia_cardiaca", 80))
    if fc > 120:
        score += 3
    elif fc > 100:
        score += 2
    elif fc < 50:
        score += 3

    # Pressão arterial
    pressao = dados.get("pressao", "120/80")

    try:
        sys, dia = pressao.split("/")
        sys = int(sys)
        dia = int(dia)
    except:
        sys = 120
        dia = 80

    if sys < 90 or dia < 60:
        score += 4
    elif sys > 180 or dia > 120:
        score += 4
    elif sys > 140 or dia > 90:
        score += 2

    # Sintomas
    sintomas = dados.get("sintomas", "").lower()

    if "dor no peito" in sintomas:
        score += 4
    if "falta de ar" in sintomas:
        score += 4
    if "desmaio" in sintomas:
        score += 4
    if "convuls" in sintomas:
        score += 4
    if "hemorragia" in sintomas:
        score += 4
    if "dor forte" in sintomas:
        score += 2
    if "febre" in sintomas:
        score += 1

    # Resultado final
    if score >= 8:
        return "Emergente", score
    elif score >= 5:
        return "Muito Urgente", score
    elif score >= 3:
        return "Urgente", score
    elif score >= 1:
        return "Pouco Urgente", score
    else:
        return "Não Urgente", score
    
def listar_fila_triagem():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            c.id,
            p.nome,
            p.idade,
            c.hora,
            c.prioridade,
            c.estado
        FROM consultas c
        JOIN pacientes p ON c.paciente = p.id
        ORDER BY c.id DESC
    """)

    dados = cur.fetchall()
    conn.close()
    return dados
