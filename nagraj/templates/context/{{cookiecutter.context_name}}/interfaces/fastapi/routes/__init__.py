"""FastAPI routes for {{ cookiecutter.context_name }} bounded context."""

from fastapi import APIRouter

router = APIRouter(prefix="/{{ cookiecutter.domain_name }}/{{ cookiecutter.context_name }}") 