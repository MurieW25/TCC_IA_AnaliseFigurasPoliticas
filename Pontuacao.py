from Flags import Flags
import pandas as pd
import numpy as np

#DATA FRAME INICIAL COM OS PERIODOS DE CADA FIGURA POLÍTICA

data_frame_1 = {
    "Nome": [
        'José Sarney',
        'Fernando Collor',
        'Itamar Franco',
        'Fernando Henrique Cardoso',
        'Luiz Inácio Lula da Silva',
        'Dilma Rousseff',
        'Michel Temer',
        'Jair Bolsonaro',
        'Luiz Inácio Lula da Silva'
    ],
    "Inicio_periodo_efetivo": [
        '15/03/1985',
        '15/03/1990',
        '29/12/1992',
        '01/01/1995',
        '01/01/2003',
        '01/01/2011',
        '31/08/2016',
        '01/01/2019',
        '01/01/2023'
    ],
    "Fim_periodo_efetivo": [
        '15/03/1990',
        '29/12/1992',
        '01/01/1995',
        '01/01/2003',
        '01/01/2011',
        '31/08/2016',
        '01/01/2019',
        '01/01/2023',
        '01/01/2027'
    ]
}

df = pd.DataFrame(data_frame_1)

print(df)
database_pontuar = Flags.getFlagsSegurancaPublica()

#DEFININDO DATABASE DAS PONTUAÇÕES
df_pontuacao = pd.DataFrame(data_frame_1)

#Formatação das datas
df_pontuacao["Inicio_periodo_efetivo"] = pd.to_datetime(
    df_pontuacao["Inicio_periodo_efetivo"],
    format="%d/%m/%Y"
)

df_pontuacao["Fim_periodo_efetivo"] = pd.to_datetime(
    df_pontuacao["Fim_periodo_efetivo"],
    format="%d/%m/%Y"
)

#Duração em anos
anos_mandato = ( (df_pontuacao["Fim_periodo_efetivo"] - df_pontuacao["Inicio_periodo_efetivo"]).dt.days / 365.25 )

#Definindo pontuação inicial
df_pontuacao["pontos_inicial"] = (500 * (anos_mandato / 4)).astype(int)

print(df_pontuacao)

df_pontuacao["pontos_final"] = 0

MULT_BASE = 0.05
ADIT_BASE = 5

dados_multiplicativos = ["divida_bruta", "divida_liquida", "taxa_homicidios", "taxa_suicidios"]

for idx, row in df_pontuacao.iterrows():

    inicio = row["Inicio_periodo_efetivo"]
    fim = row["Fim_periodo_efetivo"]

    pontos = float(row["pontos_inicial"])

    meses_periodo = pd.date_range(start=inicio, end=fim, freq="MS")

    for mes in meses_periodo:

        v_mult = 0.0
        v_adit = 0.0

        for nome_base, df in database_pontuar.items():

            df_mes = df[df["Data"].dt.to_period("M") == mes.to_period("M")]

            if df_mes.empty:
                continue

            for col in df_mes.columns:

                if not col.startswith("Flag_"):
                    continue

                flag = int(df_mes[col].values[0])

                var = col.replace("Flag_", "")

                if var in dados_multiplicativos:
                    v_mult += MULT_BASE * flag
                else:
                    v_adit += ADIT_BASE * flag

        pontos = pontos * (1 + v_mult) + v_adit

    df_pontuacao.loc[idx, "pontos_final"] = round(pontos)

print(df_pontuacao[["Nome", "pontos_inicial", "pontos_final"]])