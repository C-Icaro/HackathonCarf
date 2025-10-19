#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples do Streamlit
"""

import streamlit as st

st.title("Teste Simples")
st.write("Se você está vendo esta mensagem, o Streamlit está funcionando!")

if st.button("Clique aqui"):
    st.success("Botão funcionando!")
