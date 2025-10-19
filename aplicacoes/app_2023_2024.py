#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicação Web CARF ML Predictor - Versão 2023/2024
Modelos treinados com dados de 2023 e testados com dados de 2024
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import joblib
import os

# Configuração da página
st.set_page_config(
    page_title="Projeto LexCARF - O sistema de apoio a decisão do CARF.",
    page_icon="⚖️",
    layout="wide"
)

@st.cache_data
def load_models_and_preprocessors():
    """Carrega os modelos e os pré-processadores salvos"""
    try:
        # Determinar o diretório base do projeto
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Carregar modelos
        model_provimento = joblib.load(os.path.join(base_dir, 'modelos', 'modelo_carf_provimento_2023.pkl'))
        model_votacao = joblib.load(os.path.join(base_dir, 'modelos', 'modelo_carf_votacao_2023.pkl'))
        
        # Carregar pré-processadores
        with open(os.path.join(base_dir, 'modelos', 'preprocessors_2023.pkl'), 'rb') as f:
            preprocessors = pickle.load(f)
        
        return model_provimento, model_votacao, preprocessors
    except Exception as e:
        st.error(f"Erro ao carregar modelos: {e}")
        return None, None, None

def prever_probabilidades_2023_2024(texto_ementa, tributo, turma, model_provimento, model_votacao, preprocessors):
    """Função para prever probabilidades usando ambos os modelos"""
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
    """Função principal da aplicação"""
    
    # Título principal
    st.title("⚖️ CARF ML Predictor 2023/2024")
    st.markdown("### Predição de Probabilidades de Provimento e Tipo de Votação no CARF")
    st.markdown("**Modelos treinados com dados de 2023 e testados com dados de 2024**")
    
    # Carregar modelos
    with st.spinner("Carregando modelos..."):
        model_provimento, model_votacao, preprocessors = load_models_and_preprocessors()
    
    if model_provimento is None or model_votacao is None or preprocessors is None:
        st.error("Não foi possível carregar os modelos. Verifique se os arquivos existem.")
        st.info("Execute primeiro: `cd notebooks && python train_model_2023_2024.py`")
        return
    
    st.success("✅ Modelos carregados com sucesso!")
    
    # Sidebar com informações
    st.sidebar.markdown("## 📊 Sobre os Modelos")
    st.sidebar.info("""
    **Modelo de Provimento:**
    - Provido Total
    - Negado
    
    **Modelo de Votação:**
    - Unânime
    - Maioria  
    - Qualidade
    - Empate
    
    **Treinamento:** Dados 2023 (9.348 registros)
    **Teste:** Dados 2024 (12.310 registros)
    **Algoritmo:** Random Forest + TF-IDF
    """)
    
    st.sidebar.markdown("## 🎯 Performance dos Modelos")
    st.sidebar.success("""
    **Modelo de Provimento:**
    - Acurácia: 75%
    - Precision: Negado (66%), Provido (86%)
    - Recall: Negado (86%), Provido (66%)
    
    **Modelo de Votação:**
    - Acurácia: 87%
    - Precision: Unânime (91%), Maioria (23%)
    - Recall: Unânime (96%), Maioria (13%)
    """)
    
    st.sidebar.markdown("## 🎯 Tipos de Resultado")
    st.sidebar.markdown("""
    **Provimento:**
    - **Provido Total**: Recurso totalmente aceito
    - **Negado**: Recurso rejeitado
    
    **Votação (apenas para provimentos):**
    - **Unânime**: Todos concordam
    - **Maioria**: Maioria concorda
    - **Qualidade**: Voto de qualidade
    - **Empate**: Empate (Lei 13.988/2020)
    """)
    
    # Formulário principal
    st.markdown("## 📝 Dados do Processo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Seleção de tributo
        tributos_disponiveis = [
            "IRPF - IMPOSTO SOBRE A RENDA DA PESSOA FÍSICA",
            "IRPJ - IMPOSTO SOBRE A RENDA DA PESSOA JURÍDICA", 
            "CS - CONTRIBUIÇÕES PREVIDENCIÁRIAS",
            "COFINS - CONTRIBUIÇÃO PARA O FINANCIAMENTO DA SEGURIDADE SOCIAL",
            "PIS - CONTRIBUIÇÃO PARA O PROGRAMA DE INTEGRAÇÃO SOCIAL",
            "OUTROS-V - OUTROS VINCULADOS - COMÉRCIO EXTERIOR",
            "IPI - IMPOSTO SOBRE PRODUTOS INDUSTRIALIZADOS",
            "CSLL - CONTRIBUIÇÃO SOCIAL SOBRE O LUCRO LÍQUIDO",
            "IRRF - IMPOSTO SOBRE A RENDA RETIDO NA FONTE",
            "ITR - IMPOSTO TERRITORIAL RURAL"
        ]
        
        tributo_selecionado = st.selectbox(
            "Selecione o tipo de tributo:",
            tributos_disponiveis
        )
    
    with col2:
        # Seleção de turma
        turmas_disponiveis = [
            "3ª TE-2ªSEÇÃO-2003-CARF-MF-DF",
            "02ª TO-04ªCÂMARA-02ªSEÇÃO-CARF-MF-DF", 
            "02ª TO-04ªCÂMARA-03ªSEÇÃO-CARF-MF-DF",
            "01ª TO-03ªCÂMARA-03ªSEÇÃO-CARF-MF-DF",
            "01ª TO-02ªCÂMARA-03ªSEÇÃO-CARF-MF-DF",
            "01ª TO-02ªCÂMARA-02ªSEÇÃO-CARF-MF-DF",
            "1ª TE-2ªSEÇÃO-2001-CARF-MF-DF",
            "01ª TO-04ªCÂMARA-03ªSEÇÃO-CARF-MF-DF",
            "02ª TO-03ªCÂMARA-03ªSEÇÃO-CARF-MF-DF",
            "03ª TURMA-CSRF-CARF-MF-DF"
        ]
        
        turma_selecionada = st.selectbox(
            "Selecione a turma:",
            turmas_disponiveis
        )
    
    # Campo de texto para ementa
    texto_ementa = st.text_area(
        "Digite o texto parcial da ementa ou outras informações relevantes:",
        height=200,
        placeholder="Exemplo: Assunto: Imposto sobre a Renda de Pessoa Física - IRPF. Ano-calendário: 2009. PROCESSO ADMINISTRATIVO FISCAL..."
    )
    
    # Botão de predição
    if st.button("🔮 Prever Probabilidades", type="primary"):
        if texto_ementa.strip():
            with st.spinner("Processando predição..."):
                prob_provimento, prob_votacao, erro = prever_probabilidades_2023_2024(
                    texto_ementa, 
                    tributo_selecionado, 
                    turma_selecionada,
                    model_provimento,
                    model_votacao,
                    preprocessors
                )
            
            if erro:
                st.error(f"Erro na predição: {erro}")
            else:
                # Exibir resultados
                st.markdown("## 📊 Resultados da Predição")
                
                # Criar duas colunas para os resultados
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 🎯 Probabilidade de Provimento")
                    
                    # Métricas de provimento
                    col_prov1, col_prov2 = st.columns(2)
                    
                    with col_prov1:
                        st.metric(
                            "Provido Total",
                            f"{prob_provimento.get('Provido Total', 0):.1%}",
                            delta=None
                        )
                    
                    with col_prov2:
                        st.metric(
                            "Negado", 
                            f"{prob_provimento.get('Negado', 0):.1%}",
                            delta=None
                        )
                    
                    # Predição principal de provimento
                    predicao_provimento = max(prob_provimento, key=prob_provimento.get)
                    confianca_provimento = max(prob_provimento.values())
                    
                    if predicao_provimento == 'Provido Total':
                        st.success(f"✅ **Provimento:** {predicao_provimento} ({confianca_provimento:.1%})")
                    else:
                        st.error(f"❌ **Provimento:** {predicao_provimento} ({confianca_provimento:.1%})")
                
                with col2:
                    st.markdown("### 🗳️ Tipo de Votação")
                    
                    # Métricas de votação
                    col_vot1, col_vot2, col_vot3, col_vot4 = st.columns(4)
                    
                    with col_vot1:
                        st.metric(
                            "Unânime",
                            f"{prob_votacao.get('Unânime', 0):.1%}",
                            delta=None
                        )
                    
                    with col_vot2:
                        st.metric(
                            "Maioria", 
                            f"{prob_votacao.get('Maioria', 0):.1%}",
                            delta=None
                        )
                    
                    with col_vot3:
                        st.metric(
                            "Qualidade",
                            f"{prob_votacao.get('Qualidade', 0):.1%}",
                            delta=None
                        )
                    
                    with col_vot4:
                        st.metric(
                            "Empate",
                            f"{prob_votacao.get('Empate', 0):.1%}",
                            delta=None
                        )
                    
                    # Predição principal de votação
                    predicao_votacao = max(prob_votacao, key=prob_votacao.get)
                    confianca_votacao = max(prob_votacao.values())
                    
                    st.info(f"🗳️ **Votação:** {predicao_votacao} ({confianca_votacao:.1%})")
                
                # Resumo combinado
                st.markdown("## 🎯 Resumo Combinado")
                
                if predicao_provimento == 'Provido Total':
                    st.success(f"""
                    **Resultado Esperado:** {predicao_provimento} por {predicao_votacao}
                    
                    - Probabilidade de Provimento: {confianca_provimento:.1%}
                    - Tipo de Votação: {confianca_votacao:.1%}
                    - Confiança Combinada: {(confianca_provimento + confianca_votacao) / 2:.1%}
                    """)
                else:
                    st.error(f"""
                    **Resultado Esperado:** {predicao_provimento}
                    
                    - Probabilidade de Negação: {confianca_provimento:.1%}
                    - Tipo de Votação: Não aplicável (recurso negado)
                    """)
                
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
            st.session_state.exemplo_turma = "3ª TE-2ªSEÇÃO-2003-CARF-MF-DF"
            st.rerun()
    
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
            st.rerun()
    
    # Aplicar exemplo se selecionado
    if hasattr(st.session_state, 'exemplo_texto'):
        texto_ementa = st.session_state.exemplo_texto
        tributo_selecionado = st.session_state.exemplo_tributo
        turma_selecionada = st.session_state.exemplo_turma
        st.rerun()

if __name__ == "__main__":
    main()
