from fastapi import APIRouter, File, UploadFile, HTTPException
from io import BytesIO
from services.file_service import FileService

router = APIRouter()


@router.post("/uploadfile/")
async def handle_file_upload(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file was provided.")
    content = await file.read()

    buffered_upload = UploadFile(filename=file.filename, file=BytesIO(content))
    file_service = FileService()
    parsed_data = file_service.get_parsed_file(file=buffered_upload)

    if not parsed_data:
        raise HTTPException(status_code=422, detail="File could not be processed.")

    return parsed_data
