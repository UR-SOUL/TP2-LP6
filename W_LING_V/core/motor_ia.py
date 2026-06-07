import os
import pandas as pd
import numpy as np
import optuna
import joblib  # Biblioteca para salvar e carregar modelos binários
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import CountVectorizer

class MotorIAHospitalar:
    def __init__(self, nome_csv="Healthcare.csv"):
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        self.csv_path = os.path.join(diretorio_atual, nome_csv)
        
        # Caminhos onde o modelo e o vetorizador serão salvos fisicamente
        self.modelo_path = os.path.join(diretorio_atual, "melhor_modelo.pkl")
        self.vectorizer_path = os.path.join(diretorio_atual, "vectorizer.pkl")
        
        self.vectorizer = CountVectorizer(tokenizer=lambda x: [s.strip() for s in x.split(',')])
        self.modelo_otimizado = None
        self.classes = []

        # Tenta carregar o modelo automaticamente se ele já foi treinado antes
        self.carregar_modelo_treinado()

    def preparar_dados(self):
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"Dataset não encontrado em: {self.csv_path}")
        
        df = pd.read_csv(self.csv_path)
        X = self.vectorizer.fit_transform(df['Symptoms']).toarray()
        y = df['Disease'].values
        self.classes = list(np.unique(y))
        return X, y

    def _objective(self, trial, X, y):
        classifier_name = trial.suggest_categorical("classifier", ["RandomForest", "SVC", "NaiveBayes"])
        
        if classifier_name == "RandomForest":
            n_estimators = trial.suggest_int("rf_n_estimators", 10, 50)
            max_depth = trial.suggest_int("rf_max_depth", 2, 10)
            model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
        elif classifier_name == "SVC":
            c_param = trial.suggest_float("svc_c", 0.1, 5.0, log=True)
            model = SVC(C=c_param, kernel='linear', random_state=42)
        else:
            model = GaussianNB()

        return cross_val_score(model, X, y, n_jobs=-1, cv=3).mean()

    def executar_otimizacao(self, n_trials=5):
        """Roda o Optuna, treina o melhor modelo e guarda-o no disco."""
        X, y = self.preparar_dados()
        optuna.logging.set_verbosity(optuna.logging.WARNING)
        study = optuna.create_study(direction="maximize")
        study.optimize(lambda trial: self._objective(trial, X, y), n_trials=n_trials)
        
        melhores_params = study.best_params
        if melhores_params.get("classifier") == "RandomForest":
            self.modelo_otimizado = RandomForestClassifier(
                n_estimators=melhores_params["rf_n_estimators"],
                max_depth=melhores_params["rf_max_depth"],
                random_state=42
            )
        elif melhores_params.get("classifier") == "SVC":
            self.modelo_otimizado = SVC(C=melhores_params["svc_c"], kernel='linear', random_state=42)
        else:
            self.modelo_otimizado = GaussianNB()
            
        self.modelo_otimizado.fit(X, y)
        
        # SALVAGUARDA FÍSICA NO DISCO
        joblib.dump(self.modelo_otimizado, self.modelo_path)
        joblib.dump(self.vectorizer, self.vectorizer_path)
        print("[IA] Treino concluído com sucesso. Modelo guardado no disco!")
        
        return study.best_value, study.best_trial.params

    def carregar_modelo_treinado(self):
        """Verifica se existem ficheiros guardados e carrega-os na RAM."""
        if os.path.exists(self.modelo_path) and os.path.exists(self.vectorizer_path):
            self.modelo_otimizado = joblib.load(self.modelo_path)
            self.vectorizer = joblib.load(self.vectorizer_path)
            print("[IA] Modelo e Vetorizador carregados do disco com sucesso (Previsão Instantânea Ativa).")
            return True
        return False

    def prever_doenca(self, lista_sintomas):
        if self.modelo_otimizado is None:
            # Se o utilizador nunca treinou o modelo, força o treino rápido
            print("[IA] Aviso: Nenhum modelo encontrado no disco. Iniciando treino automático...")
            self.executar_otimizacao(n_trials=3)
            
        string_sintomas = ", ".join(lista_sintomas)
        X_input = self.vectorizer.transform([string_sintomas]).toarray()
        predicao = self.modelo_otimizado.predict(X_input)
        return str(predicao[0])