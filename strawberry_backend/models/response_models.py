"""
Модуль с моделями ответа сервера
"""

from enum import Enum
from pydantic import BaseModel

from config.config import config


class BaseResponse(BaseModel):
    """
    Модель базового ответа.

    status - int, статус операции:
        * 0 - OK
        * 1 - VK API Auth error
        * 2 - Worker error
        * 3 - Request error (cannot parse)
        * 4 - Unknown error
        * 5 - Not implemented
        * 6 - Database error
        * 7 - Rate limit exceeded

    description - str, текстовое описание ошибки,
    может содержать дополнительную информацию
    """

    status: int
    description: str


class FeedbackResponse(BaseResponse):
    """
    Модель с ответом на отправку фидбека
    """

    pass


class Post(BaseModel):
    """
    Класс с описанием поста

    post_id - int, айди поста в базе данных. На фронтенде наверное не понадобится

    user_id : int, айди юзера, который сделал пост, тоже не понадобится

    method : str, название метода, которым сделан этот текст

    hint : str, затравка/тема поста, введенные пользователем для генерации

    text : str, сам текст, который сделала нейросеть

    rating : int, оценка поста, целое число (Задать посту оценку - см. /send_feedback)

    date : int, unix дата, когда был отправлен запрос

    group_id : int, айди группы, для которой сделан пост

    status : str, описание статуса запроса: 0 - новый пост, 1 - готово, 2 - ошибка

    gen_time : int - количество миллисекунд, затраченных на генерацию. date + gen_time = дата, когда генерация закончена

    platform : str - платформа, с которой отправлен запрос

    published : int - 0 - не опубликовано, 1 - опубликовано

    hidden : int - 0 - виден, 1 - спрятан
    """

    post_id: int
    user_id: int
    method: str
    hint: str
    text: str
    rating: int
    date: int
    group_id: int
    status: str
    gen_time: int
    platform: str
    published: int
    hidden: int


class PostListResponse(BaseResponse):
    """
    Модель со списком постов

    posts : int - Список постов
    """

    posts: list[Post]


class PostResponse(BaseResponse):
    """
    Модель со списком постов

    post : Post - Пост
    """

    post: Post


class GenerateResponse(BaseResponse):
    """
    Модель с айди генерации для поллинга

    generation_id : int - айди генерации для поллинга и получения результата
    """

    generation_id: int


class UploadResponse(BaseResponse):
    """
    Модель с результатом загрузки файла

    upload_result : str - ответ сервера загрузки
    """

    upload_result: str


class MethodsResponse(BaseResponse):
    """
    Модель со списком возможных методов генерации

    methods: dict[str,list[str]] - методы по категориям
    """

    methods: dict[str, list[str]]
