#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt


# In[2]:


# campos do df: cnpj_cpf tipo_pessoa nome  valor_titulo  taxa_cessao  vencimento  dias_ate_venc  valor_aquisicao  uf
# gerando dataframe com as informacoes extraidas
df = pd.read_csv('infos_extraidas.csv')

# removendo aspas desnecessarias
df['cnpj_cpf'] = df['cnpj_cpf'].astype(str).str.strip("'")


# In[3]:




# ## Calculando o Valor Total de Aquisição da Cessão 

# In[4]:




# In[5]:


# calculando valor total de aquisicao da cessao 
VAL_TOTOAL = df['valor_aquisicao'].sum()


# ## Soma do Valor de Face dos 5 sacados com maior Volume 

# In[6]:


# dividindo os grupos
grupos = df.groupby('cnpj_cpf')


# In[7]:


df_volume_faces = df.drop_duplicates(subset='cnpj_cpf')[['cnpj_cpf', 'tipo_pessoa', 'uf', 'nome']]

# Zera os valores
df_volume_faces['volume_faces'] = 0

# definindo o tipo certo para a coluna
df_volume_faces['volume_faces'] = df_volume_faces['volume_faces'].astype('float')

# Garante que os nomes de colunas estão limpos
df_volume_faces.columns = df_volume_faces.columns.str.strip()


# In[8]:




# In[9]:


# verificando os tipo


# In[10]:


# Define o índice como cnpj_cpf - remove essa coluna do df
df_volume_faces.set_index('cnpj_cpf', inplace=True)


# In[11]:




# In[12]:


# somando os valores de face de cada grupo(cada cpf/cnpj)
for doc, gp in grupos:
    soma = gp.valor_titulo.sum()
    doc = doc.strip("'")
    df_volume_faces.loc[doc, 'volume_faces'] = soma


# In[13]:




# In[14]:


# ordenando o df pelo valor da soma dos títulos
TOP5_DEVEDORES = df_volume_faces.sort_values(by='volume_faces', ascending=False)


# In[15]:




# In[16]:


# separando o top5
row_slice = slice(0,5)
TOP5_DEVEDORES = TOP5_DEVEDORES[row_slice]


# In[17]:




# In[18]:


TOP5_DEVEDORES.to_clipboard()


# ## Calculando Numero de Créditos de PJ e PF 

# In[19]:


contagens = df['tipo_pessoa'].value_counts(dropna=False)


# In[20]:


CREDITOS_PF = int(contagens['PF'])
CREDITOS_PJ = int(contagens['PJ'])



# ## Calculando Ticket médio de PF e PJ 

# In[21]:


grupos = df.groupby('tipo_pessoa')


# In[22]:


numero_titulos_pj = grupos.size()['PJ']
soma_faces_pj = grupos['valor_titulo'].sum()['PJ']

TICKET_MEDIO_PJ = soma_faces_pj/numero_titulos_pj



# In[23]:


numero_titulos_pf = grupos.size()['PF']
soma_faces_pf = grupos['valor_titulo'].sum()['PF']

TICKET_MEDIO_PF = soma_faces_pj/numero_titulos_pf



# ## Calculando Prazo médio de vencimento 

# In[24]:


PRAZO_MEDIO_GERAL = df['dias_ate_venc'].mean()


# In[25]:


# Separando os grupos
grupos = df.groupby('tipo_pessoa')


# In[26]:


# dados sobre PJ
PRAZO_MEDIO_PJ = grupos.get_group('PJ')['dias_ate_venc'].mean()


# In[27]:


# dados sobre PF
PRAZO_MEDIO_PF = grupos.get_group('PF')['dias_ate_venc'].mean()


# ## Plotando um gráfico do valor de aquisição pela data de vencimento dos créditos da cessão 

# In[28]:




# In[29]:


df_agrupado = df.groupby('vencimento')['valor_aquisicao'].sum().reset_index()


# In[30]:




# In[31]:


df_agrupado = df.groupby('vencimento')['valor_aquisicao'].sum().reset_index()
df_agrupado = df_agrupado.sort_values('vencimento')
df_agrupado['vencimento'] = pd.to_datetime(df_agrupado['vencimento'])  # se necessário
df_agrupado['vencimento_str'] = df_agrupado['vencimento'].dt.strftime('%d/%m/%y')

plt.figure(figsize=(16, 6))
plt.plot(df_agrupado['vencimento_str'], df_agrupado['valor_aquisicao'], marker='o')
plt.title('Valor de Aquisição por Data de Vencimento')
plt.xlabel('Data de Vencimento')
plt.xticks(fontsize=5)
plt.ylabel('Valor de Aquisição (R$)')
plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()
plt.show()


# In[32]:




# In[33]:


df_agrupado.to_csv('./mapa_interativo/dados_grafico.csv')


# ## Coletando dados necessários para indicar a dispersão geográfica dos créditos

# In[34]:


n_creditos_uf = df.groupby('uf').size()
df_agrupado_uf = df.groupby('uf')[['valor_titulo', 'valor_aquisicao']].sum().reset_index()
df_agrupado_uf.columns = ['uf', 'valor_face', 'valor_aquisicao']
df_agrupado_uf['valor_medio_face'] = df_agrupado_uf['valor_face'] / n_creditos_uf.values
df_agrupado_uf['valor_medio_aquisicao'] = df_agrupado_uf['valor_aquisicao'] / n_creditos_uf.values
df_agrupado_uf = df_agrupado_uf.merge(n_creditos_uf.rename('n_creditos'), on='uf')




# In[35]:




# In[36]:


extremos = df.groupby('uf')[['valor_titulo', 'valor_aquisicao']].agg(['max', 'min']).reset_index()
extremos.columns = ['uf', 
                    'valor_face_max', 'valor_face_min', 
                    'valor_aquisicao_max', 'valor_aquisicao_min']



# In[37]:


df_agrupado_uf = df_agrupado_uf.merge(extremos, on='uf')


# In[38]:




# In[40]:


df_agrupado_uf.to_csv('./mapa_interativo/dados_mapa_clean.csv')

