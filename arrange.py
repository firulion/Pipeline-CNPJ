from ast import Break
from dataclasses import replace
import numpy as np
import pandas as pd


def validaCNPJ(cnpj):           # Converter cnpj em lista para tratamento na função
    if len(cnpj) != 14:
        return False

    cnpj_list = list(map(int,cnpj))
    cnpjverify = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    cnpj_cv = []
    for number1, number2 in zip(cnpjverify, cnpj_list[0:12]):
        cnpj_cv.append(number1*number2)
        soma = sum(cnpj_cv)
        
    if soma%11 < 2:                    
        if cnpj_list[12] != 0:
            return False

    resto = soma%11
    if (11-resto != cnpj_list[12]):
        if soma%11 > 2:
            return False
    cnpjverify2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    cnpj_cv2 = []
    for number3, number4 in zip(cnpjverify2, cnpj_list[0:13]):
        cnpj_cv2.append(number3*number4)
    soma2 = sum(cnpj_cv2)
    if soma2%11 < 2:
        if cnpj_list[13] == 0:
            return True
    elif (11-(soma2%11) == cnpj_list[13]):
        return True
    else:
        return False


df = pd.read_csv("estab-part-00.csv")


# Criando coluna com cnpj completo para fazer validação
df['cod_identificador_matriz_filial']=df['cod_identificador_matriz_filial'].apply(lambda x: str(x).zfill(4))
df['cnpj_dv']=df['cnpj_dv'].apply(lambda x: str(x).zfill(2))
df['cnpj_total']=df['cnpj_basico'].astype(str)+df['cod_identificador_matriz_filial'].astype(str)+df['cnpj_dv'].astype(str)

#print (df['cnpj_total'].head(10))

# Criando coluna que indica se o cnpj é válido ou não através da função validaCNPJ
df['cnpj_valido'] = df.apply(lambda row : validaCNPJ(row['cnpj_total']), axis = 1)

#print (df['cnpj_valido'].head(30))


#Criando tabela auxiliar para dividir os cod_...secundaria
newdf = df[['cnpj_basico','cod_cnae_fiscal_secundaria']]

newdf['cod_cnae_fiscal_secundaria'] = newdf['cod_cnae_fiscal_secundaria'].str.replace('|', ',', regex = True)
newdf['cod_cnae_fiscal_secundaria'] = newdf['cod_cnae_fiscal_secundaria'].str.split(',')    # Separa a string pela ',' gerando uma lista


newdf = newdf.apply( pd.Series.explode )    # "Explode" o novo data frame, transformando a lista gerada em novas linhas na tabela
  

#print(newdf.head(60))