from Databases import Database
import pandas as pd
import numpy as np

bases_economia = Database.getDatabaseEconomia()

#as flags serão utilizadas para realizar o treino da IA, variação usada para realizar o desconto/soma de pontos

bases_economia_flags = {}

invertidas={"cambio_compra", "inflacao_expectativa_6m", "divida_bruta", "divida_liquida"}

for nome_base, df in bases_economia.items():

    coluna_valor = [c for c in df.columns if c != "Data"][0]

    coluna_variacao = f"Variacao_{coluna_valor}"
    coluna_flag = f"Flag_{coluna_valor}"

    df_flag = df[["Data"]].copy()

    df_flag[coluna_variacao] = pd.to_numeric(df[coluna_valor], errors="coerce").diff()

    flag = np.sign(df_flag[coluna_variacao])
    if coluna_valor in invertidas:
        flag = -flag

    df_flag[coluna_flag] = (flag.fillna(0).astype(int))

    bases_economia_flags[nome_base] = df_flag

for nome_base, df in bases_economia_flags.items():
    print(df.head())

#bases_IBGE_flags = {}

class Flags:
    def getFlagsEconomia():
        return bases_economia_flags