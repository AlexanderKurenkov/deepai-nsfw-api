from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.moderation import moderate_image

# Создание маршрутизатора для обработки эндпоинтов
router = APIRouter()

@router.post("/moderate")
async def moderate(file: UploadFile = File(...)):
    """
    Эндпоинт для модерации изображения.

    :param file: Загружаемый файл (изображение формата JPG, PNG или JPEG)
    :return: Результат модерации от DeepAI API
    :raises HTTPException: Если передан файл неподдерживаемого формата
    """
    # Проверка расширения файла
    if not file.filename.endswith((".jpg", ".png", ".jpeg")):
        raise HTTPException(status_code=400, detail="Неподдерживаемый формат файла")

    # Вызов функции модерации
    return await moderate_image(file)
