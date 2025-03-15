from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import User
from src.errors import UserNotFound

from .schemas import UserCreateModel
from .utils import generate_passwd_hash


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)

        result = await session.exec(statement)

        user = result.first()

        return user

    async def user_exists(self, email, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        return True if user is not None else False

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)

        new_user.password_hash = generate_passwd_hash(user_data_dict["password"])
        new_user.role = "user"

        session.add(new_user)

        await session.commit()

        return new_user


    async def update_user(self, user:User , user_data: dict,session:AsyncSession):

        for k, v in user_data.items():
            setattr(user, k, v)

        await session.commit()

        return user
    

    async def delete_user(self, user_uid: str, session: AsyncSession):
        user = await self.get_user_by_uid(user_uid, session)

        if not user:
            raise UserNotFound()

        await session.delete(user)

        await session.commit()

    
    async def get_all_users(self, session: AsyncSession):
        statement = select(User)

        result = await session.exec(statement)

        return result.all()
    
    async def get_user_by_uid(self, user_uid: str, session: AsyncSession):
        statement = select(User).where(User.uid == user_uid)

        result = await session.exec(statement)

        return result.first()
    
    async def delete_user_by_uid(self, user_uid: str, session: AsyncSession):
        user = await self.get_user_by_uid(user_uid, session)

        if not user:
            raise UserNotFound()

        await session.delete(user)

        await session.commit()
