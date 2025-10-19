#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para treinar o modelo CARF
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import pickle
import warnings
warnings.filterwarnings('ignore')

def main():
    print("Treinando modelo CARF...")
    
    # Carregar dados
    df = pd.read_csv('../dados/carf_julgamentos_2024.csv')
    print(f'Dados carregados: {df.shape}')

    # Limpeza básica
    df_clean = df.dropna(subset=['resultado_julgamento', 'votacao', 'texto_ementa', 'tributo'])
    print(f'Dados após limpeza: {df_clean.shape}')

    # Criar target para votação
    def criar_target_votacao(votacao, resultado):
        if pd.isna(votacao) or pd.isna(resultado):
            return None
        votacao_str = str(votacao).strip()
        resultado_str = str(resultado).lower()
        if 'provido' in resultado_str and 'negado' not in resultado_str:
            if votacao_str == 'Unânime':
                return 'Unânime'
            elif votacao_str == 'Maioria':
                return 'Maioria'
            elif votacao_str == 'Qualidade':
                return 'Qualidade'
        return None

    df_clean['target_votacao'] = df_clean.apply(
        lambda row: criar_target_votacao(row['votacao'], row['resultado_julgamento']), 
        axis=1
    )

    df_votacao = df_clean.dropna(subset=['target_votacao'])
    print(f'Dados para modelo: {df_votacao.shape}')
    print(f'Distribuição: {df_votacao["target_votacao"].value_counts()}')

    # Preparar features
    le_tributo = LabelEncoder()
    le_turma = LabelEncoder()

    tributo_counts = df_votacao['tributo'].value_counts()
    tributos_frequentes = tributo_counts[tributo_counts >= 50].index.tolist()

    df_votacao['tributo_codificado'] = df_votacao['tributo'].apply(
        lambda x: x if x in tributos_frequentes else 'OUTROS'
    )
    df_votacao['tributo_encoded'] = le_tributo.fit_transform(df_votacao['tributo_codificado'])

    df_votacao['turma_simplificada'] = df_votacao['turma'].str.extract(r'(\d+ª)')[0].fillna('OUTROS')
    df_votacao['turma_encoded'] = le_turma.fit_transform(df_votacao['turma_simplificada'])

    # TF-IDF
    df_votacao['texto_ementa_clean'] = df_votacao['texto_ementa'].fillna('').astype(str)
    df_votacao['texto_ementa_clean'] = df_votacao['texto_ementa_clean'].str[:1000]

    tfidf = TfidfVectorizer(
        max_features=1000,
        stop_words=None,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95
    )

    tfidf_matrix = tfidf.fit_transform(df_votacao['texto_ementa_clean'])
    print(f'TF-IDF shape: {tfidf_matrix.shape}')

    # Combinar features
    features_categoricas = ['tributo_encoded', 'turma_encoded']
    X_categoricas = df_votacao[features_categoricas].values
    X_texto = tfidf_matrix.toarray()
    X_combined = np.hstack([X_categoricas, X_texto])

    y = df_votacao['target_votacao'].values

    # Treinar modelo
    X_train, X_test, y_train, y_test = train_test_split(
        X_combined, y, test_size=0.2, random_state=42, stratify=y
    )

    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight='balanced'
    )

    rf_model.fit(X_train, y_train)
    y_pred = rf_model.predict(X_test)

    print('Modelo treinado!')
    print(classification_report(y_test, y_pred))

    # Salvar modelo
    joblib.dump(rf_model, '../modelo_carf_rf.pkl')

    feature_names = features_categoricas + [f'tfidf_{i}' for i in range(tfidf_matrix.shape[1])]

    with open('../preprocessors.pkl', 'wb') as f:
        pickle.dump({
            'le_tributo': le_tributo,
            'le_turma': le_turma,
            'tfidf': tfidf,
            'tributos_frequentes': tributos_frequentes,
            'feature_names': feature_names
        }, f)

    print('Modelo e componentes salvos com sucesso!')

if __name__ == "__main__":
    main()
