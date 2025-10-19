#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise dos tipos de provimento nos dados CARF
"""

import pandas as pd
import numpy as np

def main():
    # Carregar dados
    df = pd.read_csv('dados/carf_julgamentos_2024.csv')

    print('=== ANALISE DOS TIPOS DE PROVIMENTO ===')
    print(f'Total de registros: {df.shape[0]}')

    # Análise do resultado_julgamento
    print(f'\nDistribuicao de resultado_julgamento:')
    resultado_counts = df['resultado_julgamento'].value_counts()
    print(resultado_counts)

    # Criar categorias de provimento
    def categorizar_provimento(resultado):
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

    df['categoria_provimento'] = df['resultado_julgamento'].apply(categorizar_provimento)

    print(f'\nDistribuicao de categoria_provimento:')
    categoria_counts = df['categoria_provimento'].value_counts()
    print(categoria_counts)

    # Análise da votação
    print(f'\nDistribuicao de votacao:')
    votacao_counts = df['votacao'].value_counts()
    print(votacao_counts)

    # Análise combinada
    print(f'\n=== ANALISE COMBINADA ===')
    df_clean = df.dropna(subset=['resultado_julgamento', 'votacao'])
    print(f'Registros com dados completos: {df_clean.shape[0]}')

    # Cruzamento categoria_provimento x votacao
    cruzamento = pd.crosstab(df_clean['categoria_provimento'], df_clean['votacao'], margins=True)
    print(f'\nCruzamento categoria_provimento x votacao:')
    print(cruzamento)

    # Análise específica para casos de provimento
    df_provimento = df_clean[df_clean['categoria_provimento'].isin(['Provido Total', 'Provido Parcial'])]
    print(f'\n=== CASOS DE PROVIMENTO ===')
    print(f'Total de casos de provimento: {df_provimento.shape[0]}')
    
    if df_provimento.shape[0] > 0:
        print(f'\nDistribuicao por tipo de provimento:')
        print(df_provimento['categoria_provimento'].value_counts())
        
        print(f'\nDistribuicao por votacao (apenas provimentos):')
        print(df_provimento['votacao'].value_counts())
        
        # Cruzamento para casos de provimento
        cruzamento_provimento = pd.crosstab(df_provimento['categoria_provimento'], df_provimento['votacao'], margins=True)
        print(f'\nCruzamento categoria_provimento x votacao (apenas provimentos):')
        print(cruzamento_provimento)

if __name__ == "__main__":
    main()
