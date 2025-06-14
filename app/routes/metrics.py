from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from app.services.google_storage import carregar_dados_filtrados
from app.utils.excel_exporter import exportar_para_excel
from typing import Optional
import io

router = APIRouter()

@router.get("/dados/")
def listar_dados(app: Optional[str] = None, ano: Optional[str] = None, mes: Optional[str] = None):
    df = carregar_dados_filtrados(app, ano, mes)
    return df.to_dict(orient="records")

@router.get("/exportar/")
def exportar_excel(app: Optional[str] = None, ano: Optional[str] = None, mes: Optional[str] = None):
    df = carregar_dados_filtrados(app, ano, mes)
    output = io.BytesIO()
    exportar_para_excel(df, output)
    output.seek(0)
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": "attachment; filename=dados_filtrados.xlsx"})