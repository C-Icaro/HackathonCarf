#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Demonstração do Modelo CARF 2023/2024
Modelos treinados com dados de 2023 e testados com dados de 2024
"""

import pandas as pd
import numpy as np
import pickle
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

def carregar_modelos():
    """Carrega os modelos e os pré-processadores"""
    try:
        # Determinar o diretório base do projeto
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        model_provimento = joblib.load(os.path.join(base_dir, 'modelos', 'modelo_carf_provimento_2023.pkl'))
        model_votacao = joblib.load(os.path.join(base_dir, 'modelos', 'modelo_carf_votacao_2023.pkl'))
        
        with open(os.path.join(base_dir, 'modelos', 'preprocessors_2023.pkl'), 'rb') as f:
            preprocessors = pickle.load(f)
        
        return model_provimento, model_votacao, preprocessors
    except Exception as e:
        print(f"Erro ao carregar modelos: {e}")
        return None, None, None

def prever_probabilidades_2023_2024(texto_ementa, tributo, turma, model_provimento, model_votacao, preprocessors):
    """Faz predição das probabilidades usando ambos os modelos"""
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
        
        # Fazer predições
        prob_provimento = model_provimento.predict_proba(X_input)[0]
        prob_votacao = model_votacao.predict_proba(X_input)[0]
        
        # Criar resultados
        resultado_provimento = {}
        for i, classe in enumerate(model_provimento.classes_):
            resultado_provimento[classe] = prob_provimento[i]
        
        resultado_votacao = {}
        for i, classe in enumerate(model_votacao.classes_):
            resultado_votacao[classe] = prob_votacao[i]
        
        return resultado_provimento, resultado_votacao, None
        
    except Exception as e:
        return None, None, str(e)

def main():
    """Função principal de demonstração"""
    print("=" * 70)
    print("PROJETO LEXCARF - DEMONSTRACAO")
    print("O sistema de apoio a decisao do CARF")
    print("=" * 70)
    
    # Carregar modelos
    print("Carregando modelos...")
    model_provimento, model_votacao, preprocessors = carregar_modelos()
    
    if model_provimento is None or model_votacao is None or preprocessors is None:
        print("Erro: Nao foi possivel carregar os modelos!")
        return
    
    print("Modelos carregados com sucesso!")
    print(f"Classes de provimento: {model_provimento.classes_}")
    print(f"Classes de votacao: {model_votacao.classes_}")
    
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
            "turma": "3ª TE-2ªSEÇÃO-2003-CARF-MF-DF"
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
            "turma": "01ª TO-02ªCÂMARA-02ªSEÇÃO-CARF-MF-DF"
        }
    ]
    
    # Executar exemplos
    for i, exemplo in enumerate(exemplos, 1):
        print(f"\n{'-' * 70}")
        print(f"EXEMPLO {i}: {exemplo['nome']}")
        print(f"{'-' * 70}")
        
        print(f"Tributo: {exemplo['tributo']}")
        print(f"Turma: {exemplo['turma']}")
        print(f"Ementa: {exemplo['texto_ementa'][:100]}...")
        
        # Fazer predição
        prob_provimento, prob_votacao, erro = prever_probabilidades_2023_2024(
            exemplo['texto_ementa'],
            exemplo['tributo'],
            exemplo['turma'],
            model_provimento,
            model_votacao,
            preprocessors
        )
        
        if erro:
            print(f"Erro na predicao: {erro}")
        else:
            print("\nPROBABILIDADES DE PROVIMENTO:")
            for classe, prob in prob_provimento.items():
                print(f"  {classe}: {prob:.1%}")
            
            print("\nPROBABILIDADES DE VOTACAO:")
            for classe, prob in prob_votacao.items():
                print(f"  {classe}: {prob:.1%}")
            
            # Predições principais
            predicao_provimento = max(prob_provimento, key=prob_provimento.get)
            confianca_provimento = max(prob_provimento.values())
            
            predicao_votacao = max(prob_votacao, key=prob_votacao.get)
            confianca_votacao = max(prob_votacao.values())
            
            print(f"\nPREDICAO PRINCIPAL:")
            print(f"  Provimento: {predicao_provimento} ({confianca_provimento:.1%})")
            print(f"  Votacao: {predicao_votacao} ({confianca_votacao:.1%})")
            
            # Resumo combinado
            if predicao_provimento == 'Provido Total':
                print(f"\nRESULTADO ESPERADO: {predicao_provimento} por {predicao_votacao}")
                print(f"Confianca combinada: {(confianca_provimento + confianca_votacao) / 2:.1%}")
            else:
                print(f"\nRESULTADO ESPERADO: {predicao_provimento}")
    
    print(f"\n{'=' * 70}")
    print("DEMONSTRACAO CONCLUIDA!")
    print("Para usar a interface web, execute: streamlit run app_2023_2024.py")
    print(f"{'=' * 70}")

if __name__ == "__main__":
    main()
