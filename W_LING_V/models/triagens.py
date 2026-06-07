from abc import ABC, abstractmethod

class TriagemRealidade(ABC):
    def __init__(self, nome: str, idade: int, temperatura: float, sintomas: list):
        self.nome = nome
        self.idade = idade
        self.temperatura = temperatura
        self.sintomas = sintomas
        self.seccao_destino = ""
        self.prioridade = "Normal"
        self.cor = "#10B981"

    @abstractmethod
    def processar_encaminhamento(self) -> None:
        pass

class ProcessadorTriagemUrgente(TriagemRealidade):
    
    def processar_encaminhamento(self) -> None:
        # 1. Validação de Risco Crítico Crónico -> UTI
        if self.temperatura >= 41.0 or "inconsciente" in self.sintomas:
            self.seccao_destino = "UTI (Unidade de Cuidados Intensivos)"
            self.prioridade = "Emergência Absoluta"
            self.cor = "#DC2626"
            return

        # 2. Divisão por Idade (Urgências Infantis vs Adultos)
        if self.idade <= 12:
            if self.temperatura >= 38.5 or "vomito" in self.sintomas:
                self.seccao_destino = "Banco de Urgência Infantil"
                self.prioridade = "Urgente"
                self.cor = "#EAB308"
            else:
                self.seccao_destino = "Pediatria (Consulta Geral)"
                self.prioridade = "Eletivo"
                self.cor = "#10B981"
                
        # 3. Divisão por Natureza do Trauma (Queimados e Acidentes)
        elif "queimadura" in self.sintomas or "fratura" in self.sintomas or "sangramento" in self.sintomas:
            self.seccao_destino = "Queimados e Acidentes"
            self.prioridade = "Muito Urgente"
            self.cor = "#EA580C"
            
        # 4. Padrão Clínica Geral / Adulto
        else:
            self.seccao_destino = "Banco de Urgência Geral"
            if self.temperatura >= 38.0:
                self.prioridade = "Urgente"
                self.cor = "#EAB308"