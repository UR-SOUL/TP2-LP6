import customtkinter as ctk
import sqlite3
from tkinter import messagebox, ttk
from core.motor_ia import MotorIAHospitalar
from core.mapeamento import traduzir_e_recomendar

class TelaConsulta(ctk.CTkFrame):
    def __init__(self, master, usuario_logado, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#0B132B")
        self.usuario_logado = usuario_logado
        self.motor_ia = MotorIAHospitalar()
        self.paciente_selecionado_id = None
     

        ctk.CTkLabel(self, text="Painel Clínico de Consultas Médicas", font=("Segoe UI", 18, "bold"), text_color="#06B6D4").pack(pady=10)

        # Divisão da Tela: Esquerda (Fila de Espera) | Direita (Prontuário de Atendimento)
        self.pane = ctk.CTkFrame(self, fg_color="transparent")
        self.pane.pack(fill="both", expand=True, padx=10, pady=5)

        # Lado Esquerdo - Fila
        self.f_esquerda = ctk.CTkFrame(self.pane, width=200, fg_color="#1C2541")
        self.f_esquerda.pack(side="left", fill="both", padx=5, pady=5)
        
        ctk.CTkLabel(self.f_esquerda, text="Fila de Espera", font=("Segoe UI", 12, "bold")).pack(pady=5)
        self.tree_fila = ttk.Treeview(self.f_esquerda, columns=("ID", "Nome"), show="headings", height=12)
        self.tree_fila.heading("ID", text="ID")
        self.tree_fila.heading("Nome", text="Paciente")
        self.tree_fila.column("ID", width=30)
        self.tree_fila.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree_fila.bind("<<TreeviewSelect>>", self.carregar_prontuario_paciente)

        # Lado Direito - Atendimento
        self.f_direita = ctk.CTkFrame(self.pane, fg_color="#1C2541")
        self.f_direita.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        self.lbl_nome_paciente = ctk.CTkLabel(self.f_direita, text="Nenhum paciente selecionado", font=("Segoe UI", 14, "bold"), text_color="#06B6D4")
        self.lbl_nome_paciente.pack(pady=10)

        self.lbl_detalhes_clinicos = ctk.CTkLabel(self.f_direita, text="Sinais Vitais / Queixas: ", font=("Segoe UI", 11), justify="left")
        self.lbl_detalhes_clinicos.pack(anchor="w", padx=15, pady=5)

        # Botão Inteligência Artificial
        self.btn_ia = ctk.CTkButton(self.f_direita, text="Executar Diagnóstico Preditivo (IA)", fg_color="#0D9488", command=self.chamar_ia, state="disabled")
        self.btn_ia.pack(pady=10)

        # Caixa de Alerta de Salvaguarda Ética
        self.f_alerta = ctk.CTkFrame(self.f_direita, fg_color="#0B132B", border_width=1, border_color="#D97706")
        self.lbl_alerta_titulo = ctk.CTkLabel(self.f_alerta, text="⚠️ SALVAGUARDA ÉTICA MÉDICA (NÃO AUTOMEDICAÇÃO):", font=("Segoe UI", 10, "bold"), text_color="#D97706")
        self.lbl_alerta_corpo = ctk.CTkLabel(self.f_alerta, text="Aguardando inferência da IA...", font=("Segoe UI", 11, "italic"), wraplength=400)

        # Campos de texto livre do médico
        self.txt_diagnostico_final = ctk.CTkEntry(self.f_direita, placeholder_text="Diagnóstico Clínico Soberano Final", width=400)
        self.txt_diagnostico_final.pack(pady=5)
        
        self.txt_receita = ctk.CTkEntry(self.f_direita, placeholder_text="Prescrição de Medicamentos / Exames adicionais", width=400)
        self.txt_receita.pack(pady=5)

        self.btn_concluir = ctk.CTkButton(self.f_direita, text="Concluir Consulta e Atualizar Prontuário", fg_color="#10B981", command=self.concluir_consulta, state="disabled")
        self.btn_concluir.pack(pady=15)

        self.atualizar_fila()

    def atualizar_fila(self):
        for item in self.tree_fila.get_children():
            self.tree_fila.delete(item)
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM pacientes_triados WHERE status = 'Aguardando Consulta'")
        for linha in cursor.fetchall():
            self.tree_fila.insert("", "end", values=linha)
        conn.close()

    def carregar_prontuario_paciente(self, event):
        item = self.tree_fila.selection()
        if not item: return
        self.paciente_selecionado_id = self.tree_fila.item(item)['values'][0]

        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nome, idade, temperatura, sintomas, seccao_encaminhada FROM pacientes_triados WHERE id=?", (self.paciente_selecionado_id,))
        self.dados_paciente = cursor.fetchone()
        conn.close()

        nome, idade, temp, sintomas, seccao = self.dados_paciente
        self.lbl_nome_paciente.configure(text=f"Prontuário: {nome} ({idade} Anos)")
        self.lbl_detalhes_clinicos.configure(text=f"Triado para: {seccao} | Temp: {temp}ºC\nSintomas Relatados: {sintomas}")
        
        self.btn_ia.configure(state="normal")
        self.btn_concluir.configure(state="normal")

    def chamar_ia(self):
        sintomas_lista = [s.strip() for s in self.dados_paciente[3].split(',')]
        
        # Executa inferência do classificador otimizado
        predicao_en = self.motor_ia.prever_doenca(sintomas_lista)
        nome_pt, diretriz = traduzir_e_recomendar(predicao_en)

        self.f_alerta.pack(pady=10, fill="x", padx=20)
        self.lbl_alerta_titulo.pack(anchor="w", padx=10, pady=2)
        self.lbl_alerta_corpo.configure(text=f"A IA sugere quadro compatível com: {nome_pt}.\nDiretriz: {diretriz}")
        self.lbl_alerta_corpo.pack(anchor="w", padx=10, pady=5)
        
        self.txt_diagnostico_final.delete(0, 'end')
        self.txt_diagnostico_final.insert(0, nome_pt) # Preenche como sugestão editável

    def concluir_consulta(self):
        diag = self.txt_diagnostico_final.get()
        meds = self.txt_receita.get()
        if not diag: return

        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        # Salva o atendimento na tabela de consultas
        cursor.execute("""
            INSERT INTO consultas (paciente_id, medico_id, diagnostico_ia, diagnostico_final, medicamentos)
            VALUES (?, ?, ?, ?, ?)
        """, (self.paciente_selecionado_id, self.usuario_logado._user_id, self.txt_diagnostico_final.get(), diag, meds))
        
        # Altera status para retirá-lo da Fila do Posto
        cursor.execute("UPDATE pacientes_triados SET status='Atendido' WHERE id=?", (self.paciente_selecionado_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Consulta arquivada com sucesso no histórico eletrónico.")
        self.f_alerta.pack_forget()
        self.txt_diagnostico_final.delete(0, 'end')
        self.txt_receita.delete(0, 'end')
        self.lbl_nome_paciente.configure(text="Nenhum paciente selecionado")
        self.atualizar_fila()