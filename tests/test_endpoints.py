import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_get_dados():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/dados/?ano=2025")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_exportar_excel():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/exportar/?ano=2025")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"