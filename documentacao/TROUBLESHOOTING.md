# CARF ML Predictor - Guia de Solução de Problemas

## 🚨 Problemas Comuns e Soluções

### 1. "Aplicação não está rodando"

**Possíveis causas:**
- Dependências não instaladas
- Modelo não treinado
- Porta ocupada
- Erro no código

**Soluções:**

#### A) Verificar dependências
```bash
pip install streamlit pandas numpy scikit-learn plotly
```

#### B) Treinar modelo primeiro
```bash
cd notebooks
python train_model.py
cd ..
```

#### C) Testar aplicação simples
```bash
streamlit run teste_streamlit.py
```

#### D) Usar porta diferente
```bash
streamlit run app_final.py --server.port 8502
```

### 2. "Erro ao carregar modelo"

**Soluções:**
```bash
# Verificar se os arquivos existem
dir modelo_carf_rf.pkl
dir preprocessors.pkl

# Se não existirem, treinar modelo
cd notebooks
python train_model.py
cd ..
```

### 3. "Erro de importação"

**Soluções:**
```bash
# Instalar todas as dependências
pip install -r requirements.txt

# Ou instalar individualmente
pip install streamlit pandas numpy scikit-learn plotly joblib
```

### 4. "Porta já em uso"

**Soluções:**
```bash
# Usar porta diferente
streamlit run app_final.py --server.port 8502

# Ou matar processo na porta 8501
netstat -ano | findstr :8501
taskkill /PID <PID_NUMBER> /F
```

## 🔧 Comandos de Diagnóstico

### Verificar Python e pacotes
```bash
python --version
python -c "import streamlit; print('Streamlit OK')"
python -c "import pandas; print('Pandas OK')"
python -c "import numpy; print('Numpy OK')"
python -c "import sklearn; print('Sklearn OK')"
```

### Testar modelo
```bash
python demo.py
```

### Verificar arquivos
```bash
dir modelo_carf_rf.pkl
dir preprocessors.pkl
dir app_final.py
```

## 🚀 Execução Recomendada

### Passo a passo completo:

1. **Instalar dependências:**
```bash
pip install streamlit pandas numpy scikit-learn plotly joblib
```

2. **Treinar modelo:**
```bash
cd notebooks
python train_model.py
cd ..
```

3. **Testar modelo:**
```bash
python demo.py
```

4. **Executar aplicação:**
```bash
streamlit run app_final.py
```

5. **Acessar no navegador:**
```
http://localhost:8501
```

## 📱 URLs de Acesso

- **Aplicação principal:** http://localhost:8501
- **Teste simples:** http://localhost:8504 (se executar teste_streamlit.py)
- **Porta alternativa:** http://localhost:8502

## 🆘 Se nada funcionar

1. **Reinstalar tudo:**
```bash
pip uninstall streamlit pandas numpy scikit-learn plotly joblib
pip install streamlit pandas numpy scikit-learn plotly joblib
```

2. **Usar ambiente virtual:**
```bash
python -m venv venv
venv\Scripts\activate
pip install streamlit pandas numpy scikit-learn plotly joblib
streamlit run app_final.py
```

3. **Executar apenas a demonstração:**
```bash
python demo.py
```

## 📞 Suporte

Se os problemas persistirem:
1. Verifique a versão do Python (recomendado: 3.8+)
2. Execute `python demo.py` para testar o modelo
3. Use `streamlit run teste_streamlit.py` para testar o Streamlit
4. Verifique se não há firewall bloqueando a porta 8501
