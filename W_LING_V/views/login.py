import customtkinter as ctk
import sqlite3
from tkinter import messagebox
# Importa as classes corretas do teu modelo de utilizadores
from models.usuarios import Administrador, Enfermeiro, Medico 

class TelaLogin(ctk.CTk):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        
        self.title("Sistema Hospitalar Inteligente - Login")
        self.geometry("400x450")
        self.configure(fg_color="#0B132B")
        self.resizable(False, False)

        # Componentes visuais
        self.lbl_titulo = ctk.CTkLabel(self, text="HOSPITAL INTELIGENTE", font=("Segoe UI", 20, "bold"), text_color="#06B6D4")
        self.lbl_titulo.pack(pady=40)

        self.txt_user = ctk.CTkEntry(self, placeholder_text="Nome de Utilizador", width=260, height=40, fg_color="#1C2541", border_color="#06B6D4")
        self.txt_user.pack(pady=12)

        self.txt_senha = ctk.CTkEntry(self, placeholder_text="Palavra-passe", show="*", width=260, height=40, fg_color="#1C2541", border_color="#06B6D4")
        self.txt_senha.pack(pady=12)

        self.btn_entrar = ctk.CTkButton(self, text="Autenticar no Sistema", command=self.autenticar, width=260, height=45, fg_color="#06B6D4", hover_color="#0D9488", font=("Segoe UI", 13, "bold"))
        self.btn_entrar.pack(pady=30)

    def autenticar(self):
        user = self.txt_user.get()
        senha = self.txt_senha.get()

        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, cargo FROM usuarios WHERE username=? AND senha=?", (user, senha))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            uid, username, cargo = resultado
            
            # --- CORREÇÃO DA INSTANCIAÇÃO POR CARGO ---
            if cargo == "ADMIN":
                obj_usuario = Administrador(uid, username)
            elif cargo == "ENFERMEIRO":
                obj_usuario = Enfermeiro(uid, username) # Instancia a classe especifica de Enfermeiro
            elif cargo == "MEDICO":
                obj_usuario = Medico(uid, username)     # Instancia a classe especifica de Medico
            else:
                messagebox.showerror("Erro de Permissão", "Cargo não reconhecido pelo sistema do posto de saúde.")
                return
            
            self.destroy()
            self.on_login_success(obj_usuario)
        else:
            messagebox.showerror("Erro de Autenticação", "Credenciais de acesso incorretas para o posto de saúde.")