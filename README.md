# Google Play Métricas API

API para consulta e exportação de métricas de aplicativos Android via Google Play.

## Endpoints

### 🔍 Consultar dados brutos
- `GET /dados/`  
  Retorna os dados brutos filtrados por:
  - `app`: nome do pacote (ex: br.gov.sp.detran.consultas)
  - `ano`: ano desejado (ex: 2025)
  - `mes`: número do mês (ex: 6)

Exemplo:
```
GET /dados/?app=br.gov.sp.detran.consultas&ano=2025&mes=6
```

### 📥 Exportar para Excel
- `GET /exportar/`  
  Exporta os mesmos dados filtrados para Excel.

## Execução local

```bash
uvicorn app.main:app --reload
```

Acesse a documentação interativa em:
[http://localhost:8000/docs](http://localhost:8000/docs)

## Execução com Docker

```bash
docker build -t googleplay-api .
docker run -d -p 8000:8000 -v $(pwd)/ssp-detecta-a0181c69ec58.json:/app/ssp-detecta-a0181c69ec58.json googleplay-api
```

## Autoria

Publicado no repositório [GitHub](https://github.com/Leo-bombs/coleta_metricas)