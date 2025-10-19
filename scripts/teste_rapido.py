#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Teste Rápido - CARF ML Predictor
"""

import os
import sys

def main():
    print("=" * 60)
    print("TESTE RAPIDO - CARF ML PREDICTOR")
    print("=" * 60)
    
    # Verificar estrutura de pastas
    pastas_necessarias = [
        'aplicacoes',
        'modelos', 
        'dados',
        'scripts',
        'notebooks',
        'documentacao',
        'assets'
    ]
    
    print("Verificando estrutura de pastas...")
    for pasta in pastas_necessarias:
        if os.path.exists(pasta):
            print(f"OK {pasta}/")
        else:
            print(f"ERRO {pasta}/ - PASTA NAO ENCONTRADA!")
    
    # Verificar arquivos principais
    arquivos_principais = [
        'run.py',
        'README.md',
        'requirements.txt',
        'aplicacoes/app_2023_2024.py',
        'modelos/modelo_carf_provimento_2023.pkl',
        'modelos/modelo_carf_votacao_2023.pkl',
        'modelos/preprocessors_2023.pkl',
        'dados/carf_2023_sem_vazamento.csv',
        'dados/carf_sem_vazamento.csv'
    ]
    
    print("\nVerificando arquivos principais...")
    for arquivo in arquivos_principais:
        if os.path.exists(arquivo):
            print(f"OK {arquivo}")
        else:
            print(f"ERRO {arquivo} - ARQUIVO NAO ENCONTRADO!")
    
    # Verificar Python e dependências
    print("\nVerificando ambiente Python...")
    try:
        import pandas
        print(f"OK pandas: {pandas.__version__}")
    except ImportError:
        print("ERRO pandas nao instalado")
    
    try:
        import streamlit
        print(f"OK streamlit: {streamlit.__version__}")
    except ImportError:
        print("ERRO streamlit nao instalado")
    
    try:
        import sklearn
        print(f"OK scikit-learn: {sklearn.__version__}")
    except ImportError:
        print("ERRO scikit-learn nao instalado")
    
    print("\n" + "=" * 60)
    print("COMANDOS PARA EXECUTAR:")
    print("=" * 60)
    print("1. Execução principal:")
    print("   python run.py")
    print()
    print("2. Execução direta:")
    print("   python -m streamlit run aplicacoes/app_2023_2024.py")
    print()
    print("3. Demonstração:")
    print("   python aplicacoes/demo_2023_2024.py")
    print()
    print("Acesse: http://localhost:8501")
    print("=" * 60)

if __name__ == "__main__":
    main()
