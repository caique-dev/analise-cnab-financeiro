import pandas as pd
from datetime import datetime

# Caminho do arquivo CNAB
CAMINHO_CNAB = './REMFIDC11042025143341.txt'

# Data da cessão (extraída do nome do arquivo)
DATA_CESSAO = datetime.strptime("11042025", "%d%m%Y")

# função que calcula o valor de aquisicao
def val_aquis(val_titulo, taxa_cessao, n):
    return val_titulo/pow((1+taxa_cessao), (n/360))

# Lê o arquivo e processa as linhas
registros = []
with open(CAMINHO_CNAB, 'r', encoding='utf-8') as f:
    linhas = f.readlines()[1:]  # pula o header
    linhas = linhas[:len(linhas)-1] # remove o tail

for i, linha in enumerate(linhas):
    # print('linha ', i)
    cnpj_cpf = linha[220:234].strip()
    tipo_pessoa = linha[218:220].strip()
    nome_sacado = linha[234:263].strip()
    valor_titulo = int(linha[126:139])/100 # gerando duas casas decimais
    taxa_cessao = int(linha[109:114]) / 1000  # gerando tres casas decimais
    data_vencimento = datetime.strptime(linha[120:126], "%d%m%y")
    uf = linha[349:351].strip()
    
    dias_ate_venc = (data_vencimento - DATA_CESSAO).days
    valor_aquisicao = val_aquis(valor_titulo, taxa_cessao, dias_ate_venc)

    registros.append({
        "cnpj_cpf": cnpj_cpf,
        "tipo_pessoa": 'PF' if (tipo_pessoa == '01') else 'PJ',
        "nome": nome_sacado,
        "valor_titulo": valor_titulo,
        "taxa_cessao": taxa_cessao,
        "vencimento": data_vencimento,
        "dias_ate_venc": dias_ate_venc,
        "valor_aquisicao": valor_aquisicao,
        "uf": uf
    })


# Cria DataFrame
df = pd.DataFrame(registros)
# salvando cpf como string
df['cnpj_cpf']=df['cnpj_cpf'].apply(lambda x: f"'{x}'").astype("string")
# print(df.cnpj_cpf.head())

# Salva como CSV para conferência
df.to_csv('./infos_extraidas.csv', index=False)
