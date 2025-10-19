# 🚀 Como Executar a Plataforma CARF ML Predictor (Sem Vazamento)

## ✅ **Opção 1: Execução Direta (Recomendada)**

```bash
python -m streamlit run app_2023_2024.py
```

**Acesse:** http://localhost:8501

## ✅ **Opção 2: Script Automatizado**

```bash
python executar_plataforma.py
```

## ✅ **Opção 3: Demonstração em Linha de Comando**

```bash
python demo_2023_2024.py
```

---

## 📊 **Sobre a Plataforma Sem Vazamento**

### **Modelos Treinados:**
- **Dados de treinamento**: 2023 (13.470 registros limpos)
- **Dados de teste**: 2024 (16.066 registros limpos)
- **Vazamento removido**: ~38% dos registros

### **Performance Real:**
- **Modelo de Provimento**: 75% acurácia
- **Modelo de Votação**: 87% acurácia
- **Validação**: Dados de 2023 vs 2024

### **Funcionalidades:**
- ✅ Predição de Provimento (Total/Negado)
- ✅ Predição de Tipo de Votação (Unânime/Maioria/Qualidade/Empate)
- ✅ Interface web moderna
- ✅ Exemplos pré-definidos
- ✅ Métricas de performance

---

## 🔧 **Arquivos Necessários**

- `app_2023_2024.py` - Aplicação principal
- `modelo_carf_provimento_2023.pkl` - Modelo de provimento
- `modelo_carf_votacao_2023.pkl` - Modelo de votação
- `preprocessors_2023.pkl` - Componentes de pré-processamento

---

## 🆘 **Solução de Problemas**

### **Se der erro "streamlit não encontrado":**
```bash
pip install streamlit
```

### **Se der erro "modelo não encontrado":**
```bash
cd notebooks
python train_model_2023_2024.py
cd ..
```

### **Se der erro de porta ocupada:**
```bash
python -m streamlit run app_2023_2024.py --server.port 8502
```

---

## 🎯 **URLs de Acesso**

- **Aplicação Principal**: http://localhost:8501
- **Porta Alternativa**: http://localhost:8502

---

**🎉 Plataforma Pronta para Uso!**

A plataforma está configurada com modelos treinados em dados de 2023 e validados em dados de 2024, garantindo alta qualidade e ausência de vazamento de informação.
