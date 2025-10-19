#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para treinar modelo CARF usando dados de 2023 (treinamento) e 2024 (teste)
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
        elif votacao_str == 'Empate - Lei 13.988/2020':
            return 'Empate'
    
    return None

def main():
    print("Treinando modelo CARF com dados 2023 (treinamento) e 2024 (teste)...")
    
    # Carregar dados de treinamento (2023)
    df_train = pd.read_csv('../dados/carf_2023_sem_vazamento.csv')
    print(f'Dados de treinamento 2023: {df_train.shape}')
    
    # Carregar dados de teste (2024)
    df_test = pd.read_csv('../dados/carf_sem_vazamento.csv')
    print(f'Dados de teste 2024: {df_test.shape}')
    
    # Limpeza básica dos dados de treinamento
    df_train_clean = df_train.dropna(subset=['resultado_julgamento', 'votacao', 'texto_ementa', 'tributo'])
    print(f'Dados de treinamento após limpeza: {df_train_clean.shape}')
    
    # Limpeza básica dos dados de teste
    df_test_clean = df_test.dropna(subset=['resultado_julgamento', 'votacao', 'texto_ementa', 'tributo'])
    print(f'Dados de teste após limpeza: {df_test_clean.shape}')
    
    # Criar categorias de provimento para treinamento
    df_train_clean['categoria_provimento'] = df_train_clean['resultado_julgamento'].apply(categorizar_provimento)
    
    # Remover casos não conhecidos e outros para o modelo de provimento
    df_train_provimento = df_train_clean[df_train_clean['categoria_provimento'].isin(['Provido Total', 'Provido Parcial', 'Negado'])]
    print(f'Dados para modelo de provimento (treinamento): {df_train_provimento.shape}')
    print(f'Distribuição de provimento (treinamento):')
    print(df_train_provimento['categoria_provimento'].value_counts())
    
    # Criar target para votação (apenas casos de provimento)
    df_train_provimento['target_votacao'] = df_train_provimento.apply(
        lambda row: criar_target_votacao(row['votacao'], row['resultado_julgamento']), 
        axis=1
    )
    
    df_train_votacao = df_train_provimento.dropna(subset=['target_votacao'])
    print(f'Dados para modelo de votação (treinamento): {df_train_votacao.shape}')
    print(f'Distribuição de votação (treinamento):')
    print(df_train_votacao['target_votacao'].value_counts())
    
    # Preparar features para ambos os modelos
    le_tributo = LabelEncoder()
    le_turma = LabelEncoder()
    
    # Codificar tributo
    tributo_counts = df_train_provimento['tributo'].value_counts()
    tributos_frequentes = tributo_counts[tributo_counts >= 30].index.tolist()  # Reduzido para 2023
    
    df_train_provimento['tributo_codificado'] = df_train_provimento['tributo'].apply(
        lambda x: x if x in tributos_frequentes else 'OUTROS'
    )
    df_train_provimento['tributo_encoded'] = le_tributo.fit_transform(df_train_provimento['tributo_codificado'])
    
    # Codificar turma
    df_train_provimento['turma_simplificada'] = df_train_provimento['turma'].str.extract(r'(\d+ª)')[0].fillna('OUTROS')
    df_train_provimento['turma_encoded'] = le_turma.fit_transform(df_train_provimento['turma_simplificada'])
    
    # TF-IDF
    df_train_provimento['texto_ementa_clean'] = df_train_provimento['texto_ementa'].fillna('').astype(str)
    df_train_provimento['texto_ementa_clean'] = df_train_provimento['texto_ementa_clean'].str[:1000]
    
    tfidf = TfidfVectorizer(
        max_features=1000,
        stop_words=None,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95
    )
    
    tfidf_matrix = tfidf.fit_transform(df_train_provimento['texto_ementa_clean'])
    print(f'TF-IDF shape (treinamento): {tfidf_matrix.shape}')
    
    # Features categóricas
    features_categoricas = ['tributo_encoded', 'turma_encoded']
    X_categoricas = df_train_provimento[features_categoricas].values
    X_texto = tfidf_matrix.toarray()
    X_combined = np.hstack([X_categoricas, X_texto])
    
    # MODELO 1: Provimento (Total, Parcial, Negado)
    print('\n=== TREINANDO MODELO DE PROVIMENTO ===')
    y_provimento = df_train_provimento['categoria_provimento'].values
    
    rf_model_provimento = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight='balanced'
    )
    
    rf_model_provimento.fit(X_combined, y_provimento)
    print('Modelo de Provimento treinado!')
    
    # MODELO 2: Votação (Unânime, Maioria, Qualidade, Empate) - apenas casos de provimento
    print('\n=== TREINANDO MODELO DE VOTAÇÃO ===')
    
    X_votacao = X_combined[df_train_provimento['target_votacao'].notna()]
    y_votacao = df_train_votacao['target_votacao'].values
    
    rf_model_votacao = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight='balanced'
    )
    
    rf_model_votacao.fit(X_votacao, y_votacao)
    print('Modelo de Votação treinado!')
    
    # TESTE COM DADOS DE 2024
    print('\n=== TESTANDO COM DADOS DE 2024 ===')
    
    # Preparar dados de teste
    df_test_clean['categoria_provimento'] = df_test_clean['resultado_julgamento'].apply(categorizar_provimento)
    df_test_provimento = df_test_clean[df_test_clean['categoria_provimento'].isin(['Provido Total', 'Provido Parcial', 'Negado'])]
    
    # Aplicar mesmas transformações
    df_test_provimento['tributo_codificado'] = df_test_provimento['tributo'].apply(
        lambda x: x if x in tributos_frequentes else 'OUTROS'
    )
    df_test_provimento['tributo_encoded'] = le_tributo.transform(df_test_provimento['tributo_codificado'])
    
    df_test_provimento['turma_simplificada'] = df_test_provimento['turma'].str.extract(r'(\d+ª)')[0].fillna('OUTROS')
    df_test_provimento['turma_encoded'] = le_turma.transform(df_test_provimento['turma_simplificada'])
    
    df_test_provimento['texto_ementa_clean'] = df_test_provimento['texto_ementa'].fillna('').astype(str)
    df_test_provimento['texto_ementa_clean'] = df_test_provimento['texto_ementa_clean'].str[:1000]
    
    # TF-IDF para teste
    X_test_categoricas = df_test_provimento[features_categoricas].values
    X_test_texto = tfidf.transform(df_test_provimento['texto_ementa_clean']).toarray()
    X_test_combined = np.hstack([X_test_categoricas, X_test_texto])
    
    # Predições de provimento
    y_test_provimento = df_test_provimento['categoria_provimento'].values
    y_pred_provimento = rf_model_provimento.predict(X_test_combined)
    
    print('Modelo de Provimento - Métricas no teste 2024:')
    print(classification_report(y_test_provimento, y_pred_provimento))
    
    # Predições de votação
    df_test_provimento['target_votacao'] = df_test_provimento.apply(
        lambda row: criar_target_votacao(row['votacao'], row['resultado_julgamento']), 
        axis=1
    )
    df_test_votacao = df_test_provimento.dropna(subset=['target_votacao'])
    
    if len(df_test_votacao) > 0:
        X_test_votacao = X_test_combined[df_test_provimento['target_votacao'].notna()]
        y_test_votacao = df_test_votacao['target_votacao'].values
        y_pred_votacao = rf_model_votacao.predict(X_test_votacao)
        
        print('Modelo de Votação - Métricas no teste 2024:')
        print(classification_report(y_test_votacao, y_pred_votacao))
    
    # Salvar modelos e componentes
    print('\n=== SALVANDO MODELOS ===')
    
    # Salvar modelo de provimento
    joblib.dump(rf_model_provimento, '../modelo_carf_provimento_2023.pkl')
    
    # Salvar modelo de votação
    joblib.dump(rf_model_votacao, '../modelo_carf_votacao_2023.pkl')
    
    feature_names = features_categoricas + [f'tfidf_{i}' for i in range(tfidf_matrix.shape[1])]
    
    # Salvar componentes de pré-processamento
    with open('../preprocessors_2023.pkl', 'wb') as f:
        pickle.dump({
            'le_tributo': le_tributo,
            'le_turma': le_turma,
            'tfidf': tfidf,
            'tributos_frequentes': tributos_frequentes,
            'feature_names': feature_names
        }, f)
    
    print('Modelos e componentes salvos com sucesso!')
    print('Arquivos criados:')
    print('- modelo_carf_provimento_2023.pkl (modelo de provimento)')
    print('- modelo_carf_votacao_2023.pkl (modelo de votação)')
    print('- preprocessors_2023.pkl (componentes de pré-processamento)')
    
    print('\n=== RESUMO FINAL ===')
    print(f'Dados de treinamento (2023): {len(df_train_provimento)} registros')
    print(f'Dados de teste (2024): {len(df_test_provimento)} registros')
    print(f'Modelos treinados e testados com sucesso!')

if __name__ == "__main__":
    main()
