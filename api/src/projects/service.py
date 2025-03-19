from datetime import datetime

from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import Project

from .schemas import ProjectCreateModel, ProjectUpdateModel


class ProjectService:
    async def get_all_projects(self, session: AsyncSession):
        statement = select(Project).order_by(desc(Project.created_at))

        result = await session.exec(statement)

        return result.all()

    async def get_project_by_uid(self, project_uid: str, session: AsyncSession):
        statement = select(Project).where(Project.uid == project_uid)

        result = await session.exec(statement)

        return result.first()
    
    async def get_projects_by_user_uid(self, user_uid: str, session: AsyncSession):
        statement = select(Project).where(Project.user_uid == user_uid).order_by(desc(Project.created_at))

        result = await session.exec(statement)

        return result.all()
    
    async def create_project(self, project_data: ProjectCreateModel, user_uid: str, session: AsyncSession):
        project_data_dict = project_data.model_dump()

        new_project = Project(**project_data_dict)

        new_project.user_uid = user_uid
        new_project.created_at = datetime.now()
        new_project.update_at = datetime.now()

        session.add(new_project)

        await session.commit()

        return new_project
    
    async def update_project(self, project_uid: str, update_data: ProjectUpdateModel,session:AsyncSession):

        project_data = await self.get_project_by_uid(project_uid, session)

        if project_data is not None:
            project_data_dict = update_data.model_dump()
            project_data.update_at = datetime.now()

            for k, v in project_data_dict.items():
                setattr(project_data, k, v)

            await session.commit()

            return project_data
        else:
            return None
    
    async def delete_project(self, project_uid: str, session: AsyncSession):
        project_to_delete = await self.get_project_by_uid(project_uid, session)

        if project_to_delete is not None:
            await session.delete(project_to_delete)

            await session.commit()

            return project_to_delete
        else:
            return None
    

