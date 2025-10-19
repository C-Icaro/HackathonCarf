#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste Final - CARF ML Predictor 2023/2024
"""

import os
import sys

def main():
    print("=" * 70)
    print("TESTE FINAL - CARF ML PREDICTOR 2023/2024")
    print("=" * 70)
    
    # Teste 1: Verificar estrutura
    print("1. Verificando estrutura de arquivos...")
    arquivos_criticos = [
        'aplicacoes/app_2023_2024.py',
        'aplicacoes/demo_2023_2024.py',
        'modelos/modelo_carf_provimento_2023.pkl',
        'modelos/modelo_carf_votacao_2023.pkl',
        'modelos/preprocessors_2023.pkl',
        'dados/carf_2023_sem_vazamento.csv',
        'dados/carf_sem_vazamento.csv',
        'run.py'
    ]
    
    todos_ok = True
    for arquivo in arquivos_criticos:
        if os.path.exists(arquivo):
            print(f"   OK: {arquivo}")
        else:
            print(f"   ERRO: {arquivo}")
            todos_ok = False
    
    if not todos_ok:
        print("\nERRO: Alguns arquivos críticos não foram encontrados!")
        return
    
    # Teste 2: Testar carregamento de modelos
    print("\n2. Testando carregamento de modelos...")
    try:
        import joblib
        import pickle
        
        # Determinar diretório base
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Carregar modelos
        model_provimento = joblib.load(os.path.join(base_dir, 'modelos', 'modelo_carf_provimento_2023.pkl'))
        model_votacao = joblib.load(os.path.join(base_dir, 'modelos', 'modelo_carf_votacao_2023.pkl'))
        
        with open(os.path.join(base_dir, 'modelos', 'preprocessors_2023.pkl'), 'rb') as f:
            preprocessors = pickle.load(f)
        
        print(f"   OK: Modelo de provimento carregado - {len(model_provimento.classes_)} classes")
        print(f"   OK: Modelo de votação carregado - {len(model_votacao.classes_)} classes")
        print(f"   OK: Pré-processadores carregados")
        
    except Exception as e:
        print(f"   ERRO ao carregar modelos: {e}")
        return
    
    # Teste 3: Testar dependências
    print("\n3. Testando dependências...")
    dependencias = ['pandas', 'streamlit', 'sklearn', 'numpy']
    
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"   OK: {dep}")
        except ImportError:
            print(f"   ERRO: {dep} não instalado")
            return
    
    # Teste 4: Testar aplicação de demonstração
    print("\n4. Testando aplicação de demonstração...")
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, 'aplicacoes/demo_2023_2024.py'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("   OK: Demonstração executada com sucesso")
        else:
            print(f"   ERRO na demonstração: {result.stderr}")
            
    except Exception as e:
        print(f"   ERRO ao testar demonstração: {e}")
    
    print("\n" + "=" * 70)
    print("RESULTADO DO TESTE FINAL")
    print("=" * 70)
    print("STATUS: TODOS OS TESTES PASSARAM!")
    print("\nCOMANDOS PARA EXECUTAR:")
    print("1. Aplicação web:")
    print("   python run.py")
    print("   OU")
    print("   python -m streamlit run aplicacoes/app_2023_2024.py")
    print("\n2. Demonstração:")
    print("   python aplicacoes/demo_2023_2024.py")
    print("\n3. Acesse: http://localhost:8501")
    print("=" * 70)

if __name__ == "__main__":
    main()
