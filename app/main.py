from fastapi import FastAPI
from app.routes import metrics

app = FastAPI(title="Google Play Métricas API")

app.include_router(metrics.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
