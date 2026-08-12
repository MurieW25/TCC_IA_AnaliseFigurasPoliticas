from Databases import Database
import pandas as pd
import numpy as np

bases_economia = {}
#bases_educacao = {}
#bases_saude = {}
bases_segurancapublica = {}

#as flags serão utilizadas para realizar o treino da IA, variação usada para realizar o desconto/soma de pontos

bases_economia_flags = {}
#bases_educacao_flags = {}
#bases_saude_flags = {}
bases_segurancapublica_flags = {}

invertidas={}

def calculaFlags(db, db_flags):
    for nome_base, df in db.items():

        coluna_valor = [c for c in df.columns if c != "Data"][0]

        coluna_variacao = f"Variacao_{coluna_valor}"
        coluna_flag = f"Flag_{coluna_valor}"

        df_flag = df[["Data"]].copy()

        df_flag[coluna_variacao] = pd.to_numeric(df[coluna_valor], errors="coerce").diff()

        flag = np.sign(df_flag[coluna_variacao])
        if coluna_valor in invertidas:
            flag = -flag

        df_flag[coluna_flag] = (flag.fillna(0).astype(int))

        db_flags[nome_base] = df_flag

def printFlags(db):
    for nome_base, df in db.items():
        print(df.head())

class Flags:
    def getFlagsEconomia():
        bases_economia = Database.getDatabaseEconomia()
        invertidas={"cambio_compra", "inflacao_expectativa_6m", "divida_bruta", "divida_liquida"}
        calculaFlags(bases_economia, bases_economia_flags)
        return bases_economia_flags

    #def getFlagsEducacao():
    #    bases_educacao = Database.getDatabaseEducacao()
    #    return bases_educacao_flags

    #def getFlagsSaude():
    #    bases_saude = Database.getDatabaseSaude()
    #    return bases_saude_flags

    def getFlagsSegurancaPublica():
        bases_segurancapublica = Database.getDatabaseSegurancaPublica()
        for nome_base, df in Database.getDatabaseSegurancaPublica().items():
            invertidas = [c for c in df.columns if c != "Data"][0]
        calculaFlags(bases_segurancapublica, bases_segurancapublica_flags)
        return bases_segurancapublica_flags