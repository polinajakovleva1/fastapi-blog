from fastapi import FastAPI

app = FastAPI(
    title="FastAPI Blog Backend",
    description="Backend-приложение для блога с админскими CRUD-операциями, публичным API и системой управления пользователями",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"messages": "Работает!!!", "status": "ok"}