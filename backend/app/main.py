from fastapi import FastAPI

from app.config import settings

app = FastAPI(title="ModelOps Lab API", version="0.1.0")


def health_response() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.environment,
    }


@app.get("/api/v1/health")
def health_check_v1() -> dict[str, str]:
    return health_response()


@app.get("/health")
def health_check_compat() -> dict[str, str]:
    return health_response()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "ModelOps Lab API"}
