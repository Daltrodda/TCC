# gateway/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

AUTH_SERVICE_URL = "http://auth:8000"  # nome do serviço no docker-compose

@app.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_auth(path: str, request: Request):
    method = request.method
    url = f"{AUTH_SERVICE_URL}/{path}"

    # Repassa o corpo, cabeçalhos e query params
    headers = dict(request.headers)
    body = await request.body()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=method,
                url=url,
                content=body,
                headers=headers,
                params=request.query_params
            )
            return JSONResponse(
                status_code=response.status_code,
                content=response.json()
            )
        except httpx.RequestError as e:
            return JSONResponse(
                status_code=502,
                content={"error": f"Erro ao acessar o serviço Auth: {str(e)}"}
            )
