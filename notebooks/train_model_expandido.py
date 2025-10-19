#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para treinar modelo CARF expandido
Inclui probabilidade de provimento (total, parcial, negação) e tipo de votação
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

def categorizar_provimento(resultado):
    """Categoriza o resultado do julgamento"""
    if pd.isna(resultado):
        return None
    
    resultado_str = str(resultado).lower()
    
    if 'provido' in resultado_str and 'parcial' not in resultado_str and 'negado' not in resultado_str:
        return 'Provido Total'
    elif 'provido' in resultado_str and 'parcial' in resultado_str:
        return 'Provido Parcial'
    elif 'negado' in resultado_str:
        return 'Negado'
    elif 'nao conhecido' in resultado_str or 'não conhecido' in resultado_str:
        return 'Nao Conhecido'
    else:
        return 'Outros'

def criar_target_votacao(votacao, resultado):
    """Cria target para tipo de votação"""
    if pd.isna(votacao) or pd.isna(resultado):
        return None
    
    votacao_str = str(votacao).strip()
    resultado_str = str(resultado).lower()
    
    # Só considerar casos onde houve provimento
    if 'provido' in resultado_str and 'negado' not in resultado_str:
        if votacao_str == 'Unânime':
            return 'Unânime'
        elif votacao_str == 'Maioria':
            return 'Maioria'
        elif votacao_str == 'Qualidade':
            return 'Qualidade'
    
    return None

def main():
    print("Treinando modelo CARF expandido...")
    
    # Carregar dados
    df = pd.read_csv('../dados/carf_julgamentos_2024.csv')
    print(f'Dados carregados: {df.shape}')

    # Limpeza básica
    df_clean = df.dropna(subset=['resultado_julgamento', 'votacao', 'texto_ementa', 'tributo'])
    print(f'Dados após limpeza: {df_clean.shape}')

    # Criar categorias de provimento
    df_clean['categoria_provimento'] = df_clean['resultado_julgamento'].apply(categorizar_provimento)
    
    # Remover casos não conhecidos e outros para o modelo de provimento
    df_provimento = df_clean[df_clean['categoria_provimento'].isin(['Provido Total', 'Provido Parcial', 'Negado'])]
    print(f'Dados para modelo de provimento: {df_provimento.shape}')
    print(f'Distribuição de provimento:')
    print(df_provimento['categoria_provimento'].value_counts())

    # Criar target para votação (apenas casos de provimento)
    df_provimento['target_votacao'] = df_provimento.apply(
        lambda row: criar_target_votacao(row['votacao'], row['resultado_julgamento']), 
        axis=1
    )

    df_votacao = df_provimento.dropna(subset=['target_votacao'])
    print(f'Dados para modelo de votação: {df_votacao.shape}')
    print(f'Distribuição de votação:')
    print(df_votacao['target_votacao'].value_counts())

    # Preparar features para ambos os modelos
    le_tributo = LabelEncoder()
    le_turma = LabelEncoder()

    # Codificar tributo
    tributo_counts = df_provimento['tributo'].value_counts()
    tributos_frequentes = tributo_counts[tributo_counts >= 50].index.tolist()

    df_provimento['tributo_codificado'] = df_provimento['tributo'].apply(
        lambda x: x if x in tributos_frequentes else 'OUTROS'
    )
    df_provimento['tributo_encoded'] = le_tributo.fit_transform(df_provimento['tributo_codificado'])

    # Codificar turma
    df_provimento['turma_simplificada'] = df_provimento['turma'].str.extract(r'(\d+ª)')[0].fillna('OUTROS')
    df_provimento['turma_encoded'] = le_turma.fit_transform(df_provimento['turma_simplificada'])

    # TF-IDF
    df_provimento['texto_ementa_clean'] = df_provimento['texto_ementa'].fillna('').astype(str)
    df_provimento['texto_ementa_clean'] = df_provimento['texto_ementa_clean'].str[:1000]

    tfidf = TfidfVectorizer(
        max_features=1000,
        stop_words=None,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95
    )

    tfidf_matrix = tfidf.fit_transform(df_provimento['texto_ementa_clean'])
    print(f'TF-IDF shape: {tfidf_matrix.shape}')

    # Features categóricas
    features_categoricas = ['tributo_encoded', 'turma_encoded']
    X_categoricas = df_provimento[features_categoricas].values
    X_texto = tfidf_matrix.toarray()
    X_combined = np.hstack([X_categoricas, X_texto])

    # MODELO 1: Provimento (Total, Parcial, Negado)
    print('\n=== TREINANDO MODELO DE PROVIMENTO ===')
    y_provimento = df_provimento['categoria_provimento'].values

    X_train_prov, X_test_prov, y_train_prov, y_test_prov = train_test_split(
        X_combined, y_provimento, test_size=0.2, random_state=42, stratify=y_provimento
    )

    rf_model_provimento = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight='balanced'
    )

    rf_model_provimento.fit(X_train_prov, y_train_prov)
    y_pred_prov = rf_model_provimento.predict(X_test_prov)

    print('Modelo de Provimento - Métricas:')
    print(classification_report(y_test_prov, y_pred_prov))

    # MODELO 2: Votação (Unânime, Maioria, Qualidade) - apenas casos de provimento
    print('\n=== TREINANDO MODELO DE VOTAÇÃO ===')
    
    # Usar os mesmos pré-processadores para consistência
    X_votacao = X_combined[df_provimento['target_votacao'].notna()]
    y_votacao = df_votacao['target_votacao'].values

    X_train_vot, X_test_vot, y_train_vot, y_test_vot = train_test_split(
        X_votacao, y_votacao, test_size=0.2, random_state=42, stratify=y_votacao
    )

    rf_model_votacao = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight='balanced'
    )

    rf_model_votacao.fit(X_train_vot, y_train_vot)
    y_pred_vot = rf_model_votacao.predict(X_test_vot)

    print('Modelo de Votação - Métricas:')
    print(classification_report(y_test_vot, y_pred_vot))

    # Salvar modelos e componentes
    print('\n=== SALVANDO MODELOS ===')
    
    # Salvar modelo de provimento
    joblib.dump(rf_model_provimento, '../modelo_carf_provimento.pkl')
    
    # Salvar modelo de votação
    joblib.dump(rf_model_votacao, '../modelo_carf_votacao.pkl')

    feature_names = features_categoricas + [f'tfidf_{i}' for i in range(tfidf_matrix.shape[1])]

    # Salvar componentes de pré-processamento
    with open('../preprocessors_expandido.pkl', 'wb') as f:
        pickle.dump({
            'le_tributo': le_tributo,
            'le_turma': le_turma,
            'tfidf': tfidf,
            'tributos_frequentes': tributos_frequentes,
            'feature_names': feature_names
        }, f)

    print('Modelos e componentes salvos com sucesso!')
    print('Arquivos criados:')
    print('- modelo_carf_provimento.pkl (modelo de provimento)')
    print('- modelo_carf_votacao.pkl (modelo de votação)')
    print('- preprocessors_expandido.pkl (componentes de pré-processamento)')

if __name__ == "__main__":
    main()
