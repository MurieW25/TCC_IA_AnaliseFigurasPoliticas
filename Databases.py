
import requests
import pandas as pd
from IPython.display import display

from DadosAbertosBrasil import ipea

bases_economia = {}
#bases_educacao = {}
#bases_saude = {}
bases_segurancapublica = {}


# --------------------------------------------------- FUNCOES ADICIONAIS
def padronizaIBGE(df_IBGE, nome):
    df = df_IBGE.rename(columns={
    "D3C": "Data",
    "V": "Valor"})
    df_IBGE["Nome"] = nome
    return df

def padronizar_df_IPEADATA(df, nome):
    df = df.copy()

    df = df.rename(columns={
        "VALDATA": "Data",
        "VALVALOR": "Valor"
    })

    df["Data"] = pd.to_datetime(df["Data"], utc=True)

    df["Nome"] = nome

    df = df[["Nome", "Data", "Valor"]]

    return df

# --------------------------------------------------- INICIO DATABASES ECONOMIA

#BUSCA DATABASES NO SITE DO IPEADATA POR API
# Baixa todos os metadados
url = "https://www.ipeadata.gov.br/api/odata4/Metadados"

dados = requests.get(url).json()["value"]

meta = pd.DataFrame(dados)

#print("Quantidade de séries:", len(meta))
#print(meta.columns.tolist())

def buscar_serie(texto):
    resultado = meta[
        meta["SERNOME"].str.contains(texto, case=False, na=False)
    ][["SERCODIGO", "SERNOME", "FNTSIGLA", "PERNOME"]]

    return resultado.sort_values("SERNOME")

display(buscar_serie("PIB"))
display(buscar_serie("paridade do poder de compra"))
display(buscar_serie("PIB per capita"))
display(buscar_serie("variação real"))
display(buscar_serie("IPCA"))
display(buscar_serie("expectativa"))
display(buscar_serie("câmbio"))
display(buscar_serie("salário mínimo"))
display(buscar_serie("dívida interna líquida"))

dados = requests.get(url).json()

#print(dados.keys())
#print(len(dados["value"]))

meta_macro = meta[
    (meta["BASNOME"] == "Macroeconômico")
    & (meta["SERSTATUS"] == "A")
]

SERIES_ECONOMIA = {
    # PIB
    "pib": "WEO_PIBWEOBRA",

    # PIB PPC
    "pib_ppc": "WDI_PIBPPCBRA",

    # PIB PPC per capita
    "pib_ppc_percapita": "WDI_PIBPPCCAPBRA",

    # PIB variação real
    "pib_variacao_real": "WEO_PIBRWEOBRA",

    # Expectativa inflação IPCA (6 meses)
    "inflacao_expectativa_6m": "BM12_IPCAEXP612",

    # Câmbio compra/venda
    "cambio_compra": "BM12_MCC12",
    "cambio_venda": "BM12_SFCC12",

    # Salário mínimo
    "salario_minimo_real": "GAC12_SALMINDOL12",

    # PPC salário mínimo
    "salario_minimo_ppc": "GAC12_PPCTAXAC12",
}



def carregar_serie_economia(codigo, nome_serie):
    url = f"https://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{codigo}')"

    try:
        r = requests.get(url, timeout=30)
        data = r.json()

        if "value" not in data or len(data["value"]) == 0:
            print(f"Série vazia: {codigo}")
            return None

        df = pd.DataFrame(data["value"])
        df = padronizar_df_IPEADATA(df, nome_serie)

        if "VALDATA" in df.columns:
            df["VALDATA"] = pd.to_datetime(df["VALDATA"], utc=True)

        return df

    except Exception as e:
        print(f"Erro na série {codigo}: {e}")
        return None

for nome, codigo in SERIES_ECONOMIA.items():
    df = carregar_serie_economia(codigo, nome)
    if df is not None:
        bases_economia[nome] = df
        bases_economia[nome] = (bases_economia[nome].pivot_table(index="Data", columns= "Nome", values="Valor", aggfunc="first").reset_index())
        print(bases_economia[nome].head())

#DATABASES DO BACEN ATRAVÉS DE API - REFERENTE ÀS DÍVIDAS PÚBLICAS

def carregar_bcb(codigo, nome):
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json"

    r = requests.get(url)
    df = pd.DataFrame(r.json())

    df.columns = ["Data", "Valor"]
    df["Data"] = pd.to_datetime(df["Data"], dayfirst=True)
    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")
    df["Nome"] = nome
    df = df[["Nome", "Data", "Valor"]]

    return df

bases_economia["divida_bruta"] = carregar_bcb(13762, "divida_bruta")
bases_economia["divida_liquida"] = carregar_bcb(4505, "divida_liquida")

bases_economia["divida_bruta"] = (bases_economia["divida_bruta"].pivot_table(index="Data", columns= "Nome", values="Valor", aggfunc="first").reset_index())
bases_economia["divida_liquida"] = (bases_economia["divida_liquida"].pivot_table(index="Data", columns= "Nome", values="Valor", aggfunc="first").reset_index())

# --------------------------------------------------- FIM DATABASES ECONOMIA

# --------------------------------------------------- INICIO DATABASES EDUCACAO

# --------------------------------------------------- FIM DATABASES EDUCACAO

# --------------------------------------------------- INICIO DATABASES SAUDE

# ---------------------------------------------------- FIM DATABASES SAUDE

# --------------------------------------------------- INICIO DATABASES SEGURANCA PUBLICA
#código usado para buscar os codigos das databases
# series_segpub = ipea.lista_series(contendo="BUSCA")
#print(series_segpub[['codigo', 'nome']])

SERIES_SEGURANCAPUBLICA = {
    "homicidios_registrados" : "AVIOL12_HOMIC",
    "taxa_homicidios" : "AVIOL12_THOMIC",
}

for nome, codigo in SERIES_SEGURANCAPUBLICA.items():
    try:
        df = ipea.serie(codigo)
    except Exception as e:
        print(f"ERRO NA SERIE {codigo}: {e}")

    if df is not None:
        bases_segurancapublica[nome] = df
        #bases_segurancapublica[nome] = (bases_economia[nome].pivot_table(index="Data", columns= "Nome", values="Valor", aggfunc="first").reset_index())
        print(bases_segurancapublica[nome].head())

# --------------------------------------------------- FIM DATABASES SEGURANCA PUBLICA

class Database:
    def getDatabaseEconomia():
        return bases_economia

    #def getDatabaseEducacao():
    #    return bases_educacao

    #def getDatabaseSaude():
    #    return bases_saude

    #def getDatabaseSegurancaPublica():
    #    return bases_segurancapublica