#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Demonstração do Modelo CARF
Hackathon CARF 2024

Este script demonstra o uso do modelo treinado para prever
probabilidades de aprovação dos processos no CARF.
"""

import pandas as pd
import numpy as np
import pickle
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

def carregar_modelo():
    """Carrega o modelo e os pré-processadores"""
    try:
        model = joblib.load('modelo_carf_rf.pkl')
        with open('preprocessors.pkl', 'rb') as f:
            preprocessors = pickle.load(f)
        return model, preprocessors
    except Exception as e:
        print(f"Erro ao carregar modelo: {e}")
        return None, None

def prever_probabilidades(texto_ementa, tributo, turma, model, preprocessors):
    """Faz predição das probabilidades"""
    try:
        # Extrair componentes
        le_tributo = preprocessors['le_tributo']
        le_turma = preprocessors['le_turma']
        tfidf = preprocessors['tfidf']
        tributos_frequentes = preprocessors['tributos_frequentes']
        
        # Preparar dados de entrada
        texto_clean = str(texto_ementa)[:1000] if texto_ementa else ""
        
        # Codificar tributo
        tributo_codificado = tributo if tributo in tributos_frequentes else 'OUTROS'
        tributo_encoded = le_tributo.transform([tributo_codificado])[0]
        
        # Codificar turma
        turma_simplificada = str(turma).split('ª')[0] + 'ª' if 'ª' in str(turma) else 'OUTROS'
        turma_encoded = le_turma.transform([turma_simplificada])[0]
        
        # Criar embedding TF-IDF
        texto_tfidf = tfidf.transform([texto_clean]).toarray()
        
        # Combinar features
        X_input = np.hstack([[tributo_encoded, turma_encoded], texto_tfidf[0]])
        X_input = X_input.reshape(1, -1)
        
        # Fazer predição
        probabilidades = model.predict_proba(X_input)[0]
        
        # Criar resultado
        resultado = {}
        for i, classe in enumerate(model.classes_):
            resultado[classe] = probabilidades[i]
        
        return resultado, None
        
    except Exception as e:
        return None, str(e)

def main():
    """Função principal de demonstração"""
    print("=" * 60)
    print("CARF ML PREDICTOR - DEMONSTRACAO")
    print("=" * 60)
    
    # Carregar modelo
    print("Carregando modelo...")
    model, preprocessors = carregar_modelo()
    
    if model is None or preprocessors is None:
        print("Erro: Nao foi possivel carregar o modelo!")
        return
    
    print("Modelo carregado com sucesso!")
    print(f"Classes disponiveis: {model.classes_}")
    
    # Exemplos de demonstração
    exemplos = [
        {
            "nome": "Exemplo 1: IRPF - Imposto sobre Renda Pessoa Fisica",
            "texto_ementa": """
            Assunto: Imposto sobre a Renda de Pessoa Fisica - IRPF
            Ano-calendario: 2009
            PROCESSO ADMINISTRATIVO FISCAL. APRESENTACAO DOCUMENTAL. MOMENTO OPORTUNO. 
            IMPUGNACAO. EXCECOES TAXATIVAS. PRECLUSAO.
            De acordo com o art. 16, inciso III, do Decreto 70.235, de 1972, os atos 
            processuais se concentram no momento da impugnacao, cujo teor devera abranger 
            "os motivos de fato e de direito em que se fundamenta, os pontos de discordancia, 
            as razoes e provas que possuir, considerando-se nao impugnada a materia que nao 
            tenha sido expressamente contestada pelo impugnante.
            """,
            "tributo": "IRPF - IMPOSTO SOBRE A RENDA DA PESSOA FISICA",
            "turma": "1ª TE-1ªSEÇÃO-1001-CARF-MF-DF"
        },
        {
            "nome": "Exemplo 2: COFINS - Contribuicao para Seguridade Social",
            "texto_ementa": """
            ASSUNTO: CONTRIBUIÇÃO PARA O FINANCIAMENTO DA SEGURIDADE SOCIAL (COFINS)
            Periodo de apuracao: 01/07/2004 a 30/09/2004
            COFINS. NAO CUMULATIVIDADE. RESSARCIMENTO. CORRECAO MONETARIA APLICACAO DA SELIC. 
            POSSIBILIDADE.
            Conforme decidido no julgamento do REsp 1.767.945/PR, realizado sob o rito dos 
            recursos repetitivos, e devida a correcao monetaria no ressarcimento de credito 
            escritural da nao cumulatividade acumulado ao final do trimestre, apos escoado 
            o prazo de 360 dias para a analise do correspondente pedido administrativo pelo Fisco.
            """,
            "tributo": "COFINS - CONTRIBUIÇÃO PARA O FINANCIAMENTO DA SEGURIDADE SOCIAL",
            "turma": "03ª TURMA-CSRF-CARF-MF-DF"
        },
        {
            "nome": "Exemplo 3: IRPJ - Imposto sobre Renda Pessoa Juridica",
            "texto_ementa": """
            ASSUNTO: IMPOSTO SOBRE A RENDA DE PESSOA JURIDICA (IRPJ)
            Ano-calendario: 2013
            RESTITUICAO COMPENSACAO. DIREITO CREDITORIO. PROVA DA CERTEZA E LIQUIDEZ.
            Somente podem ser objeto de pedido de restituicao ou de declaracao de compensacao 
            creditos liquidos e certos do sujeito passivo contra a Fazenda Publica. Nesse contexto, 
            o credito pleiteado pelo sujeito passivo somente sera liquido e certo se, quanto a 
            certeza, nao houver controversia sobre sua existencia e, quanto a liquidez, quando 
            restar indubitavelmente determinada a sua importancia.
            """,
            "tributo": "IRPJ - IMPOSTO SOBRE A RENDA DA PESSOA JURIDICA",
            "turma": "1ª TE-1ªSEÇÃO-1001-CARF-MF-DF"
        }
    ]
    
    # Executar exemplos
    for i, exemplo in enumerate(exemplos, 1):
        print(f"\n{'-' * 60}")
        print(f"EXEMPLO {i}: {exemplo['nome']}")
        print(f"{'-' * 60}")
        
        print(f"Tributo: {exemplo['tributo']}")
        print(f"Turma: {exemplo['turma']}")
        print(f"Ementa: {exemplo['texto_ementa'][:100]}...")
        
        # Fazer predição
        probabilidades, erro = prever_probabilidades(
            exemplo['texto_ementa'],
            exemplo['tributo'],
            exemplo['turma'],
            model,
            preprocessors
        )
        
        if erro:
            print(f"Erro na predicao: {erro}")
        else:
            print("\nPROBABILIDADES DE APROVACAO:")
            for classe, prob in probabilidades.items():
                print(f"  {classe}: {prob:.1%}")
            
            # Predição principal
            predicao_principal = max(probabilidades, key=probabilidades.get)
            confianca = max(probabilidades.values())
            print(f"\nPREDICAO PRINCIPAL: {predicao_principal} ({confianca:.1%})")
    
    print(f"\n{'=' * 60}")
    print("DEMONSTRACAO CONCLUIDA!")
    print("Para usar a interface web, execute: streamlit run app.py")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    main()
