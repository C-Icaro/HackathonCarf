#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detecção de vazamento de informação nos dados CARF 2023
"""

import pandas as pd
import numpy as np

def main():
    print("=== DETECCAO DE VAZAMENTO - DADOS CARF 2023 ===")
    
    # Carregar dados de 2023
    df_2023 = pd.read_csv('dados/carf_julgamentos_2023.csv')
    print(f'Total de registros 2023: {len(df_2023)}')
    
    # Palavras indicativas de decisão que podem indicar vazamento
    palavras_vazamento = [
        'provido', 'negado', 'mantém-se', 'mantem-se', 'improcedente', 'procedente',
        'dar provimento', 'nega-se', 'recurso conhecido', 'decide-se', 'não se conhece',
        'voto de qualidade', 'unânime', 'maioria', 'qualidade', 'acordam os membros',
        'por unanimidade', 'por maioria', 'votaram', 'conclusões', 'julgamento',
        'decisão', 'acórdão', 'sentença', 'resultado', 'provimento', 'negação',
        'acordam', 'votação', 'votou', 'deliberou', 'julgou', 'decidiu'
    ]
    
    def detectar_vazamento(texto):
        """Detecta possível vazamento de informação no texto"""
        if pd.isna(texto):
            return False
        
        texto_lower = str(texto).lower()
        
        # Verificar cada palavra
        for palavra in palavras_vazamento:
            if palavra in texto_lower:
                return True
        
        return False
    
    # Aplicar detecção de vazamento
    print("Detectando possível vazamento de informação...")
    df_2023['possivel_vazamento'] = df_2023['texto_ementa'].apply(detectar_vazamento)
    
    # Contar registros com possível vazamento
    vazamento_count = df_2023['possivel_vazamento'].sum()
    print(f'Registros com possível vazamento: {vazamento_count}')
    print(f'Registros sem vazamento: {len(df_2023) - vazamento_count}')
    print(f'Percentual removido: {(vazamento_count/len(df_2023))*100:.1f}%')
    
    # Mostrar exemplos de registros com possível vazamento
    exemplos_vazamento = df_2023[df_2023['possivel_vazamento'] == True].head(3)
    
    print('\n=== EXEMPLOS DE REGISTROS REMOVIDOS (possível vazamento) ===')
    for i, row in exemplos_vazamento.iterrows():
        print(f'\nRegistro {i+1}:')
        print(f'Resultado: {row["resultado_julgamento"]}')
        print(f'Votação: {row["votacao"]}')
        print(f'Texto da ementa (primeiros 200 chars):')
        texto_limpo = str(row["texto_ementa"]).encode('ascii', 'ignore').decode('ascii')
        print(f'{texto_limpo[:200]}...')
        print('-' * 80)
    
    # Mostrar exemplos de registros sem vazamento
    exemplos_limpos = df_2023[df_2023['possivel_vazamento'] == False].head(3)
    
    print('\n=== EXEMPLOS DE REGISTROS MANTIDOS (sem vazamento) ===')
    for i, row in exemplos_limpos.iterrows():
        print(f'\nRegistro {i+1}:')
        print(f'Resultado: {row["resultado_julgamento"]}')
        print(f'Votação: {row["votacao"]}')
        print(f'Texto da ementa (primeiros 200 chars):')
        texto_limpo = str(row["texto_ementa"]).encode('ascii', 'ignore').decode('ascii')
        print(f'{texto_limpo[:200]}...')
        print('-' * 80)
    
    # Criar dataset sem vazamento
    print('\n=== CRIANDO DATASET LIMPO 2023 ===')
    df_sem_vazamento = df_2023[df_2023['possivel_vazamento'] == False].copy()
    df_sem_vazamento = df_sem_vazamento.drop('possivel_vazamento', axis=1)
    
    # Salvar dataset limpo
    df_sem_vazamento.to_csv('dados/carf_2023_sem_vazamento.csv', index=False)
    
    print(f'Dataset limpo 2023 salvo: dados/carf_2023_sem_vazamento.csv')
    print(f'Registros no dataset limpo: {len(df_sem_vazamento)}')
    
    # Análise da distribuição dos resultados
    print('\n=== ANALISE DA DISTRIBUICAO ===')
    print('Distribuição original 2023:')
    print(df_2023['resultado_julgamento'].value_counts())
    
    print('\nDistribuição após remoção 2023:')
    print(df_sem_vazamento['resultado_julgamento'].value_counts())
    
    print('\nDistribuição de votação original 2023:')
    print(df_2023['votacao'].value_counts())
    
    print('\nDistribuição de votação após remoção 2023:')
    print(df_sem_vazamento['votacao'].value_counts())
    
    # Análise para treinamento
    print('\n=== DADOS PARA TREINAMENTO ===')
    casos_provimento = df_sem_vazamento[df_sem_vazamento['resultado_julgamento'].str.contains('Provido', na=False)]
    casos_negacao = df_sem_vazamento[df_sem_vazamento['resultado_julgamento'].str.contains('Negado', na=False)]
    
    print(f'Casos de provimento: {len(casos_provimento)}')
    print(f'Casos de negacao: {len(casos_negacao)}')
    print(f'Total de casos para modelo de provimento: {len(casos_provimento) + len(casos_negacao)}')
    
    # Verificar casos de votação
    casos_votacao = casos_provimento.dropna(subset=['votacao'])
    print(f'Casos para modelo de votacao: {len(casos_votacao)}')
    
    print(f'\nDistribuicao de votacao (apenas provimentos):')
    print(casos_votacao['votacao'].value_counts())
    
    print('\n=== RESUMO FINAL ===')
    print(f'Total de registros originais 2023: {len(df_2023)}')
    print(f'Registros removidos por vazamento: {vazamento_count}')
    print(f'Registros mantidos: {len(df_sem_vazamento)}')
    print(f'Percentual de dados preservados: {((len(df_sem_vazamento)/len(df_2023))*100):.1f}%')
    print(f'Dataset limpo salvo em: dados/carf_2023_sem_vazamento.csv')

if __name__ == "__main__":
    main()
