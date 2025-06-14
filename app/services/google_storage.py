import os
import pandas as pd
from google.cloud import storage
from io import BytesIO
from datetime import datetime

# Caminho para credencial
CAMINHO_CREDENCIAL = "ssp-detecta-a0181c69ec58.json"
BUCKET_NAME = "pubsite_prod_rev_13544123004760068805"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CAMINHO_CREDENCIAL

client = storage.Client()
bucket = client.bucket(BUCKET_NAME)

def coletar_dados(prefixo, categoria, pacote, ano):
    blobs = list(bucket.list_blobs(prefix=prefixo))
    blobs_csv = [
        blob for blob in blobs
        if blob.name.endswith(".csv") and ano in blob.name and pacote in blob.name
    ]

    registros = []
    for blob in blobs_csv:
        try:
            content = blob.download_as_bytes()
            df = pd.read_csv(BytesIO(content), encoding="utf-16")
            df["source_file"] = blob.name
            df["categoria"] = categoria
            registros.append(df)
        except Exception as e:
            print(f"Erro ao processar {blob.name}: {e}")

    if registros:
        return pd.concat(registros, ignore_index=True)
    return pd.DataFrame()

def carregar_dados_filtrados(app=None, ano=None, mes=None):
    app = app or ""
    ano = ano or datetime.now().strftime("%Y")
    dfs = [
        coletar_dados("stats/crashes/", "Crashes", app, ano),
        coletar_dados("stats/installs/", "Installs", app, ano),
        coletar_dados("stats/ratings/", "Ratings", app, ano),
        coletar_dados("reviews/", "Reviews", app, ano),
    ]
    df_merged = pd.concat([df for df in dfs if not df.empty], ignore_index=True, sort=False)

    colunas_padrao = {
        "Date": "data", "day": "data", "App Version": "versao",
        "App version": "versao", "App version code": "versao",
        "Review Submit Date": "data", "Review Title": "comentario",
        "Review Text": "comentario", "Star Rating": "nota",
        "Rating": "nota", "Country": "pais", "Device": "dispositivo",
        "Android Version": "os"
    }
    df_merged.rename(columns=colunas_padrao, inplace=True)

    if mes:
        df_merged["data"] = pd.to_datetime(df_merged["data"], errors="coerce")
        df_merged = df_merged[df_merged["data"].dt.month == int(mes)]

    return df_merged