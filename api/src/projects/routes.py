from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.db.main import get_session
from src.projects.service import ProjectService
from .schemas import Project, ProjectCreateModel, ProjectUpdateModel
from src.errors import ProjectNotFound

project_router = APIRouter()
project_service = ProjectService()
access_token_bearer = AccessTokenBearer()
admin_role_checker = Depends(RoleChecker(["admin"]))
user_role_checker = Depends(RoleChecker(["admin", "user"]))


# @project_router.get("/", response_model=List[Project])
# async def get_all_projects(
#     session: AsyncSession = Depends(get_session),
#     _: dict = Depends(access_token_bearer)
# ):
#     projects = await project_service.get_all_projects(session)
#     return projects


@project_router.get("/user", response_model=List[Project], dependencies=[user_role_checker])
async def get_projects_by_user_uid(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
):
    user_uid = token_details["user"]["user_uid"]
    projects = await project_service.get_projects_by_user_uid(user_uid, session)
    return projects


@project_router.get("/user/{project_uid}", response_model=Project, dependencies=[user_role_checker])
async def get_project_by_uid(
    project_uid: str,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer)
):
    project = await project_service.get_project_by_uid(project_uid, session)

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    return project


@project_router.post("/user", response_model=Project, dependencies=[user_role_checker])
async def create_project(
    project_data: ProjectCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> dict:
    user_uid = token_details["user"]["user_uid"]
    project = await project_service.create_project(project_data, user_uid, session)

    return project


@project_router.put("/user/{project_uid}", response_model=Project, dependencies=[user_role_checker])
async def update_project(
    project_uid: str,
    update_data: ProjectUpdateModel,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer)
):
    project = await project_service.update_project(project_uid, update_data, session)

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    return project


@project_router.delete("/user/{project_uid}", dependencies=[user_role_checker])
async def delete_project(
    project_uid: str,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer)
):
    project = await project_service.delete_project(project_uid, session)

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    return project