Sistema de Supervisão Clínica e Diagnóstico Preditivo — CYCLUS IA
 
Este sistema é uma aplicação full-stack de engenharia de software hospitalar desenvolvida para otimizar o fluxo de triagem e consulta médica. O sistema integra uma interface gráfica avançada (CustomTkinter) com um motor de Inteligência Artificial agnóstico, otimizado via Busca Bayesiana (Optuna), capaz de sugerir diagnósticos com base em sintomas, mantendo uma salvaguarda ética de suporte à decisão médica.
 
Tecnologias Utilizadas
• Linguagem: Python 3.11+
• Interface Gráfica: CustomTkinter (Modo Escuro Nativo)
• Base de Dados: SQLite3
• Inteligência Artificial & Data Science:
◦ Scikit-Learn (Random Forest, SVC, Naive Bayes, CountVectorizer)
◦ Optuna (Otimização de Hiperparâmetros de Raiz)
◦ Joblib (Serialização de Modelos Preditivos)
◦ Pandas (Processamento de Datasets)
 
Arquitetura de Pastas do Projeto
Estrutura de diretórios e ficheiros do projeto:
 
hospital-cyclus-ia/
├── Healthcare.csv           # Dataset clínico internacional de treino
├── main.py                  # Ponto de entrada da aplicação (Interface/Login)
├── hospital.db              # Base de dados SQLite (Gerada automaticamente)
├── README.md                # Manual de execução
│
└── core/                    # Módulo Central de Inteligência e Lógica
   ├── treino.py            # Pipeline de treino e otimização da IA
   ├── motor_ia.py          # Motor de inferência e tradução clínica
   ├── mapeamento.py        # Diretrizes médicas e recomendações técnicas
   ├── melhor_modelo.pkl    # Classificador treinado (Gerado após treino)
   └── vectorizer.pkl       # Vetorizador de sintomas (Gerado após treino)
 
Guia de Execução do Sistema
Para garantir que o sistema funcione sem congelamentos e com total integridade preditiva, segue rigorosamente a ordem de execução abaixo.
 
Passo 1: Instalar as Dependências do Sistema
Antes de executar o código, garante que tens todas as bibliotecas necessárias instaladas. Abre o terminal na raiz do projeto e executa:
 
pip install customtkinter pandas scikit-learn optuna joblib
 
Passo 2: Executar o Pipeline de Treino da IA (Obrigatório)
Para evitar que a interface gráfica congele à procura do modelo, deves compilar a Inteligência Artificial primeiro. Este script carregará o arquivo Healthcare.csv, executará as iterações do Optuna e guardará os ficheiros de suporte na pasta core/.
 
python core/treino.py
 
Aguarda a conclusão das iterações no terminal. No final, verás a mensagem de sucesso indicando que o melhor_modelo.pkl e o vectorizer.pkl foram gerados com integridade.
 
Passo 3: Inicializar o Sistema Principal
Com a IA devidamente treinada e os ficheiros .pkl criados, podes iniciar a aplicação hospitalar:
 
python main.py
 
Fluxo de Teste Operacional
Para validar o funcionamento completo do ecossistema e capturar os ecrãs para o Relatório Técnico, segue este fluxo:
 
1. Gestão de Utilizadores (ADMIN)
• Faz login com a conta de Administrador.
• Vai à aba de gestão e cria duas contas de teste: uma para o Enfermeiro e outra para o Médico (garante a seleção correta dos cargos).
• Faz Logout.
 
2. Fluxo de Triagem (ENFERMEIRO)
• Faz login com as credenciais do Enfermeiro criadas.
• Introduz os dados de um novo paciente (Nome, Idade, Temperatura Corporal).
• Seleciona os sintomas apresentados (a interface exibirá em Português).
• Grava a triagem para enviar o paciente para a Fila de Espera do consultório.
• Faz Logout.
 
3. Fluxo de Suporte à Decisão (MÉDICO)
• Faz login com as credenciais do Médico.
• Na Fila de Espera, seleciona o paciente triado — os dados clínicos carregarão instantaneamente com os sintomas traduzidos.
• Clica em "Executar Diagnóstico Preditivo (IA)".
• O motor de inferência consumirá o melhor_modelo.pkl e trará a resposta em sub-segundos, exibindo a sugestão da doença em português dentro da caixa de Salvaguarda Ética, preenchendo automaticamente o diagnóstico soberano de forma editável.
• O médico digita a receita e clica em "Concluir Consulta".
 
4. Monitorização Geral (DASHBOARD ADMIN)
• Faz login novamente como Administrador.
• Acede ao Painel de Indicadores e clica em "Atualizar Indicadores e Painel".
• Verás o paciente consultado listado na tabela histórica com os sintomas, a sugestão que a IA deu e o diagnóstico final soberano determinado pelo médico, tudo mapeado em Português.
 
Resolução de Problemas (Troubleshooting)
 
Erro EOFError ou ficheiro corrompido no Terminal:
Acontece se o processo de treino anterior foi interrompido abruptamente. O motor clínico remove estes ficheiros automaticamente, mas se persistir, apaga manualmente os ficheiros melhor_modelo.pkl e vectorizer.pkl de dentro da pasta core/ e executa novamente:
 
python core/treino.py
 
Erro KeyError: 'sintomas' no treino:
O script de treino está blindado para mapear se o CSV utiliza a coluna inglesa Symptom ou a portuguesa sintomas. Garante apenas que o arquivo Healthcare.csv se encontra dentro da pasta core/ junto ao script de treino.
 