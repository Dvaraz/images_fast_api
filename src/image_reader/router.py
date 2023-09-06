import base64
import os
import time
import aiofiles

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi_cache.decorator import cache

from pathlib import Path

from src.database import async_session_maker, get_async_session
from src.image_reader.schemas import Image, GetImages
from src.image_reader.models import Images
from src.image_reader.crud import add_image_information_to_database, delete_information_from_database


router_images = APIRouter(
    prefix="/images",
    tags=["Images"]
)

router_images_2 = APIRouter(
    prefix="/image",
    tags=["Images"]
)

some_file_path = Path(Path.home(), "PycharmProjects", "images_fast_api", "images")


def images_properties(image: Path) -> dict:
    """
    get information about image
    :param image: path to the image
    :return: information in dict format
    """
    kbfactor = float(1 << 10)
    image_dict = {image.name: {"image_size": f'{os.path.getsize(image) / kbfactor: .1f} kb',
                               "last_modify_time": time.ctime(os.path.getmtime(image))
                               }}
    return image_dict


@router_images.get("/{image_name}")
async def get_image(image_name: str) -> FileResponse:
    """
    return image by image name
    :param image_name:
    :return: image in .jpg format
    """
    image_path = Path(some_file_path, f"{image_name}.jpg")
    if image_path.exists():
        return FileResponse(image_path)
    raise HTTPException(status_code=404, detail={
        "status": "error",
        "data": None,
        "details": f"image {image_name} does not exist"
    })


@router_images_2.get("/get_inf_about_images")
async def get_images_information():
    dict_to_js = {}
    for image in some_file_path.iterdir():
        dict_to_js.update(images_properties(image))

    return dict_to_js


@router_images_2.get("")
@cache(expire=30)
async def get_images_information(session: AsyncSession = Depends(get_async_session)) -> list[GetImages]:
    query = select(Images).order_by(Images.id.desc()).limit(10)
    images = await session.execute(query)
    return images.scalars().all()


@router_images_2.post("", status_code=201)
async def create_image(image: Image):
    """
    create image from base64 string and add information about image to database
    :param image: name and base64 string
    :return:
    """
    save_to = Path(some_file_path, f"{image.name}.jpg")
    kbfactor = float(1 << 10)

    async with aiofiles.open(save_to, "wb") as file:
        await file.write(base64.b64decode(image.base64_image))

    image_size = f'{os.path.getsize(save_to) / kbfactor: .1f} kb'
    image_name = image.name
    image_last_edit_at = time.ctime(os.path.getmtime(save_to))
    await add_image_information_to_database(
        image_name=image_name,
        image_size=image_size,
        last_edit_at=image_last_edit_at
        )
    return {"image_created": image_name}


@router_images_2.delete("{image_name}")
async def delete_image(image_name: str):
    """
    delete image from directory and from database by image name
    :param image_name:
    :return:
    """
    try:
        Path(some_file_path, f"{image_name}.jpg").unlink()
        await delete_information_from_database(image_name)
        return {"image_deleted": image_name}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
            "status": "error",
            "data": None,
            "details": f"image {image_name} does not exist"
        })


