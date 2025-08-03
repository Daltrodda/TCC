from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Gateway HTTPS ativo com sucesso 🚀"}
