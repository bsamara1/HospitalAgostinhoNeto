import customtkinter as ctk

def centralizar_janela(janela, largura, altura):
    """Garante o centro absoluto e milimétrico da janela pop-up no monitor."""
    # 1. Força o CustomTkinter a calcular o tamanho real interno dos widgets
    janela.update_idletasks()
    
    # 2. Descobre quem é a janela principal do programa (o root/parent)
    janela_principal = janela.winfo_toplevel()
    if janela.master:
        janela_principal = janela.master.winfo_toplevel()
        
    # 3. Obtém a posição e o tamanho exato da tua aplicação no ecrã
    main_x = janela_principal.winfo_x()
    main_y = janela_principal.winfo_y()
    main_w = janela_principal.winfo_width()
    main_h = janela_principal.winfo_height()
    
    # 4. Caso o programa principal não tenha tamanho válido, usa o monitor inteiro
    if main_w <= 100 or main_h <= 100:
        main_x = 0
        main_y = 0
        main_w = janela.winfo_screenwidth()
        main_h = janela.winfo_screenheight()
        
    # 5. Cálculo matemático preciso do centro absoluto
    x = main_x + (main_w // 2) - (largura // 2)
    y = main_y + (main_h // 2) - (altura // 2)
    
    # Evita que a janela saia das bordas visíveis do monitor
    x = max(0, x)
    y = max(0, y)
    
    # 6. Aplica a geometria e bloqueia o tamanho para evitar desvios temporários
    janela.geometry(f"{largura}x{altura}+{x}+{y}")