from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.moderation import Moderate_Image
from app.schemas.responses import ModerationResponse

router = APIRouter()

@router.post("/moderate", response_model=ModerationResponse)
async def moderate(file: UploadFile = File(...)):
    if not file.filename.endswith((".jpg", ".png", ".jpeg")):
        raise HTTPException(status_code=400, detail="Неподдерживаемый формат файла")
    return await Moderate_Image(file)