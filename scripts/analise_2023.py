#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise dos dados CARF 2023 para treinamento
"""

import pandas as pd
import numpy as np

def main():
    print("=== ANALISE DOS DADOS CARF 2023 ===")
    
    # Carregar dados de 2023
    df_2023 = pd.read_csv('dados/carf_julgamentos_2023.csv')
    print(f'Dados 2023 carregados: {df_2023.shape}')
    print(f'Colunas: {list(df_2023.columns)}')
    
    # Análise básica
    print(f'\n=== ANALISE BASICA ===')
    print(f'Total de registros: {len(df_2023)}')
    
    # Verificar valores nulos
    print(f'\nValores nulos por coluna:')
    null_counts = df_2023.isnull().sum()
    for col, count in null_counts.items():
        if count > 0:
            print(f'  {col}: {count} ({count/len(df_2023)*100:.1f}%)')
    
    # Análise do resultado_julgamento
    print(f'\nDistribuicao de resultado_julgamento:')
    resultado_counts = df_2023['resultado_julgamento'].value_counts()
    print(resultado_counts)
    
    # Análise da votação
    print(f'\nDistribuicao de votacao:')
    votacao_counts = df_2023['votacao'].value_counts()
    print(votacao_counts)
    
    # Análise do tributo
    print(f'\nDistribuicao de tributo (top 10):')
    tributo_counts = df_2023['tributo'].value_counts().head(10)
    print(tributo_counts)
    
    # Análise da turma
    print(f'\nDistribuicao de turma (top 10):')
    turma_counts = df_2023['turma'].value_counts().head(10)
    print(turma_counts)
    
    # Análise de texto_ementa
    print(f'\n=== ANALISE DE TEXTO_EMENTA ===')
    textos_validos = df_2023['texto_ementa'].notna().sum()
    print(f'Textos de ementa validos: {textos_validos} ({textos_validos/len(df_2023)*100:.1f}%)')
    
    if textos_validos > 0:
        # Tamanho médio dos textos
        tamanhos = df_2023['texto_ementa'].dropna().str.len()
        print(f'Tamanho medio dos textos: {tamanhos.mean():.0f} caracteres')
        print(f'Tamanho minimo: {tamanhos.min()} caracteres')
        print(f'Tamanho maximo: {tamanhos.max()} caracteres')
        
        # Exemplo de texto
        print(f'\nExemplo de texto_ementa:')
        exemplo = df_2023['texto_ementa'].dropna().iloc[0]
        print(f'{str(exemplo)[:200]}...')
    
    # Análise combinada
    print(f'\n=== ANALISE COMBINADA ===')
    df_clean = df_2023.dropna(subset=['resultado_julgamento', 'votacao', 'texto_ementa', 'tributo'])
    print(f'Registros com dados completos: {df_clean.shape[0]}')
    
    if df_clean.shape[0] > 0:
        # Cruzamento resultado x votação
        cruzamento = pd.crosstab(df_clean['resultado_julgamento'], df_clean['votacao'], margins=True)
        print(f'\nCruzamento resultado_julgamento x votacao:')
        print(cruzamento)

if __name__ == "__main__":
    main()
