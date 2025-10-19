#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CARF ML Predictor - Execução Principal
Sistema de predição de resultados do CARF sem vazamento de informação
"""

import os
import sys
import subprocess

def main():
    print("=" * 70)
    print("⚖️  CARF ML PREDICTOR 2023/2024")
    print("=" * 70)
    print("Sistema de predição de resultados do CARF")
    print("Modelos treinados com dados de 2023 e testados com dados de 2024")
    print("=" * 70)
    
    # Verificar se os arquivos necessários existem
    arquivos_necessarios = [
        'aplicacoes/app_2023_2024.py',
        'modelos/modelo_carf_provimento_2023.pkl',
        'modelos/modelo_carf_votacao_2023.pkl',
        'modelos/preprocessors_2023.pkl'
    ]
    
    print("Verificando arquivos necessários...")
    todos_presentes = True
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} - ARQUIVO NÃO ENCONTRADO!")
            todos_presentes = False
    
    if not todos_presentes:
        print("\n❌ Alguns arquivos necessários não foram encontrados!")
        print("Execute primeiro: cd notebooks && python train_model_2023_2024.py")
        return
    
    print("\n✅ Todos os arquivos necessários estão presentes!")
    
    # Verificar se streamlit está instalado
    try:
        import streamlit
        print(f"✅ Streamlit instalado: {streamlit.__version__}")
    except ImportError:
        print("❌ Streamlit não está instalado!")
        print("Execute: pip install streamlit")
        return
    
    print("\n" + "=" * 70)
    print("🚀 INICIANDO A PLATAFORMA...")
    print("=" * 70)
    print("📱 Acesse: http://localhost:8501")
    print("⏹️  Para parar: Ctrl+C")
    print("=" * 70)
    
    # Executar a aplicação
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'aplicacoes/app_2023_2024.py',
            '--server.headless', 'true',
            '--server.port', '8501'
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Aplicação encerrada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro ao executar a aplicação: {e}")

if __name__ == "__main__":
    main()
