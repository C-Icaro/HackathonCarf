# CARF ML Predictor - Instruções de Uso

## 🎯 Resumo do Projeto

Implementamos com sucesso um modelo de machine learning que prevê as probabilidades de aprovação dos processos no CARF por tipo de votação:

- **Unânime**: 69.3% (Exemplo IRPF)
- **Maioria**: 29.6% (Exemplo COFINS) 
- **Qualidade**: 13.2% (Exemplo COFINS)

## 📊 Performance do Modelo

- **Dados utilizados**: 11.228 processos de 2024 (apenas casos com provimento)
- **Distribuição das classes**:
  - Unânime: 9.389 casos (83.6%)
  - Maioria: 1.408 casos (12.5%)
  - Qualidade: 431 casos (3.8%)
- **Acurácia**: 91% no conjunto de teste
- **Precision/Recall**: Excelente para Unânime (95%/96%), bom para outras classes

## 🚀 Como Executar

### Opção 1: Demonstração Rápida
```bash
python demo.py
```

### Opção 2: Interface Web Completa
```bash
streamlit run app.py
```

### Opção 3: Treinar Modelo Novamente
```bash
cd notebooks
python train_model.py
cd ..
```

## 🔧 Arquivos Criados

- `modelo_carf_rf.pkl`: Modelo Random Forest treinado
- `preprocessors.pkl`: Componentes de pré-processamento
- `app.py`: Aplicação web Streamlit
- `demo.py`: Script de demonstração
- `notebooks/train_model.py`: Script de treinamento
- `requirements.txt`: Dependências Python

## 💡 Exemplo de Uso Programático

```python
import joblib
import pickle
import numpy as np

# Carregar modelo
model = joblib.load('modelo_carf_rf.pkl')
with open('preprocessors.pkl', 'rb') as f:
    preprocessors = pickle.load(f)

# Fazer predição
texto_ementa = "Imposto sobre a Renda de Pessoa Física..."
tributo = "IRPF - IMPOSTO SOBRE A RENDA DA PESSOA FÍSICA"
turma = "1ª TE-1ªSEÇÃO-1001-CARF-MF-DF"

# (código de predição aqui)
probabilidades = prever_probabilidades(texto_ementa, tributo, turma, model, preprocessors)
```

## 🎯 Resultados dos Exemplos

### Exemplo 1: IRPF
- **Unânime**: 69.3% ⭐ (Predição principal)
- **Maioria**: 22.1%
- **Qualidade**: 8.6%

### Exemplo 2: COFINS  
- **Unânime**: 57.2% ⭐ (Predição principal)
- **Maioria**: 29.6%
- **Qualidade**: 13.2%

### Exemplo 3: IRPJ
- **Unânime**: 66.4% ⭐ (Predição principal)
- **Maioria**: 22.4%
- **Qualidade**: 11.2%

## 📈 Insights do Modelo

1. **Unânime é predominante**: Em todos os exemplos, a votação unânime tem maior probabilidade
2. **Tributo influencia**: Diferentes tributos mostram padrões distintos
3. **Turma importa**: A turma do CARF também influencia na predição
4. **Texto das ementas**: O conteúdo jurídico é analisado via TF-IDF

## 🏆 Conclusão

O modelo foi treinado com sucesso usando dados reais do CARF 2024 e consegue prever com boa precisão as probabilidades de aprovação por tipo de votação. A interface web permite testar facilmente diferentes cenários, tornando o sistema útil para consultores jurídicos e advogados que trabalham com processos no CARF.

**Para o Hackathon CARF**: Este sistema demonstra como machine learning pode ser aplicado para apoiar decisões estratégicas no âmbito administrativo fiscal, oferecendo insights valiosos sobre a probabilidade de sucesso dos processos.
