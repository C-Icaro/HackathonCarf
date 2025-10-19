# LexCarf - CARF ML Predictor Expandido

O projeto LexCarf é um sistema de apoio a decisão estratégica para o CARF, utilizando machine learning para prever **duas dimensões** dos resultados dos processos:

## 🎯 Objetivos

### 1. **Probabilidade de Provimento**
- **Provido Total**: Recurso totalmente aceito
- **Negado**: Recurso rejeitado

### 2. **Tipo de Votação** (apenas para provimentos)
- **Unânime**: Todos os conselheiros concordam
- **Maioria**: Maioria dos conselheiros concorda  
- **Qualidade**: Decisão por voto de qualidade do presidente

## 🚀 Como Executar

### Opção 1: Aplicação Web Expandida (Recomendada)
```bash
streamlit run app_expandido.py
```

### Opção 2: Demonstração em Linha de Comando
```bash
python demo_expandido.py
```

### Opção 3: Treinar Modelos Novamente
```bash
cd notebooks
python train_model_expandido.py
cd ..
```

### Opção 4: Aplicação Original
```bash
streamlit run app_final.py
```

## 📊 Tecnologias Utilizadas

- **Python 3.8+**
- **Scikit-learn**: Machine Learning
- **Streamlit**: Interface Web
- **Pandas**: Manipulação de Dados
- **Plotly**: Visualizações
- **TF-IDF**: Processamento de Texto

## 📁 Estrutura do Projeto

```
├── dados/
│   └── carf_julgamentos_2024.csv    # Dados de treinamento
├── notebooks/
│   └── notebook.ipynb              # Notebook de treinamento
├── assets/                          # Imagens e recursos
├── app.py                          # Aplicação Streamlit
├── run_app.py                      # Script de execução
├── requirements.txt                # Dependências
└── README.md                       # Este arquivo
```

## 🔧 Modelos Implementados

### Modelo de Provimento:
- **Algoritmo**: Random Forest Classifier
- **Classes**: Provido Total, Negado
- **Acurácia**: 80%
- **Dados**: 20.081 processos de 2024

### Modelo de Votação:
- **Algoritmo**: Random Forest Classifier  
- **Classes**: Unânime, Maioria, Qualidade
- **Acurácia**: 90%
- **Dados**: 11.228 processos de provimento

### Features Comuns:
- **Tributo** + **Turma** + **Embeddings de texto** (TF-IDF)
- **Validação**: Divisão 80/20 treino/teste

## 📈 Performance

O modelo foi treinado com dados reais do CARF 2024 e consegue identificar padrões nos textos jurídicos das ementas, combinando informações categóricas (tributo, turma) com análise semântica do conteúdo.

## 💡 Exemplos de Resultados

### Exemplo 1: IRPF
- **Provimento**: Negado (60.0%) ❌
- **Votação**: Unânime (63.5%) (não aplicável)
- **Resultado**: Recurso provavelmente será negado

### Exemplo 2: COFINS  
- **Provimento**: Provido Total (64.9%) ✅
- **Votação**: Unânime (59.0%) 🗳️
- **Resultado**: Provido Total por Unânime (confiança: 61.9%)

### Exemplo 3: IRPJ
- **Provimento**: Negado (63.8%) ❌
- **Votação**: Unânime (55.9%) (não aplicável)
- **Resultado**: Recurso provavelmente será negado

## 🎯 Aplicação Web

A interface web expandida (`app_expandido.py`) permite:
- ✅ **Duas dimensões**: Provimento + Tipo de Votação
- ✅ **Métricas visuais**: Probabilidades em formato de métricas
- ✅ **Resumo combinado**: Resultado esperado com confiança
- ✅ **Exemplos pré-definidos**: Para teste rápido
- ✅ **Design responsivo**: Interface moderna e intuitiva

## Equipe:


 <div align="left">
  <table>
    <tr >
     <td><b>Analistas de domínio:</b></td>
  <td align="center"><a href="https://www.linkedin.com/in/vicky-auricchio-saes-0a496a243/"><img style="border-radius:5%;" src="assets/fotos/Vicky.jpg" width="100px;" alt="Vicky Auricchio Saes - Foto" /><br><sub><b>Vicky Auricchio</b><br>Direito, FGV</sub></a></td>
  <td align="center"><a href="https://www.linkedin.com/in/lavinia-mendonca/"><img style="border-radius: 5%;" src="assets/fotos/Amanda.jpg" width="100px;" alt="Lavínia Mendonça - Foto" /><br><sub><b>Lavínia Mendonça</b><br>Administração Tecnológica, Inteli</sub></a></td>

  </table>
</div>

<div align="left">
  <table>
    <tr>
      <td><b>Analistas de dados:</b></td>
      <td align="center"><a href="https://www.linkedin.com/in/carlosicaro"><img style="border-radius: 5%;" src="assets/fotos/Carlos.png" width="100px;" alt="Carlos Icaro Kauã Coelho Paiva - Foto" /><br><sub><b>Carlos Icaro</b><br>Eng. da Computação, Inteli</sub></a></td>
      <td align="center"><a href="https://www.linkedin.com/in/amandadarosa/"><img style="border-radius: 5%;" src="assets/fotos/Amanda.jpg" width="100px;" alt="Amanda Cristina da Rosa - Foto" /><br><sub><b>Amanda Cristina</b><br>Eng. da Computação, Inteli</sub></a></td>
    </tr>
  </table>
</div>

## Realizado durante o HackathonCARF.

O HackathonCARF é uma realização conjunta do Conselho Adminstrativo de Recursos Fiscais (CARF) com a Universidade Federal da Bahia (UFBA) realizado entre os dias 16 e 19 de outubro de 2025. O objetivo é a criação de um ambiente propício para a criação de novas tecnologias que visem aumentar a eficiência do CARF.

<div align="center" style="height: 240px; overflow: hidden;">
  <img src="./assets/BannerCarf.jpg" alt="Hackathon Carf - Foto" style="width: 60%; height: 100%; object-fit: cover; object-position: center top;" />
</div>
