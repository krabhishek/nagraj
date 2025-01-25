import uvicorn

from {{cookiecutter.project_slug}}.example_domain_one.interface.rest_api.fastapi_app import (
    create_app,
)

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "{{cookiecutter.project_slug}}.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
