#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para detectar e remover vazamento de informação (data leakage)
nos textos das ementas do CARF
"""

import pandas as pd
import re

def main():
    print("=== DETECÇÃO DE VAZAMENTO DE INFORMAÇÃO (DATA LEAKAGE) ===")
    
    # Carregar dados
    df = pd.read_csv('dados/carf_julgamentos_2024.csv')
    print(f'Total de registros originais: {len(df)}')
    
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
    df['possivel_vazamento'] = df['texto_ementa'].apply(detectar_vazamento)
    
    # Contar registros com possível vazamento
    vazamento_count = df['possivel_vazamento'].sum()
    print(f'Registros com possível vazamento: {vazamento_count}')
    print(f'Registros sem vazamento: {len(df) - vazamento_count}')
    print(f'Percentual removido: {(vazamento_count/len(df))*100:.1f}%')
    
    # Mostrar exemplos de registros com possível vazamento
    exemplos_vazamento = df[df['possivel_vazamento'] == True].head(3)
    
    print('\n=== EXEMPLOS DE REGISTROS REMOVIDOS (possível vazamento) ===')
    for i, row in exemplos_vazamento.iterrows():
        print(f'\nRegistro {i+1}:')
        print(f'Resultado: {row["resultado_julgamento"]}')
        print(f'Votação: {row["votacao"]}')
        print(f'Texto da ementa (primeiros 200 chars):')
        print(f'{str(row["texto_ementa"])[:200]}...')
        print('-' * 80)
    
    # Mostrar exemplos de registros sem vazamento
    exemplos_limpos = df[df['possivel_vazamento'] == False].head(3)
    
    print('\n=== EXEMPLOS DE REGISTROS MANTIDOS (sem vazamento) ===')
    for i, row in exemplos_limpos.iterrows():
        print(f'\nRegistro {i+1}:')
        print(f'Resultado: {row["resultado_julgamento"]}')
        print(f'Votação: {row["votacao"]}')
        print(f'Texto da ementa (primeiros 200 chars):')
        print(f'{str(row["texto_ementa"])[:200]}...')
        print('-' * 80)
    
    # Criar dataset sem vazamento
    print('\n=== CRIANDO DATASET LIMPO ===')
    df_sem_vazamento = df[df['possivel_vazamento'] == False].copy()
    df_sem_vazamento = df_sem_vazamento.drop('possivel_vazamento', axis=1)
    
    # Salvar dataset limpo
    df_sem_vazamento.to_csv('dados/carf_sem_vazamento.csv', index=False)
    
    print(f'Dataset limpo salvo: dados/carf_sem_vazamento.csv')
    print(f'Registros no dataset limpo: {len(df_sem_vazamento)}')
    
    # Análise da distribuição dos resultados
    print('\n=== ANÁLISE DA DISTRIBUIÇÃO ===')
    print('Distribuição original:')
    print(df['resultado_julgamento'].value_counts())
    
    print('\nDistribuição após remoção:')
    print(df_sem_vazamento['resultado_julgamento'].value_counts())
    
    print('\nDistribuição de votação original:')
    print(df['votacao'].value_counts())
    
    print('\nDistribuição de votação após remoção:')
    print(df_sem_vazamento['votacao'].value_counts())
    
    print('\n=== RESUMO FINAL ===')
    print(f'Total de registros originais: {len(df)}')
    print(f'Registros removidos por vazamento: {vazamento_count}')
    print(f'Registros mantidos: {len(df_sem_vazamento)}')
    print(f'Percentual de dados preservados: {((len(df_sem_vazamento)/len(df))*100):.1f}%')
    print(f'Dataset limpo salvo em: dados/carf_sem_vazamento.csv')

if __name__ == "__main__":
    main()
