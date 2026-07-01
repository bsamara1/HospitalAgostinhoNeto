# Manual de Alterações — Sistema HAN
**Hospital Agostinho Neto — Sistema de Gestão Hospitalar**

Este documento explica todas as alterações feitas ao projeto, o que mudou, onde está e porquê foi necessário mudar.

---

## Índice

1. [Problema original](#1-problema-original)
2. [Nova arquitetura — janela única](#2-nova-arquitetura--janela-única)
3. [Ficheiro: main.py](#3-ficheiro-mainpy)
4. [Ficheiro: interface/app_shell.py (NOVO)](#4-ficheiro-interfaceapp_shellpy-novo)
5. [Ficheiro: interface/login.py](#5-ficheiro-interfaceloginpy)
6. [Ficheiro: interface/main_window.py](#6-ficheiro-interfacemain_windowpy)
7. [Ficheiro: interface/_base.py](#7-ficheiro-interface_basepy)
8. [Ficheiros de ecrã (dashboard, medicos, pacientes…)](#8-ficheiros-de-ecrã)
9. [Ficheiro: database/database.py](#9-ficheiro-databasedatabasepy)
10. [Ficheiro: requirements.txt](#10-ficheiro-requirementstxt)
11. [Regras para adicionar um novo ecrã](#11-regras-para-adicionar-um-novo-ecrã)

---

## 1. Problema original

O projeto tinha vários problemas graves que impediam a navegação normal:

### Problema A — Cada ecrã era uma janela independente
Cada ficheiro (login, dashboard, médicos, pacientes…) criava o seu próprio `ctk.CTk()` — ou seja, o seu próprio intérprete Tkinter. Ao navegar entre ecrãs:
- A janela atual era destruída com `self.destroy()`
- Uma nova janela era criada do zero

**Consequência:** todas as imagens criadas (logo, ícones, avatar) ficavam inválidas porque pertenciam ao intérprete anterior. Aparecia o erro:
```
_tkinter.TclError: image "pyimage4" doesn't exist
```

### Problema B — Código duplicado em todos os ficheiros
A sidebar, a topbar e a lógica de navegação estavam copiadas em todos os 10+ ficheiros, com bugs ligeiramente diferentes em cada um (por exemplo, `if/if/elif` em vez de `if/elif/elif`).

### Problema C — requirements.txt errado
O ficheiro continha o texto `python main.py` em vez das dependências reais. Qualquer pessoa que clonasse o projeto e corresse `pip install -r requirements.txt` não instalava nada.

### Problema D — Schema da base de dados desatualizado
A tabela `medicos` local tinha colunas antigas (`especialidade`, `horario`) mas o código tentava inserir colunas novas (`email`, `telefone`, `estado`). Os dados não eram guardados.

---

## 2. Nova arquitetura — janela única

### Antes
```
root (CTk, escondido)
 ├── Login (CTkToplevel) — ao fazer login: destroy + novo CTk
 │    └── Dashboard (CTk) — ao clicar menu: destroy + novo CTk
 │         └── Medicos (CTk) — ao clicar menu: destroy + novo CTk
 │              └── ...
```
Cada navegação destruía e criava janelas → imagens inválidas, efeito de piscar.

### Agora
```
root (CTk, escondido)
 └── AppShell (CTkToplevel) — NUNCA fecha, só troca o conteúdo interno
      ├── LoginContent    — renderiza dentro do AppShell
      └── MainContent     — renderiza dentro do AppShell
           ├── Sidebar (fixa, construída uma vez)
           └── content_frame (área direita, só esta parte muda)
                ├── DashboardContent
                ├── MedicosContent
                ├── PacientesContent
                └── ...
```

**Regra fundamental:** nenhum ecrã é uma janela. Todos são classes simples que recebem um `parent` (frame) e renderizam o seu conteúdo dentro dele.

---

## 3. Ficheiro: `main.py`

**O que faz:** ponto de entrada da aplicação.

**O que mudou:**
- Antes criava `Login(root)` diretamente
- Agora cria `AppShell(root)` — a janela única que gere tudo

**Porquê:** o `AppShell` é responsável por decidir o que mostrar (login ou app). O `main.py` não precisa de saber nada sobre isso.

```python
# Antes
from interface.login import Login
Login(root)

# Agora
from interface.app_shell import AppShell
AppShell(root)
```

Também garante que o diretório de trabalho é sempre a pasta do projeto, independentemente de onde o script for lançado:
```python
os.chdir(os.path.dirname(os.path.abspath(__file__)))
```

---

## 4. Ficheiro: `interface/app_shell.py` (NOVO)

**O que faz:** é a única janela real da aplicação. Nunca fecha — apenas troca o conteúdo interno.

**Método `show_login()`:** limpa a janela e renderiza o ecrã de login.

**Método `show_app()`:** limpa a janela e renderiza a app (sidebar + conteúdo).

**Método `_clear()`:** destrói todos os widgets filhos da janela antes de trocar de ecrã.

```python
class AppShell(ctk.CTkToplevel):
    def show_login(self):
        self._clear()
        LoginContent(self, on_success=self.show_app)

    def show_app(self):
        self._clear()
        MainContent(self, on_logout=self.show_login)
```

**Porquê:** ao trocar de conteúdo dentro da mesma janela, não há piscar e as imagens nunca ficam inválidas porque o intérprete Tkinter é sempre o mesmo.

---

## 5. Ficheiro: `interface/login.py`

**O que faz:** ecrã de autenticação.

**O que mudou:**
- Antes era `class Login(ctk.CTkToplevel)` — uma janela própria
- Agora é `class LoginContent` — uma classe simples que renderiza dentro do `AppShell`

**Como funciona:**
```python
class LoginContent:
    def __init__(self, parent, on_success):
        # parent = o AppShell
        # on_success = função a chamar quando login é bem-sucedido
        self._build()

    def _login(self):
        # verifica credenciais na BD
        if dados:
            self.on_success()   # chama AppShell.show_app()
```

**Porquê:** ao chamar `on_success()` em vez de criar uma nova janela, a transição é suave — o `AppShell` limpa e renderiza a app sem fechar nada.

---

## 6. Ficheiro: `interface/main_window.py`

**O que faz:** constrói a sidebar fixa e gere a navegação entre ecrãs.

**O que mudou:**
- Antes era `class MainWindow(ctk.CTkToplevel)`
- Agora é `class MainContent` — renderiza dentro do `AppShell`

**Método `load_screen(menu_name)`:** limpa o `content_frame` (área direita) e renderiza o ecrã correspondente. A sidebar nunca é tocada.

```python
def load_screen(self, menu_name):
    self._set_active(menu_name)          # destaca o botão ativo na sidebar
    for w in self.content_frame.winfo_children():
        w.destroy()                       # limpa só a área direita
    
    if menu_name == "Médicos":
        from interface.medicos import MedicosContent
        MedicosContent(self.content_frame)
    # ...
```

**Método `terminar_sessao()`:** em vez de criar um novo Login, chama `self.on_logout()` que é o `AppShell.show_login()`.

**Método `_set_active(nome)`:** atualiza a cor dos botões da sidebar — o ativo fica azul (`#2563EB`), os outros ficam transparentes.

---

## 7. Ficheiro: `interface/_base.py`

**O que faz:** funções partilhadas usadas por todos os ecrãs.

**O que mudou:** foi muito simplificado. Antes tinha lógica de sidebar, navegação e logout (que estava duplicada em cada ficheiro). Agora só contém:

### `_topbar_base(parent, titulo)`
Constrói a barra de topo (título da página + avatar + "Administrador") dentro de qualquer frame que lhe seja passado.

### `_placeholder(parent, titulo)`
Mostra um cartão centralizado com ícone 🚧 para ecrãs ainda em desenvolvimento.

**Porquê:** a sidebar e a navegação passaram para o `MainContent` onde pertencem. O `_base.py` só guarda o que é genuinamente partilhado entre ecrãs.

---

## 8. Ficheiros de ecrã

### Padrão de todos os ecrãs

Todos os ecrãs seguem agora o mesmo padrão simples:

```python
class NomeDoEcraContent:
    def __init__(self, parent):
        self.parent = parent
        _topbar_base(parent, "Título do Ecrã")
        # ... conteúdo específico do ecrã
```

Não são janelas. Não têm sidebar. Não têm lógica de navegação. Apenas recebem um `parent` (frame da área direita) e renderizam o seu conteúdo.

---

### `interface/dashboard.py` — `DashboardContent`
Painel principal com 4 cards de estatísticas e 3 tabelas (consultas hoje, prioridades, agenda de médicos). Os dados vêm da base de dados via `consultas_hoje()`, `consultar_prioridade()`, `consultar_agenda_medicos()`.

---

### `interface/medicos.py` — `MedicosContent`

Ecrã completo com:
- **Header** com título e botão "Adicionar Médico"
- **Barra de filtros** com campo de pesquisa (filtra em tempo real por nome, email, especialidade) e ComboBox de estado (Todos / Disponível / Ocupado / Férias)
- **Tabela** com colunas distribuídas com `grid` e pesos proporcionais (as colunas esticam para preencher a largura total)
- **Formulário** de adição em janela popup (`CTkToplevel`)
- **`refresh_table()`** reconstrói só a tabela, mantendo os filtros

**Detalhe importante sobre a tabela:**
As colunas usam `grid` com `grid_columnconfigure(weight=...)` em vez de `pack` com largura fixa. Isso faz com que as colunas se distribuam proporcionalmente pela largura disponível.

```python
_COL_WEIGHTS  = [0, 3, 3, 2, 2, 1, 0]   # 0 = tamanho fixo, >0 = proporcional
_COL_MINSIZES = [60, 160, 160, 130, 120, 110, 190]
```

**Detalhe importante sobre os filtros:**
`table_rows()` começa sempre por limpar o `body` antes de renderizar os resultados filtrados:
```python
def table_rows(self):
    for w in self.body.winfo_children():
        w.destroy()   # OBRIGATÓRIO — sem isto as linhas acumulam-se
    # ... filtra e renderiza
```

---

### `interface/pacientes.py` — `PacientesContent`
Ecrã com tabela de pacientes e formulário de adição. Estrutura idêntica ao de médicos.

---

### `interface/prioridades.py` — `PrioridadesContent`
Fila de espera ordenada por urgência clínica (Urgente → Alta → Média → Baixa). Tem:
- Filtro por categoria (`CTkSegmentedButton`)
- Seleção de linha por clique
- Botão "Alterar Prioridade" que abre um diálogo de texto

---

### `interface/definicao.py` — `DefinicaoContent`
Ecrã de perfil com dois cartões: informações pessoais e alteração de palavra-passe.

---

### Ecrãs em desenvolvimento
Os seguintes ecrãs ainda não têm conteúdo implementado e mostram uma mensagem de "em desenvolvimento":
- `marcacao.py` — `MarcacaoContent`
- `reagendamento.py` — `ReagendamentoContent`
- `cancelamento.py` — `CancelamentoContent`
- `triagem.py` — `TriagemContent`
- `relatorios.py` — `RelatoriosContent`

Para implementar um destes ecrãs, substitui `_placeholder(parent, "Nome")` pelo código real de UI.

---

## 9. Ficheiro: `database/database.py`

**O que mudou:**

### Schema da tabela `medicos` corrigido
A tabela antiga tinha colunas `especialidade` e `horario`. A nova versão tem `email`, `especialidade`, `telefone`, `estado`. O código agora faz migrações automáticas com `ALTER TABLE` para não perder dados se a BD já existir:

```python
for col in ["email TEXT", "telefone TEXT", "estado TEXT"]:
    try:
        cursor.execute(f"ALTER TABLE medicos ADD COLUMN {col}")
    except sqlite3.OperationalError:
        pass   # coluna já existe — não faz nada
```

### Funções novas adicionadas

| Função | O que faz |
|--------|-----------|
| `listar_medicos()` | Retorna todos os médicos (id, nome, email, especialidade, telefone, estado) |
| `listar_prioridades(filtro)` | Retorna consultas ordenadas por gravidade (Urgente → Baixa), com filtro opcional |
| `atualizar_prioridade_consulta(id, nova)` | Atualiza a prioridade de uma consulta específica |

---

## 10. Ficheiro: `requirements.txt`

**O que mudou:** estava com o conteúdo errado (`python main.py`). Corrigido para as dependências reais:

```
customtkinter>=6.0.0
pillow>=12.0.0
```

**Como instalar num clone novo:**
```bash
python -m venv venv
venv\Scripts\Activate.ps1      # Windows PowerShell
pip install -r requirements.txt
python main.py
```

**Nota:** nunca copiar a pasta `venv/` de outro computador. Cada pessoa cria a sua própria com os comandos acima. A pasta `venv/` está no `.gitignore` e não é partilhada pelo git.

---

## 11. Regras para adicionar um novo ecrã

Segue estes passos para implementar, por exemplo, o ecrã de Marcações:

**Passo 1 — Editar `interface/marcacao.py`:**
```python
import customtkinter as ctk
from interface._base import _topbar_base

class MarcacaoContent:
    def __init__(self, parent):
        self.parent = parent
        _topbar_base(parent, "Marcações")
        self.main_ui()          # substitui o _placeholder

    def main_ui(self):
        # o teu código de UI aqui, tudo renderiza dentro de self.parent
        frame = ctk.CTkFrame(self.parent, ...)
        frame.pack(fill="both", expand=True, padx=35, pady=20)
        # ...
```

**Passo 2 — Não precisas de tocar em mais nada.** O `main_window.py` já tem o routing para `MarcacaoContent` quando o utilizador clica em "Marcações" na sidebar.

**Regras a respeitar:**
- A classe recebe sempre `parent` como único argumento
- Nunca criar `ctk.CTk()` ou `ctk.CTkToplevel()` dentro de um ecrã (exceto para popups de formulário com `grab_set()`)
- Nunca importar nem chamar lógica de sidebar, navegação ou logout — isso é responsabilidade do `MainContent`
- Se precisares de um popup (formulário, confirmação), usa `ctk.CTkToplevel(self.parent)` com `grab_set()`

---

*Documento gerado em 29/06/2026*
