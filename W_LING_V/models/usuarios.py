class Usuario:
    def __init__(self, user_id, username, cargo):
        self._user_id = user_id
        self.username = username
        self.cargo = cargo

    def obter_menu_permitido(self):
        """Método abstrato/base que será sobrescrito pelas subclasses."""
        return []


class Administrador(Usuario):
    def __init__(self, user_id, username):
        # Admin não precisa receber o cargo por fora, ele já se auto-define como ADMIN
        super().__init__(user_id, username, "ADMIN")

    def obter_menu_permitido(self):
        # O Administrador gere os recursos humanos do hospital
        return ["Gerir Profissionais"]


class Enfermeiro(Usuario):
    def __init__(self, user_id, username):
        super().__init__(user_id, username, "ENFERMEIRO")

    def obter_menu_permitido(self):
        # O Enfermeiro opera a admissão e os protocolos de triagem
        return ["Nova Triagem"]


class Medico(Usuario):
    def __init__(self, user_id, username):
        super().__init__(user_id, username, "MEDICO")

    def obter_menu_permitido(self):
        # O Médico opera o consultório e a análise clínica/IA
        return ["Painel de Consultas"]