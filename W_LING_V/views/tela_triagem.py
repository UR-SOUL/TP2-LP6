import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from models.triagens import ProcessadorTriagemUrgente

class TelaTriagem(ctk.CTkFrame):
    def __init__(self, master, usuario_logado, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#0B132B")

        # Título Principal com Ícone
        ctk.CTkLabel(self, text="📋 Admissão Unificada & Triagem de Sintomas", 
                     font=("Segoe UI", 18, "bold"), text_color="#06B6D4").pack(pady=15)

        # Ficha de Identificação do Paciente
        self.f_cadastro = ctk.CTkFrame(self, fg_color="#1C2541", corner_radius=10)
        self.f_cadastro.pack(padx=20, pady=10, fill="x")

        self.txt_nome = ctk.CTkEntry(self.f_cadastro, placeholder_text="Nome Completo", width=250, height=35)
        self.txt_nome.grid(row=0, column=0, padx=10, pady=15)

        self.txt_idade = ctk.CTkEntry(self.f_cadastro, placeholder_text="Idade", width=70, height=35)
        self.txt_idade.grid(row=0, column=1, padx=10, pady=15)

        self.txt_doc = ctk.CTkEntry(self.f_cadastro, placeholder_text="Nº Bilhete de Identidade", width=160, height=35)
        self.txt_doc.grid(row=0, column=2, padx=10, pady=15)

        self.txt_temp = ctk.CTkEntry(self.f_cadastro, placeholder_text="Temp. (ºC)", width=90, height=35)
        self.txt_temp.grid(row=0, column=3, padx=10, pady=15)

        # Dicionário de Mapeamento Técnico (Exibição PT -> Gravação EN para a IA)
        self.MAPA_SINTOMAS = {
            "Febre Alta": "fever",
            "Dor nas Costas": "back pain",
            "Falta de Ar (Dispneia)": "shortness of breath",
            "Dor de Garganta": "sore throat",
            "Vómitos": "vomiting",
            "Diarreia": "diarrhea",
            "Insónia Aguda": "insomnia",
            "Perda de Peso Abrupta": "weight loss",
            "Dores Musculares (Mialgia)": "muscle pain",
            "Inchaço (Edema)": "swelling",
            "Perda de Apetite": "appetite loss",
            "Náuseas Constantes": "nausea",
            "Ansiedade / Agitação": "anxiety",
            "Tosse Seca/Produtiva": "cough",
            "Dor Articular (Artrite)": "joint pain",
            "Estado de Inconsciência": "inconsciente",
            "Queimadura Visível": "queimadura"
        }

        # Subtítulo de Sintomas
        ctk.CTkLabel(self, text="Selecione os Sintomas Clínicos Observados:", 
                     font=("Segoe UI", 13, "bold"), text_color="#94A3B8").pack(pady=5)

        # Contentor com Scroll e Design Limpo para os Sintomas
        self.scroll_sintomas = ctk.CTkScrollableFrame(self, fg_color="#1C2541", height=220, corner_radius=10)
        self.scroll_sintomas.pack(padx=20, pady=5, fill="both", expand=True)

        self.check_vars = {}
        
        # Grid Estética Automatizada (Distribuição Simétrica em 3 Colunas)
        for idx, sintoma_pt in enumerate(self.MAPA_SINTOMAS.keys()):
            var = ctk.StringVar(value="off")
            cb = ctk.CTkCheckBox(self.scroll_sintomas, text=sintoma_pt, variable=var, 
                                 onvalue=sintoma_pt, offvalue="off", 
                                 text_color="white", font=("Segoe UI", 12),
                                 border_color="#06B6D4", hover_color="#0D9488")
            
            row_idx = idx // 3
            col_idx = idx % 3
            cb.grid(row=row_idx, column=col_idx, padx=25, pady=10, sticky="w")
            self.check_vars[sintoma_pt] = var

        # Botão de Ação Principal
        self.btn_salvar = ctk.CTkButton(self, text="Processar Triagem e Encaminhar Paciente", 
                                        fg_color="#06B6D4", hover_color="#0D9488",
                                        font=("Segoe UI", 14, "bold"), command=self.gravar_triagem, height=45)
        self.btn_salvar.pack(pady=20)

    def gravar_triagem(self):
        nome = self.txt_nome.get()
        idade_str = self.txt_idade.get()
        doc = self.txt_doc.get()
        temp_str = self.txt_temp.get()

        # Captura em PT e converte imediatamente para EN para manter compatibilidade com o arquivo CSV da IA
        sintomas_pt = [v.get() for k, v in self.check_vars.items() if v.get() != "off"]
        sintomas_en = [self.MAPA_SINTOMAS[s] for s in sintomas_pt]

        if not nome or not idade_str or not temp_str or not sintomas_en:
            messagebox.showwarning("Campos Requeridos", "Por favor preencha os dados de identificação e selecione os sintomas.")
            return

        try:
            idade = int(idade_str)
            temperatura = float(temp_str)
        except ValueError:
            messagebox.showerror("Erro de Digitação", "A idade e a temperatura devem ser valores numéricos válidos.")
            return

        # Executa a Lógica de Negócio de Triagem Urgente
        processador = ProcessadorTriagemUrgente(nome, idade, temperatura, sintomas_en)
        processador.processar_encaminhamento()

        # Salva as duas versões na BD: sintomas_pt (para visualização humana) e sintomas_en (para o motor de IA)
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pacientes_triados (nome, idade, documento, temperatura, sintomas, seccao_encaminhada, nivel_urgencia, cor_protocolo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (nome, idade, doc, temperatura, ", ".join(sintomas_en), processador.seccao_destino, processador.prioridade, processador.cor))
        
        conn.commit()
        conn.close()

        messagebox.showinfo("Admissão Concluída", f"Paciente: {nome}\nDirecionado para: {processador.seccao_destino}\nPrioridade: {processador.prioridade}")
        
        # Reset Estético dos Campos
        self.txt_nome.delete(0, 'end')
        self.txt_idade.delete(0, 'end')
        self.txt_doc.delete(0, 'end')
        self.txt_temp.delete(0, 'end')
        for v in self.check_vars.values():
            v.set("off")