import customtkinter as ctk
from database.tabelas import inicializar_base_de_dados
from views.login import TelaLogin
from views.dashboard_admin import DashboardAdmin
from views.tela_triagem import TelaTriagem
from views.tela_consulta import TelaConsulta

class SistemaHospitalarPrincipal(ctk.CTk):
    def __init__(self, usuario_logado):
        super().__init__()
        self.usuario_logado = usuario_logado
        
        self.title(f"Hospital Inteligente - Operador: {usuario_logado.username} ({usuario_logado.cargo})")
        self.geometry("950x650")
        self.configure(fg_color="#0B132B")

        # Layout Split: Menu Lateral Esquerdo e Contentor Central Direito
        self.menu_lateral = ctk.CTkFrame(self, width=200, fg_color="#1C2541", corner_radius=0)
        self.menu_lateral.pack(side="left", fill="y")

        self.container_principal = ctk.CTkFrame(self, fg_color="transparent")
        self.container_principal.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Título da Barra de Menu
        ctk.CTkLabel(self.menu_lateral, text="🏥 Navegação", font=("Segoe UI", 14, "bold"), text_color="#06B6D4").pack(pady=20)

        # Injeção Dinâmica de Funcionalidades baseada em Controle de Acesso (POO)
        menus = self.usuario_logado.obter_menu_permitido()
        self.frames_views = {}

        if "Gerir Profissionais" in menus:
            self.frames_views["Gerir Profissionais"] = DashboardAdmin(self.container_principal, self.usuario_logado)
            ctk.CTkButton(self.menu_lateral, text="Gerir Equipa", fg_color="transparent", text_color="white", hover_color="#0B132B",
                          command=lambda: self.mostrar_aba("Gerir Profissionais")).pack(fill="x", pady=5, padx=10)

        if "Nova Triagem" in menus:
            self.frames_views["Nova Triagem"] = TelaTriagem(self.container_principal, self.usuario_logado)
            ctk.CTkButton(self.menu_lateral, text="Admissão e Triagem", fg_color="transparent", text_color="white", hover_color="#0B132B",
                          command=lambda: self.mostrar_aba("Nova Triagem")).pack(fill="x", pady=5, padx=10)

        if "Painel de Consultas" in menus:
            self.frames_views["Painel de Consultas"] = TelaConsulta(self.container_principal, self.usuario_logado)
            ctk.CTkButton(self.menu_lateral, text="Consultório Médico", fg_color="transparent", text_color="white", hover_color="#0B132B",
                          command=lambda: self.mostrar_aba("Painel de Consultas")).pack(fill="x", pady=5, padx=10)

        # --- BOTÃO SAIR (LOGOUT) ---
        # Label invisível para empurrar o botão para o fundo do menu lateral
        self.spacer = ctk.CTkLabel(self.menu_lateral, text="")
        self.spacer.pack(expand=True, fill="both")

        # Botão de Terminar Sessão estilizado em vermelho suave/alerta
        self.btn_sair = ctk.CTkButton(self.menu_lateral, text="🚪 Terminar Sessão", fg_color="#DC2626", hover_color="#991B1B",
                                      font=("Segoe UI", 12, "bold"), command=self.terminar_sessao)
        self.btn_sair.pack(fill="x", pady=20, padx=15)

        # Carregar primeira vista disponível por padrão
        if self.frames_views:
            primeira_aba = list(self.frames_views.keys())[0]
            self.mostrar_aba(primeira_aba)

    def mostrar_aba(self, nome_aba):
        for f in self.frames_views.values():
            f.pack_forget()
        self.frames_views[nome_aba].pack(fill="both", expand=True)

    def terminar_sessao(self):
        """Fecha o painel atual e reabre a tela de login de forma limpa."""
        self.destroy() # Destrói a janela do painel principal
        
        # Cria e abre uma nova instância da tela de login
        nova_tela_login = TelaLogin(on_login_success=inicializar_system)
        nova_tela_login.mainloop()

def inicializar_system(usuario):
    app_principal = SistemaHospitalarPrincipal(usuario)
    app_principal.mainloop()

if __name__ == "__main__":
    # 1. Montar a Persistência de Dados (Cria arquivo SQLite e Tabelas se vazias)
    inicializar_base_de_dados()
    
    # 2. Abrir e prender fluxo na Tela de Login
    app_login = TelaLogin(on_login_success=inicializar_system)
    app_login.mainloop()