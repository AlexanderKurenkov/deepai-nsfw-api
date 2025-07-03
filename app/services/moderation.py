import aiohttp
import logging
from fastapi import UploadFile, HTTPException
from app.core.config import settings

# URL эндпоинта DeepAI для проверки NSFW-контента
DEEP_AI_API_URL = "https://api.deepai.org/api/nsfw-detector"

# Настройка базового логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def moderate_image(file: UploadFile) -> dict:
    """
    Выполняет модерацию изображения, используя DeepAI NSFW API.

    :param file: Загружаемый файл изображения (UploadFile из FastAPI)
    :return: Словарь с результатом модерации:
             {"status": "REJECTED", "reason": "NSFW content"} — если обнаружен NSFW-контент,
             {"status": "OK"} — если изображение допустимо.
    :raises HTTPException: Если API DeepAI вернул некорректный ответ.
    """
    # Заголовки запроса с API-ключом
    headers = {"api-key": settings.deepai_api_key}

    # Чтение содержимого загружаемого файла
    contents = await file.read()

    # Формирование данных формы для отправки изображения
    data = aiohttp.FormData()
    data.add_field("file", contents, filename=file.filename, content_type=file.content_type)

    # Отправка POST-запроса к DeepAI API
    async with aiohttp.ClientSession() as session:
        async with session.post(DEEP_AI_API_URL, headers=headers, data=data) as response:
            logger.info(f"DeepAI API response object:\n{response}")

            # Получение JSON-ответа
            data = await response.json()
            logger.info(f"Тело ответа:\n{data}")

            # Проверка статуса ответа
            if response.status != 200:
                raise HTTPException(status_code=502, detail="Ошибка при выполнении запроса.")

    # Извлечение NSFW-оценки
    nsfw_score = data.get("output", {}).get("nsfw_score", 0)

    # Принятие решения на основе оценки
    if nsfw_score > 0.7:
        return {"status": "REJECTED", "reason": "NSFW content"}
    else:
        return {"status": "OK"}
