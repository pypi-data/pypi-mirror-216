from validador_colab.infra.repositories import SmarketAnalyticsRepositoryPostgres
from validador_colab.core.usecases import SmarketService
from validador_colab.infra.routes import daily_conf_router
from validador_colab.infra.routes import daily_conf_tasks
from fastapi import FastAPI, Depends
import asyncio

app = FastAPI()

app.include_router(daily_conf_router)

# TODO: Apagar temp_data automaticamente
# TODO: Implementar entrada data/industria
# TODO: Documentar API
# TODO: Rota que gera relatório


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
