import aiohttp
import logging
from fastapi import UploadFile, HTTPException
from app.core.config import settings

DEEP_AI_API_URL = "https://api.deepai.org/api/nsfw-detector"

logger = logging.getLogger(__name__)

async def moderate_image(file: UploadFile) -> dict:
    headers = {"api-key": settings.deepai_api_key}

    contents = await file.read()

    data = aiohttp.FormData()
    data.add_field("file", contents, filename=file.filename, content_type=file.content_type)

    async with aiohttp.ClientSession() as session:
        async with session.post(DEEP_AI_API_URL, headers=headers, data=data) as response:
            logger.info(f"Ответ DeepAI API:\n{response.status}")

            if response.status != 200:
                raise HTTPException(status_code=502, detail="Недопустимый ответ DeepAI API.")
            data = await response.json()

    nsfw_score = data.get("output", {}).get("nsfw_score", 0)

    if nsfw_score > 0.7:
        return {"status": "REJECTED", "reason": "NSFW content"}
    else:
        return {"status": "OK"}
