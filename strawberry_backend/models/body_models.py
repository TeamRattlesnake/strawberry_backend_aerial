"""
Модуль с телами запроса
"""

from enum import Enum
from pydantic import BaseModel

from config.config import config


class GenerateModel(BaseModel):
    """
    Модель с методами генерации
    """

    method: config.generate_methods
    context_data: list[str]
    prompt: str
    group_id: int
