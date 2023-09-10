"""
Сервер FastAPI для Strawberry
"""

from typing import Annotated

from config.config import config

from models.response_models import (
    FeedbackResponse,
    PostListResponse,
    PostResponse,
    GenerateResponse,
    UploadResponse,
    MethodsResponse,
    Post,
)
from models.body_models import GenerateModel

from modules.utils import (
    UtilsException,
    is_valid,
    is_docs,
    parse_query_string,
)

from modules.server import *

from modules.logger import logger

from fastapi import (
    FastAPI,
    Header,
    Form,
    UploadFile,
    Request,
)
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware

database = Database()
worker = Worker()

app = FastAPI(
    title=config.docs_title,
    version=config.docs_version,
    description=config.docs_description,
    contact=config.docs_contact,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.server_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def auth_check(request: Request, call_next):
    logger.info(f"Got request: {request.url},\tAuth: pending")
    try:
        auth_header = request.headers["MiniAppParams"]
        auth_query = parse_query_string(auth_header)
        client_secret = config.server_client_secret
        if is_valid(query=auth_query, secret=client_secret):
            logger.info(f"Got request: {request.url},\tAuth: succesful")
            response = await call_next(request)
            return response
        logger.info(f"Got request: {request.url},\tAuth: wrong signature")
        return JSONResponse(
            content={"status": 1, "description": "Auth: wrong signature"}
        )
    except KeyError as exc:
        logger.info(
            f"Got request: {request.url},\tAuth: error parsing header, maybe it is /docs?: {exc}"
        )
        if is_docs(request.url):
            logger.info(f"Got request: {request.url},\tAuth: it is /docs")
            response = await call_next(request)
            return response
        logger.info(
            f"Got request: {request.url},\tAuth: no MiniAppParams header: {exc}"
        )
        return JSONResponse(
            content={"status": 3, "description": "Auth: no MiniAppParams header"}
        )
    except UtilsException as exc:
        logger.info(
            f"Got request: {request.url},\tAuth: unknown error in auth_check: {exc}"
        )
        return JSONResponse(
            content={"status": 4, "description": "Auth: unknown error in auth_check"}
        )
    except Exception as exc:
        logger.info(f"Got request: {request.url},\tUnknown error: {exc}")
        return JSONResponse(content={"status": 4, "description": f"Unknown error"})


@app.post(
    "/api/v1/post/{post_id}/like",
    response_model=FeedbackResponse,
    tags=["Действия с готовым постом"],
)
async def post_like(MiniAppParams: Annotated[str, Header()], post_id: int):
    return FeedbackResponse(status=0, description="ok")


@app.post(
    "/api/v1/posts/{post_id}/dislike",
    response_model=FeedbackResponse,
    tags=["Действия с готовым постом"],
)
async def post_dislike(MiniAppParams: Annotated[str, Header()], post_id: int):
    return FeedbackResponse(status=0, description="ok")


@app.delete(
    "/api/v1/posts/{post_id}/hide",
    response_model=FeedbackResponse,
    tags=["Действия с готовым постом"],
)
async def delete_hide(MiniAppParams: Annotated[str, Header()], post_id: int):
    return FeedbackResponse(status=0, description="ok")


@app.post(
    "/api/v1/posts/{post_id}/recover",
    response_model=FeedbackResponse,
    tags=["Действия с готовым постом"],
)
async def post_recover(MiniAppParams: Annotated[str, Header()], post_id: int):
    return FeedbackResponse(status=0, description="ok")


@app.post(
    "/api/v1/posts/{post_id}/publish",
    response_model=FeedbackResponse,
    tags=["Действия с готовым постом"],
)
async def post_publish(MiniAppParams: Annotated[str, Header()], post_id: int):
    return FeedbackResponse(status=0, description="ok")


@app.get("/api/v1/posts", response_model=PostListResponse, tags=["Получение данных"])
async def get_posts(
    MiniAppParams: Annotated[str, Header()],
    group_id: int = None,
    offset: int = None,
    limit: int = None,
):
    return PostListResponse(status=0, description="ok", posts=[])


@app.get(
    "/api/v1/posts/{post_id}", response_model=PostResponse, tags=["Получение данных"]
)
async def get_post_id(MiniAppParams: Annotated[str, Header()], post_id):
    return PostResponse(
        status=0,
        description="ok",
        post=Post(
            post_id=1,
            user_id=2,
            method="gen_from_scratch",
            hint="abc",
            text="def",
            rating=1,
            date=123,
            group_id=1,
            status=1,
            gen_time=5,
            platform="non",
            published=1,
            hidden=0,
        ),
    )


@app.post(
    "/api/v1/generation/generate", response_model=GenerateResponse, tags=["Генерация"]
)
async def post_generate(MiniAppParams: Annotated[str, Header()], data: GenerateModel):
    return GenerateResponse(status=0, description="ok", generation_id=1)


@app.post(
    "/api/v1/files/upload", response_model=UploadResponse, tags=["Действия с файлами"]
)
async def post_upload(
    MiniAppParams: Annotated[str, Header()],
    upload_url: Annotated[str, Form()],
    file: UploadFile,
):
    return UploadResponse(
        status=0,
        description="ok",
        upload_result="я уже забыл что тут вообще лежит. Ссылка?",
    )


@app.get(
    "/api/v1/capabilities/methods",
    response_model=MethodsResponse,
    tags=["Описание параметров и возможностей сервиса"],
)
async def get_methods(MiniAppParams: Annotated[str, Header()]):
    return MethodsResponse(
        status=0,
        description="Это все доступные методы генерации сервера",
        methods=config.contexts_schema,
    )
