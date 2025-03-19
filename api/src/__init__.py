from fastapi import FastAPI
from src.auth.routes import auth_router
from src.projects.routes import project_router
from .errors import register_all_errors
from .middleware import register_middleware


version = "v1"

description = """
A REST API for ICU Scan
    """

version_prefix =f"/api/{version}"

app = FastAPI(
    title="ICU Scan API",
    description=description,
    version=version,
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit"},
    contact={
        "name": "Tipee",
        "url": "https://github.com/",
        "email": "Tipee@gmail.com",
    },
    terms_of_service="httpS://example.com/tos",
    openapi_url=f"{version_prefix}/openapi.json",
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redoc"
)

register_all_errors(app)

register_middleware(app)


app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["auth"])
app.include_router(project_router, prefix=f"{version_prefix}/projects", tags=["projects"])
