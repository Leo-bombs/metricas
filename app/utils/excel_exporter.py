import pandas as pd

def exportar_para_excel(df, buffer):
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Dados")