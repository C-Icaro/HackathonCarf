#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para executar a aplicação CARF ML Predictor
"""

import subprocess
import sys
import os
import time

def run_streamlit_app():
    """Executa a aplicação Streamlit"""
    print("🚀 Iniciando aplicação CARF ML Predictor...")
    
    # Verificar se os arquivos necessários existem
    required_files = ['modelo_carf_rf.pkl', 'preprocessors.pkl', 'app_final.py']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Arquivos não encontrados: {missing_files}")
        print("Execute primeiro o script de treinamento para criar o modelo.")
        return False
    
    print("✅ Todos os arquivos necessários encontrados!")
    
    try:
        # Executar aplicação
        print("🌐 Iniciando servidor Streamlit...")
        print("📱 Acesse: http://localhost:8501")
        print("⏹️  Para parar: Ctrl+C")
        
        # Executar streamlit
        result = subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app_final.py",
            "--server.headless", "false",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
        
        return result.returncode == 0
        
    except KeyboardInterrupt:
        print("\n👋 Aplicação encerrada pelo usuário.")
        return True
    except Exception as e:
        print(f"❌ Erro ao executar aplicação: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("CARF ML PREDICTOR - LAUNCHER")
    print("=" * 60)
    
    success = run_streamlit_app()
    
    if success:
        print("✅ Aplicação executada com sucesso!")
    else:
        print("❌ Falha ao executar a aplicação.")
        print("\nTroubleshooting:")
        print("1. Verifique se o Python está instalado")
        print("2. Instale as dependências: pip install streamlit pandas numpy scikit-learn")
        print("3. Execute o treinamento do modelo primeiro")

if __name__ == "__main__":
    main()
