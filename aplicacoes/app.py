#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicação Web para Demonstração do Modelo CARF
Hackathon CARF 2024

Esta aplicação permite testar o modelo de machine learning
que prevê probabilidades de aprovação dos processos no CARF.
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuração da página
st.set_page_config(
    page_title="CARF ML Predictor",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .metric-box {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_model_and_preprocessors():
    """Carrega o modelo e os pré-processadores salvos"""
    try:
        # Carregar modelo
        model = joblib.load('modelo_carf_rf.pkl')
        
        # Carregar pré-processadores
        with open('preprocessors.pkl', 'rb') as f:
            preprocessors = pickle.load(f)
        
        return model, preprocessors
    except FileNotFoundError as e:
        st.error(f"Arquivo não encontrado: {e}")
        st.info("Execute primeiro o notebook para treinar e salvar o modelo.")
        return None, None

def prever_probabilidades_carf(texto_ementa, tributo, turma, model, preprocessors):
    """
    Função para prever probabilidades usando o modelo carregado
    """
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
    """Função principal da aplicação"""
    
    # Título principal
    st.markdown('<h1 class="main-header">⚖️ CARF ML Predictor</h1>', unsafe_allow_html=True)
    st.markdown("### Predição de Probabilidades de Aprovação no Conselho Administrativo de Recursos Fiscais")
    
    # Carregar modelo
    with st.spinner("Carregando modelo..."):
        model, preprocessors = load_model_and_preprocessors()
    
    if model is None or preprocessors is None:
        st.stop()
    
    # Sidebar com informações
    st.sidebar.markdown("## 📊 Sobre o Modelo")
    st.sidebar.info("""
    Este modelo foi treinado com dados de 2024 do CARF e utiliza:
    - **Random Forest** para classificação
    - **TF-IDF** para análise de texto das ementas
    - **Features categóricas** (tributo, turma)
    """)
    
    st.sidebar.markdown("## 🎯 Tipos de Votação")
    st.sidebar.markdown("""
    - **Unânime**: Todos os conselheiros concordam
    - **Maioria**: Maioria dos conselheiros concorda
    - **Qualidade**: Decisão por voto de qualidade
    """)
    
    # Formulário principal
    st.markdown("## 📝 Dados do Processo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Seleção de tributo
        tributos_disponiveis = [
            "IRPF - IMPOSTO SOBRE A RENDA DA PESSOA FÍSICA",
            "IRPJ - IMPOSTO SOBRE A RENDA DA PESSOA JURÍDICA", 
            "COFINS - CONTRIBUIÇÃO PARA O FINANCIAMENTO DA SEGURIDADE SOCIAL",
            "CS - CONTRIBUIÇÕES PREVIDENCIÁRIAS",
            "CSLL - CONTRIBUIÇÃO SOCIAL SOBRE O LUCRO LÍQUIDO",
            "IRRF - IMPOSTO SOBRE A RENDA RETIDO NA FONTE",
            "OUTROS-V - OUTROS VINCULADOS - COMÉRCIO EXTERIOR"
        ]
        
        tributo_selecionado = st.selectbox(
            "Selecione o tipo de tributo:",
            tributos_disponiveis
        )
    
    with col2:
        # Seleção de turma
        turmas_disponiveis = [
            "1ª TE-1ªSEÇÃO-1001-CARF-MF-DF",
            "2ª TE-1ªSEÇÃO-1002-CARF-MF-DF", 
            "01ª TO-02ªCÂMARA-02ªSEÇÃO-CARF-MF-DF",
            "02ª TO-02ªCAMARA-02ªSEÇÃO-CARF-MF-DF",
            "03ª TURMA-CSRF-CARF-MF-DF",
            "1ª TE-3ªSEÇÃO-3001-CARF-MF-DF"
        ]
        
        turma_selecionada = st.selectbox(
            "Selecione a turma:",
            turmas_disponiveis
        )
    
    # Campo de texto para ementa
    texto_ementa = st.text_area(
        "Digite o texto da ementa:",
        height=200,
        placeholder="Exemplo: Assunto: Imposto sobre a Renda de Pessoa Física - IRPF. Ano-calendário: 2009. PROCESSO ADMINISTRATIVO FISCAL..."
    )
    
    # Botão de predição
    if st.button("🔮 Prever Probabilidades", type="primary"):
        if texto_ementa.strip():
            with st.spinner("Processando predição..."):
                probabilidades, erro = prever_probabilidades_carf(
                    texto_ementa, 
                    tributo_selecionado, 
                    turma_selecionada,
                    model,
                    preprocessors
                )
            
            if erro:
                st.error(f"Erro na predição: {erro}")
            else:
                # Exibir resultados
                st.markdown("## 📊 Resultados da Predição")
                
                # Criar gráfico de barras
                fig = px.bar(
                    x=list(probabilidades.keys()),
                    y=list(probabilidades.values()),
                    title="Probabilidades de Aprovação por Tipo de Votação",
                    labels={'x': 'Tipo de Votação', 'y': 'Probabilidade'},
                    color=list(probabilidades.values()),
                    color_continuous_scale='Blues'
                )
                
                fig.update_layout(
                    yaxis_tickformat='.1%',
                    height=400,
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Exibir métricas
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Unânime",
                        f"{probabilidades.get('Unânime', 0):.1%}",
                        delta=None
                    )
                
                with col2:
                    st.metric(
                        "Maioria", 
                        f"{probabilidades.get('Maioria', 0):.1%}",
                        delta=None
                    )
                
                with col3:
                    st.metric(
                        "Qualidade",
                        f"{probabilidades.get('Qualidade', 0):.1%}",
                        delta=None
                    )
                
                # Predição principal
                predicao_principal = max(probabilidades, key=probabilidades.get)
                confianca = max(probabilidades.values())
                
                st.markdown(f"""
                <div class="prediction-box">
                    <h3>🎯 Predição Principal</h3>
                    <p><strong>Tipo de Votação:</strong> {predicao_principal}</p>
                    <p><strong>Confiança:</strong> {confianca:.1%}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Informações adicionais
                st.markdown("## ℹ️ Informações do Processo")
                st.info(f"""
                **Tributo:** {tributo_selecionado}  
                **Turma:** {turma_selecionada}  
                **Ementa:** {texto_ementa[:100]}...
                """)
        else:
            st.warning("Por favor, digite o texto da ementa para fazer a predição.")
    
    # Seção de exemplos
    st.markdown("---")
    st.markdown("## 💡 Exemplos de Uso")
    
    exemplo_col1, exemplo_col2 = st.columns(2)
    
    with exemplo_col1:
        if st.button("📋 Exemplo 1: IRPF"):
            st.session_state.exemplo_texto = """
            Assunto: Imposto sobre a Renda de Pessoa Física - IRPF
            Ano-calendário: 2009
            PROCESSO ADMINISTRATIVO FISCAL. APRESENTAÇÃO DOCUMENTAL. MOMENTO OPORTUNO. 
            IMPUGNAÇÃO. EXCEÇÕES TAXATIVAS. PRECLUSÃO.
            De acordo com o art. 16, inciso III, do Decreto 70.235, de 1972, os atos 
            processuais se concentram no momento da impugnação, cujo teor deverá abranger 
            "os motivos de fato e de direito em que se fundamenta, os pontos de discordância, 
            as razões e provas que possuir, considerando-se não impugnada a matéria que não 
            tenha sido expressamente contestada pelo impugnante.
            """
            st.session_state.exemplo_tributo = "IRPF - IMPOSTO SOBRE A RENDA DA PESSOA FÍSICA"
            st.session_state.exemplo_turma = "1ª TE-1ªSEÇÃO-1001-CARF-MF-DF"
    
    with exemplo_col2:
        if st.button("📋 Exemplo 2: COFINS"):
            st.session_state.exemplo_texto = """
            ASSUNTO: CONTRIBUIÇÃO PARA O FINANCIAMENTO DA SEGURIDADE SOCIAL (COFINS)
            Período de apuração: 01/07/2004 a 30/09/2004
            COFINS. NÃO CUMULATIVIDADE. RESSARCIMENTO. CORREÇÃO MONETÁRIA APLICAÇÃO DA SELIC. 
            POSSIBILIDADE.
            Conforme decidido no julgamento do REsp 1.767.945/PR, realizado sob o rito dos 
            recursos repetitivos, é devida a correção monetária no ressarcimento de crédito 
            escritural da não cumulatividade acumulado ao final do trimestre, após escoado 
            o prazo de 360 dias para a análise do correspondente pedido administrativo pelo Fisco.
            """
            st.session_state.exemplo_tributo = "COFINS - CONTRIBUIÇÃO PARA O FINANCIAMENTO DA SEGURIDADE SOCIAL"
            st.session_state.exemplo_turma = "03ª TURMA-CSRF-CARF-MF-DF"
    
    # Aplicar exemplo se selecionado
    if hasattr(st.session_state, 'exemplo_texto'):
        texto_ementa = st.session_state.exemplo_texto
        tributo_selecionado = st.session_state.exemplo_tributo
        turma_selecionada = st.session_state.exemplo_turma
        st.rerun()

if __name__ == "__main__":
    main()
