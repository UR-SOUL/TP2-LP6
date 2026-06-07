DICIONARIO_DOENCAS = {
    "Allergy": ("Alergia Aguda", "Manter monitoramento de choque anafilático. Isolar alérgenos de contacto."),
    "Thyroid Disorder": ("Distúrbio da Tiróide", "Encaminhar para painel hormonal. Evitar medicação hormonal empírica."),
    "Influenza": ("Gripe / Influenza", "Incentivar hidratação. Evitar antipiréticos sem triagem hepática prévia."),
    "Stroke": ("Acidente Vascular Cerebral (AVC)", "TRANSFERÊNCIA IMEDIATA para Emergência Crítica. Monitorar sinais vitais de 5 em 5 min."),
    "Heart Disease": ("Cardiopatia / Insuficiência Cardíaca", "Repouso absoluto no leito, monitorar saturação de O2. Administrar oxigénio se necessário."),
    "Food Poisoning": ("Intoxicação Alimentar", "Iniciar plano de reidratação oral imediato. Coletar dados de ingestão alimentar recente."),
    "Bronchitis": ("Bronquite Aguda", "Nebulização de resgate disponível sob supervisão médica. Monitorar padrão respiratório."),
    "COVID-19": ("Suspeita de COVID-19", "Isolamento respiratório imediato no posto. Uso obrigatório de máscara cirúrgica."),
    "Dermatitis": ("Dermatite", "Evitar aplicação de corticoides tópicos antes da inspeção do médico especialista."),
    "Diabetes": ("Descompensação Glicémica", "Realizar glicemia capilar imediatamente. Não administrar insulina sem prescrição."),
    "Arthritis": ("Artrite Reumatóide", "Repouso articular temporário, aplicação de compressas consoante indicação.")
}

def traduzir_e_recomendar(doenca_en):
    return DICIONARIO_DOENCAS.get(doenca_en, (f"Patologia ({doenca_en})", "Aguardar protocolo terapêutico exclusivo prescrito pelo médico."))