# PS Caique Andrade - Questão 1
## Contato (Qualquer dúvida ou dificuldade, só me avisar)
1. [Linkedin](https://www.linkedin.com/in/caique-p-andrade)
2. [Github](https://github.com/caique-dev)
3. Email: [c204677@dac.unicamp.br](mailto:c204677@dac.unicamp.br)

---

## ✅ Pré-requisitos

- [Python 3.7+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- (Opcional) [virtualenv](https://virtualenv.pypa.io/en/latest/) para criar ambientes isolados

---

## Para Abrir o Dashboard
### 1. Dentro da raiz do projeto, execute:
```bash
cd ./mapa_interativo && python -m http.server 8000
```
### 2. Pelo navegador, entre em [localhost](http://localhost:8000/)

## Para gerar todos os arquivos utilizados pelo index.html:
1. Rode o arquivo extrai_informaloes.py
2. Rode o arquivo notebook_analiza_informacoes.ipynb ou o analiza_informacoes.py
    1. O primeiro arquivo contém o passo a passo da análise que fiz, enquanto o segundo é mais direto
3. Abra o Dashboard

## 🚀 Passo a passo para rodar o notebook (opcional)
### 2. (Opcional) Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3. Instale as dependências

```bash
pip install notebook
```

### 4. Instale a [extensão no vscode](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter])
