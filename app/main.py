from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.api.app_router import api_router

from app.core.configs import app_config

app = FastAPI(
    title=app_config.APP_NAME,
    description="This is a sample FastAPI application.",
    version="1.0.0",
    debug=app_config.DEBUG,
)
# Configuration des middlewares CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_config.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """
    Redirects the root path to the API documentation.
    """
    return RedirectResponse(url="/docs")
app.include_router(api_router, prefix="/api/v1")

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "Authentication service is running"}

if __name__ == "__main__":
    import uvicorn

    # Démarre l'application avec uvicorn sur le port 9000
    uvicorn.run('app.main:app', host="0.0.0.0", port=10000, reload=True, reload_dirs=["app"])