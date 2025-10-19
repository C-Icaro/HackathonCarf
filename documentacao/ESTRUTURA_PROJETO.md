# 📁 Estrutura do Projeto CARF ML Predictor

## 🎯 Organização do Repositório

O repositório foi organizado de forma modular e intuitiva para facilitar a navegação e manutenção:

```
HackathonCarf/
├── 🚀 run.py                    # Execução principal do sistema
├── 📋 README.md                 # Documentação principal
├── 📦 requirements.txt          # Dependências Python
├── 🚫 .gitignore               # Arquivos ignorados pelo Git
│
├── 📱 aplicacoes/               # Aplicações e interfaces
│   ├── app_2023_2024.py        # ⭐ Aplicação principal (sem vazamento)
│   ├── demo_2023_2024.py       # Demonstração em linha de comando
│   ├── executar_plataforma.py  # Script de execução automatizada
│   ├── app_expandido.py        # Versão expandida (legado)
│   ├── app_final.py            # Versão final (legado)
│   ├── app_simples.py          # Versão simplificada (legado)
│   ├── app.py                  # Versão original (legado)
│   ├── demo_expandido.py       # Demo expandida (legado)
│   ├── demo.py                 # Demo original (legado)
│   └── teste_streamlit.py      # Teste básico do Streamlit
│
├── 🤖 modelos/                 # Modelos treinados
│   ├── modelo_carf_provimento_2023.pkl  # ⭐ Modelo de provimento (2023)
│   ├── modelo_carf_votacao_2023.pkl     # ⭐ Modelo de votação (2023)
│   ├── preprocessors_2023.pkl          # ⭐ Pré-processadores (2023)
│   ├── modelo_carf_provimento.pkl      # Modelo expandido (legado)
│   ├── modelo_carf_votacao.pkl          # Modelo expandido (legado)
│   ├── preprocessors_expandido.pkl     # Pré-processadores expandidos (legado)
│   ├── modelo_carf_rf.pkl              # Modelo original (legado)
│   └── preprocessors.pkl               # Pré-processadores originais (legado)
│
├── 📊 dados/                    # Datasets
│   ├── carf_2023_sem_vazamento.csv    # ⭐ Dados de treinamento (2023)
│   ├── carf_sem_vazamento.csv         # ⭐ Dados de teste (2024)
│   ├── carf_julgamentos_2023.csv      # Dados originais 2023
│   ├── carf_julgamentos_2024.csv      # Dados originais 2024
│   ├── carf_julgamentos_2024_exemplo.csv
│   ├── CARF_Julgamentos_2022.csv
│   ├── CARF_Julgamentos_2019.csv
│   └── CARF_Julgamentos_2018.csv
│
├── 🔧 scripts/                  # Scripts de análise e processamento
│   ├── analise_2023.py          # Análise dos dados de 2023
│   ├── detectar_vazamento_2023.py # Detecção de vazamento em 2023
│   ├── verificar_dataset_limpo.py  # Verificação de qualidade
│   ├── analise_provimento.py    # Análise de provimento (legado)
│   ├── detectar_vazamento.py    # Detecção de vazamento (legado)
│   └── run_carf_app.py          # Script de execução (legado)
│
├── 📚 notebooks/                # Notebooks de desenvolvimento
│   ├── train_model_2023_2024.py # ⭐ Treinamento principal (2023/2024)
│   ├── train_model_expandido.py # Treinamento expandido (legado)
│   └── train_model.py           # Treinamento original (legado)
│
├── 📖 documentacao/             # Documentação
│   ├── COMO_EXECUTAR.md         # Instruções de execução
│   ├── RESUMO_2023_2024.md      # Resumo do projeto 2023/2024
│   ├── ANALISE_VAZAMENTO.md    # Análise de vazamento
│   ├── INSTRUCOES_FINAIS.md    # Instruções finais
│   ├── RESUMO_EXPANDIDO.md     # Resumo expandido (legado)
│   ├── RESUMO_FINAL.md          # Resumo final (legado)
│   ├── RESULTADOS.md            # Resultados (legado)
│   ├── TROUBLESHOOTING.md       # Solução de problemas
│   └── README.md                # README antigo (legado)
│
├── 🎨 assets/                   # Recursos visuais
│   ├── BannerCarf.jpg          # Banner do projeto
│   ├── Mapa estratégico do CARF.png
│   └── fotos/                   # Fotos da equipe
│       ├── Amanda.jpg
│       ├── Carlos.png
│       └── Vicky.jpg
│
└── 📁 documents/                # Documentos adicionais
    └── wad.md
```

## 🎯 Arquivos Principais (⭐)

### **Execução:**
- `run.py` - Execução principal do sistema

### **Aplicação:**
- `aplicacoes/app_2023_2024.py` - Interface web principal

### **Modelos:**
- `modelos/modelo_carf_provimento_2023.pkl` - Modelo de provimento
- `modelos/modelo_carf_votacao_2023.pkl` - Modelo de votação
- `modelos/preprocessors_2023.pkl` - Pré-processadores

### **Dados:**
- `dados/carf_2023_sem_vazamento.csv` - Dados de treinamento
- `dados/carf_sem_vazamento.csv` - Dados de teste

### **Treinamento:**
- `notebooks/train_model_2023_2024.py` - Script de treinamento

## 📋 Convenções de Nomenclatura

### **Arquivos Principais:**
- `*_2023_2024.*` - Versão atual (sem vazamento)
- `*_expandido.*` - Versão expandida (legado)
- `*_final.*` - Versão final (legado)

### **Diretórios:**
- `aplicacoes/` - Interfaces e aplicações
- `modelos/` - Modelos treinados
- `dados/` - Datasets
- `scripts/` - Scripts de processamento
- `notebooks/` - Notebooks de desenvolvimento
- `documentacao/` - Documentação
- `assets/` - Recursos visuais

## 🚀 Como Usar

### **Execução Principal:**
```bash
python run.py
```

### **Execução Direta:**
```bash
python -m streamlit run aplicacoes/app_2023_2024.py
```

### **Demonstração:**
```bash
python aplicacoes/demo_2023_2024.py
```

## 🔄 Manutenção

### **Adicionar Novos Modelos:**
1. Colocar arquivos `.pkl` em `modelos/`
2. Atualizar `run.py` se necessário

### **Adicionar Novas Aplicações:**
1. Colocar arquivos `.py` em `aplicacoes/`
2. Atualizar documentação

### **Adicionar Novos Scripts:**
1. Colocar arquivos `.py` em `scripts/`
2. Documentar funcionalidade

### **Adicionar Documentação:**
1. Colocar arquivos `.md` em `documentacao/`
2. Atualizar `README.md` principal

---

**📁 Repositório organizado e pronto para uso!**

A estrutura modular facilita a navegação, manutenção e expansão do projeto.
