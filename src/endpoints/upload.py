from fastapi import APIRouter, File, UploadFile
from services.file_Service import FileService

router = APIRouter()


@router.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint to upload a file or a file container.
    """
    file_service = FileService(file=file)
    response = file_service.get_parsed_file()
    return response