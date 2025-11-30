from fastapi import FastAPI
import uvicorn
from config.database import init_db
from controllers import produto_controller, cliente_controller, pedido_controller
from models.db import produto_model, cliente_model, pedido_model

app = FastAPI(
 title="API Loja Virtual POO",
 description="Implementação de CRUD com Herança, Polimorfismo, Decisão e Repetição.",
)
@app.on_event("startup")
async def on_startup():
 # Importar modelos para init_db
    await init_db()
# Incluir Controllers (Rotas)
app.include_router(produto_controller.router, prefix="/v1")
app.include_router(cliente_controller.router, prefix="/v1")
app.include_router(pedido_controller.router, prefix="/v1")
@app.get("/", tags=["Root"])
async def root():
    return {"message": "Bem-vindo à API Loja Virtual"}
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
