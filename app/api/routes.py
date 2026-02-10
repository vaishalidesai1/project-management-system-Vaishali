from fastapi import APIRouter, Depends, HTTPExecption

from app.domain.exceptions import DomainError, NotFoundError, InvalidStatusTransition, ValidationError
from app.repositories.memory import InMemoryProjectRepo, InMemoryTaskRepo
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.schemas.dto import ProjectCreate, ProjectOut, TaskCreate, TaskOut, TaskUpdate

router = APIRouter()

project_repo = InMemoryProjectRepo()
task_repo = InMemoryTaskRepo()

def get_project_service() -> ProjectService:
    return ProjectService(project_repo)

def get_task_service() -> TaskService:
    return TaskService(project_repo, task_repo)

def to_http(e: Exception) -> HTTPExecption:
    if isinstance(e, NotFoundError):
        return HTTPExecption(status_code = 404, details=str(e))
    if isinstance(e, InvalidStatusTransition, ValidationError, ValueError):
        return HTTPExecption(status_code = 400, details=str(e))
    if isinstance(e, DomainError):
        return HTTPExecption(status_code=500, details='Internal Server Error')

@router.post('/projects', response_model = ProjectOut ,status_code = 201)
def create_project(body: ProjectCreate, service: ProjectService = Depends(get_project_service)):
    pass