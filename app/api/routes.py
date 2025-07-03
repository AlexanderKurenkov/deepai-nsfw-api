from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.moderation import moderate_image

router = APIRouter()

@router.post("/moderate")
async def moderate(file: UploadFile = File(...)):
    if not file.filename.endswith((".jpg", ".png", ".jpeg")):
        raise HTTPException(status_code=400, detail="Неподдерживаемый формат файла")
    return await moderate_image(file)