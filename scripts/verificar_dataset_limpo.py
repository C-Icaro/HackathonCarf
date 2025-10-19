#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar se o dataset limpo está correto
"""

import pandas as pd

def main():
    print("=== VERIFICACAO DO DATASET LIMPO ===")
    
    # Verificar o dataset limpo
    df_limpo = pd.read_csv('dados/carf_sem_vazamento.csv')
    print(f'Dataset limpo carregado: {df_limpo.shape}')
    print(f'Colunas: {list(df_limpo.columns)}')
    
    # Verificar se não há mais palavras de vazamento
    palavras_vazamento = [
        'provido', 'negado', 'mantém-se', 'mantem-se', 'improcedente', 'procedente',
        'dar provimento', 'nega-se', 'recurso conhecido', 'decide-se', 'não se conhece',
        'voto de qualidade', 'unânime', 'maioria', 'qualidade', 'acordam os membros',
        'por unanimidade', 'por maioria', 'votaram', 'conclusões', 'julgamento',
        'decisão', 'acórdão', 'sentença', 'resultado', 'provimento', 'negação'
    ]
    
    def verificar_vazamento(texto):
        if pd.isna(texto):
            return False
        texto_lower = str(texto).lower()
        for palavra in palavras_vazamento:
            if palavra in texto_lower:
                return True
        return False
    
    # Verificar se ainda há vazamento
    df_limpo['tem_vazamento'] = df_limpo['texto_ementa'].apply(verificar_vazamento)
    vazamento_restante = df_limpo['tem_vazamento'].sum()
    
    print(f'Registros com vazamento restante: {vazamento_restante}')
    print(f'Percentual de vazamento restante: {(vazamento_restante/len(df_limpo))*100:.2f}%')
    
    if vazamento_restante > 0:
        print('\nExemplos de vazamento restante:')
        exemplos = df_limpo[df_limpo['tem_vazamento'] == True].head(3)
        for i, row in exemplos.iterrows():
            print(f'Registro {i}: {str(row["texto_ementa"])[:100]}...')
    else:
        print('\nDataset limpo sem vazamento detectado!')
    
    # Mostrar distribuição dos resultados
    print('\n=== DISTRIBUICAO DOS RESULTADOS ===')
    print('Resultados no dataset limpo:')
    print(df_limpo['resultado_julgamento'].value_counts())
    
    print('\nVotacao no dataset limpo:')
    print(df_limpo['votacao'].value_counts())
    
    # Verificar se ainda temos dados suficientes para treinar
    casos_provimento = df_limpo[df_limpo['resultado_julgamento'].str.contains('Provido', na=False)]
    casos_negacao = df_limpo[df_limpo['resultado_julgamento'].str.contains('Negado', na=False)]
    
    print(f'\n=== DADOS PARA TREINAMENTO ===')
    print(f'Casos de provimento: {len(casos_provimento)}')
    print(f'Casos de negacao: {len(casos_negacao)}')
    print(f'Total de casos para modelo de provimento: {len(casos_provimento) + len(casos_negacao)}')
    
    # Verificar casos de votação
    casos_votacao = casos_provimento.dropna(subset=['votacao'])
    print(f'Casos para modelo de votacao: {len(casos_votacao)}')
    
    print(f'\nDistribuicao de votacao (apenas provimentos):')
    print(casos_votacao['votacao'].value_counts())

if __name__ == "__main__":
    main()
