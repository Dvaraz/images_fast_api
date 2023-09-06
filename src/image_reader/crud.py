import time

from sqlalchemy import insert, delete

from src.database import async_session_maker
from src.image_reader.models import Images


async def add_image_information_to_database(image_name: str, image_size: str, last_edit_at: time):
    """
    function that add image information to database
    :param image_name: name of image
    :param image_size: size of image in kb
    :param last_edit_at: last time image modified
    :return:
    """
    async with async_session_maker() as session:
        stmt = insert(Images).values(
            image_name=image_name,
            image_size=image_size,
            last_edit_at=last_edit_at
        )
        await session.execute(stmt)
        await session.commit()


async def delete_information_from_database(image_name: str, ):
    async with async_session_maker() as session:
        stmt = delete(Images).where(Images.image_name == image_name)
        await session.execute(stmt)
        await session.commit()
