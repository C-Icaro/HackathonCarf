#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para executar a plataforma CARF ML Predictor 2023/2024
"""

import subprocess
import sys
import os

def main():
    print("=" * 60)
    print("CARF ML PREDICTOR 2023/2024 - PLATAFORMA SEM VAZAMENTO")
    print("=" * 60)
    
    # Verificar se os arquivos necessários existem
    arquivos_necessarios = [
        'app_2023_2024.py',
        'modelo_carf_provimento_2023.pkl',
        'modelo_carf_votacao_2023.pkl',
        'preprocessors_2023.pkl'
    ]
    
    print("Verificando arquivos necessários...")
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} - ARQUIVO NÃO ENCONTRADO!")
            return
    
    print("\nTodos os arquivos necessários estão presentes!")
    
    # Verificar se streamlit está instalado
    try:
        import streamlit
        print(f"✅ Streamlit instalado: {streamlit.__version__}")
    except ImportError:
        print("❌ Streamlit não está instalado!")
        print("Execute: pip install streamlit")
        return
    
    print("\n" + "=" * 60)
    print("INICIANDO A PLATAFORMA...")
    print("=" * 60)
    print("Acesse: http://localhost:8501")
    print("Para parar: Ctrl+C")
    print("=" * 60)
    
    # Executar a aplicação
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'app_2023_2024.py',
            '--server.headless', 'true',
            '--server.port', '8501'
        ])
    except KeyboardInterrupt:
        print("\n\nAplicação encerrada pelo usuário.")
    except Exception as e:
        print(f"\nErro ao executar a aplicação: {e}")

if __name__ == "__main__":
    main()
