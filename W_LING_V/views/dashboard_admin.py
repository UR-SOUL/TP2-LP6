'''import customtkinter as ctk
import sqlite3
from tkinter import messagebox, ttk

class DashboardAdmin(ctk.CTkFrame):
    def __init__(self, master, usuario_logado, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#0B132B")
        
        # Bloqueio de Segurança via Código
        if usuario_logado.cargo != "ADMIN":
            ctk.CTkLabel(self, text="⚠️ ACESSO NEGADO: RECURSO PRIVILEGIADO", font=("Segoe UI", 16, "bold"), text_color="#DC2626").pack(pady=50)
            return

        ctk.CTkLabel(self, text="Gestão de Profissionais de Saúde (Acesso Restrito)", font=("Segoe UI", 18, "bold"), text_color="#06B6D4").pack(pady=15)

        # Formulario
        self.frame_form = ctk.CTkFrame(self, fg_color="#1C2541", corner_radius=8)
        self.frame_form.pack(pady=10, padx=20, fill="x")

        self.txt_nome = ctk.CTkEntry(self.frame_form, placeholder_text="Username do Profissional", width=200)
        self.txt_nome.grid(row=0, column=0, padx=10, pady=10)

        self.txt_senha = ctk.CTkEntry(self.frame_form, placeholder_text="Senha", show="*", width=150)
        self.txt_senha.grid(row=0, column=1, padx=10, pady=10)

        self.cb_cargo = ctk.CTkComboBox(self.frame_form, values=["ENFERMEIRO", "MEDICO"], width=150)
        self.cb_cargo.grid(row=0, column=2, padx=10, pady=10)

        self.btn_add = ctk.CTkButton(self.frame_form, text="Registar", fg_color="#10B981", command=self.inserir_profissional, width=100)
        self.btn_add.grid(row=0, column=3, padx=10, pady=10)

        # Tabela Treeview para listagem e remoção
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(pady=15, padx=20, fill="both", expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Nome", "Cargo"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome de Utilizador")
        self.tree.heading("Cargo", text="Cargo Administrativo")
        self.tree.pack(side="left", fill="both", expand=True)

        self.btn_del = ctk.CTkButton(self, text="Remover Profissional Selecionado", fg_color="#DC2626", command=self.deletar_profissional)
        self.btn_del.pack(pady=10)
        
        self.atualizar_tabela()

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, cargo FROM usuarios WHERE cargo != 'ADMIN'")
        for linha in cursor.fetchall():
            self.tree.insert("", "end", values=linha)
        conn.close()

    def inserir_profissional(self):
        nome = self.txt_nome.get()
        senha = self.txt_senha.get()
        cargo = self.cb_cargo.get()
        if not nome or not senha:
            return

        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (username, senha, cargo) VALUES (?, ?, ?)", (nome, senha, cargo))
            conn.commit()
            messagebox.showinfo("Sucesso", f"Profissional {nome} registado com sucesso.")
            self.atualizar_tabela()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Nome de utilizador já existente no hospital.")
        finally:
            conn.close()

    def deletar_profissional(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            return
        val = self.tree.item(item_selecionado)['values']
        
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id=?", (val[0],))
        conn.commit()
        conn.close()
        self.atualizar_tabela()
        '''

import customtkinter as ctk
import sqlite3
from tkinter import messagebox, ttk
from datetime import datetime

class DashboardAdmin(ctk.CTkFrame):
    def __init__(self, master, usuario_logado, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#0B132B")
        
        if usuario_logado.cargo != "ADMIN":
            ctk.CTkLabel(self, text="⚠️ ACESSO RESTRITO: RESERVADO À ADMINISTRAÇÃO", 
                         font=("Segoe UI", 16, "bold"), text_color="#DC2626").pack(pady=100)
            return

        # Criação do Controlado de Abas Interno (Tabview) para Organização Visual
        self.tabview = ctk.CTkTabview(self, fg_color="#1C2541", segmented_button_selected_color="#06B6D4",
                                      segmented_button_unselected_hover_color="#0D9488")
        self.tabview.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.tab_dashboard = self.tabview.add("📊 Painel Estatístico & Casos do Dia")
        self.tab_equipa = self.tabview.add("👥 Gestão da Equipa Técnica")

        # Configurar as duas abas
        self.construir_aba_dashboard()
        self.construir_aba_equipa()

    # --- ABA 1: DASHBOARD & CASOS DIÁRIOS ---
    def construir_aba_dashboard(self):
        # Frame superior para os Cartões de Indicadores Rápidos (KPIs)
        self.f_kpis = ctk.CTkFrame(self.tab_dashboard, fg_color="transparent")
        self.f_kpis.pack(fill="x", pady=10, padx=10)

        # Cartão 1: Total Atendidos Hoje
        self.card_atendidos = ctk.CTkFrame(self.f_kpis, fg_color="#0B132B", border_width=1, border_color="#06B6D4", width=200, height=80)
        self.card_atendidos.pack(side="left", expand=True, padx=10, fill="both")
        self.lbl_kpi_atendidos = ctk.CTkLabel(self.card_atendidos, text="0", font=("Segoe UI", 22, "bold"), text_color="#06B6D4")
        self.lbl_kpi_atendidos.pack(pady=(10, 2))
        ctk.CTkLabel(self.card_atendidos, text="Atendimentos Concluídos Hoje", font=("Segoe UI", 11), text_color="#94A3B8").pack()

        # Cartão 2: Fila Activa no Posto
        self.card_fila = ctk.CTkFrame(self.f_kpis, fg_color="#0B132B", border_width=1, border_color="#EAB308", width=200, height=80)
        self.card_fila.pack(side="left", expand=True, padx=10, fill="both")
        self.lbl_kpi_fila = ctk.CTkLabel(self.card_fila, text="0", font=("Segoe UI", 22, "bold"), text_color="#EAB308")
        self.lbl_kpi_fila.pack(pady=(10, 2))
        ctk.CTkLabel(self.card_fila, text="Pacientes na Fila de Espera", font=("Segoe UI", 11), text_color="#94A3B8").pack()

        # Tabela de Monitorização das Doenças do Dia por Paciente
        ctk.CTkLabel(self.tab_dashboard, text="📈 Registo Clínico em Tempo Real: Patologias Diagnosticadas Hoje", 
                     font=("Segoe UI", 13, "bold"), text_color="white").pack(pady=(15, 5), anchor="w", padx=15)
        
        self.tree_frame = ctk.CTkFrame(self.tab_dashboard)
        self.tree_frame.pack(pady=5, padx=15, fill="both", expand=True)

        # Configuração da Treeview com estilo escuro adaptado
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Treeview", background="#1C2541", foreground="white", fieldbackground="#1C2541", rowheight=28)
        estilo.map("Treeview", background=[("selected", "#0D9488")])

        self.tree_doencas = ttk.Treeview(self.tree_frame, columns=("Paciente", "Idade", "Sintomas", "Previsão IA", "Diagnóstico Final"), show="headings")
        self.tree_doencas.heading("Paciente", text="Nome do Paciente")
        self.tree_doencas.heading("Idade", text="Idade")
        self.tree_doencas.heading("Sintomas", text="Sintomas Apresentados")
        self.tree_doencas.heading("Previsão IA", text="Sugestão da IA")
        self.tree_doencas.heading("Diagnóstico Final", text="Diagnóstico Soberano")
        
        self.tree_doencas.column("Idade", width=60, anchor="center")
        self.tree_doencas.pack(fill="both", expand=True)

        self.btn_atualizar_dash = ctk.CTkButton(self.tab_dashboard, text="🔄 Atualizar Indicadores e Painel", 
                                                fg_color="#06B6D4", font=("Segoe UI", 12, "bold"), command=self.carregar_dados_dashboard)
        self.btn_atualizar_dash.pack(pady=10)
        
        # Carregamento Inicial das Estatísticas
        self.carregar_dados_dashboard()

    def carregar_dados_dashboard(self):
        # Limpar tabela antes de recarregar
        for item in self.tree_doencas.get_children():
            self.tree_doencas.delete(item)

        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()

        # 1. Atualizar KPIs de Atendimento e Fila Ativa
        cursor.execute("SELECT COUNT(*) FROM pacientes_triados WHERE status='Atendido'")
        self.lbl_kpi_atendidos.configure(text=str(cursor.fetchone()[0]))

        cursor.execute("SELECT COUNT(*) FROM pacientes_triados WHERE status='Aguardando Consulta'")
        self.lbl_kpi_fila.configure(text=str(cursor.fetchone()[0]))

        # 2. Carregar Lista Mapeada de Doenças por Paciente Triado/Atendido
        cursor.execute("""
            SELECT p.nome, p.idade, p.sintomas, c.diagnostico_ia, c.diagnostico_final 
            FROM consultas c
            JOIN pacientes_triados p ON c.paciente_id = p.id
        """)
        
        for linha in cursor.fetchall():
            self.tree_doencas.insert("", "end", values=linha)

        conn.close()

    # --- ABA 2: RECURSOS HUMANOS ---
    def construir_aba_equipa(self):
        ctk.CTkLabel(self.tab_equipa, text="Registar Novo Operador Clínico no Sistema", 
                     font=("Segoe UI", 14, "bold"), text_color="#06B6D4").pack(pady=10)

        self.frame_form = ctk.CTkFrame(self.tab_equipa, fg_color="#0B132B", corner_radius=8)
        self.frame_form.pack(pady=10, padx=20, fill="x")

        self.txt_nome = ctk.CTkEntry(self.frame_form, placeholder_text="Username do Utilizador", width=180)
        self.txt_nome.grid(row=0, column=0, padx=10, pady=15)

        self.txt_senha = ctk.CTkEntry(self.frame_form, placeholder_text="Palavra-passe", show="*", width=140)
        self.txt_senha.grid(row=0, column=1, padx=10, pady=15)

        self.cb_cargo = ctk.CTkComboBox(self.frame_form, values=["ENFERMEIRO", "MEDICO"], width=140, state="readonly")
        self.cb_cargo.set("ENFERMEIRO")
        self.cb_cargo.grid(row=0, column=2, padx=10, pady=15)

        self.btn_add = ctk.CTkButton(self.frame_form, text="＋ Registar Técnico", fg_color="#10B981", hover_color="#059669", command=self.inserir_profissional, width=120)
        self.btn_add.grid(row=0, column=3, padx=10, pady=15)

        # Painel de listagem de utilizadores ativos
        self.tree_user_frame = ctk.CTkFrame(self.tab_equipa)
        self.tree_user_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.tree_users = ttk.Treeview(self.tree_user_frame, columns=("ID", "Nome", "Função"), show="headings")
        self.tree_users.heading("ID", text="ID Interno")
        self.tree_users.heading("Nome", text="Nome de Utilizador")
        self.tree_users.heading("Função", text="Cargo / Nível de Acesso")
        self.tree_users.pack(side="left", fill="both", expand=True)

        self.btn_del = ctk.CTkButton(self.tab_equipa, text="🗑️ Revogar Acesso Técnico", fg_color="#DC2626", hover_color="#991B1B", command=self.deletar_profissional)
        self.btn_del.pack(pady=10)
        
        self.atualizar_tabela_usuarios()

    def atualizar_tabela_usuarios(self):
        for item in self.tree_users.get_children():
            self.tree_users.delete(item)
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, cargo FROM usuarios WHERE cargo != 'ADMIN'")
        for linha in cursor.fetchall():
            self.tree_users.insert("", "end", values=linha)
        conn.close()

    def inserir_profissional(self):
        nome = self.txt_nome.get()
        senha = self.txt_senha.get()
        cargo = self.cb_cargo.get()
        if not nome or not senha:
            messagebox.showwarning("Campos Vazios", "Introduza as credenciais completas para o novo técnico.")
            return

        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (username, senha, cargo) VALUES (?, ?, ?)", (nome, senha, cargo))
            conn.commit()
            messagebox.showinfo("Sucesso", f"Profissional {nome} integrado com sucesso na equipa.")
            self.atualizar_tabela_usuarios()
            self.carregar_dados_dashboard()
            self.txt_nome.delete(0, 'end')
            self.txt_senha.delete(0, 'end')
        except sqlite3.IntegrityError:
            messagebox.showerror("Conflito", "Este nome de utilizador já se encontra registado no posto.")
        finally:
            conn.close()

    def deletar_profissional(self):
        item_selecionado = self.tree_users.selection()
        if not item_selecionado:
            return
        val = self.tree_users.item(item_selecionado)['values']
        
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id=?", (val[0],))
        conn.commit()
        conn.close()
        self.atualizar_tabela_usuarios()