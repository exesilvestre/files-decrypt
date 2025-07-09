from fastapi import APIRouter, File, UploadFile, HTTPException, Request
from typing import Any
from io import BytesIO
from services.file_Service import FileService
from utils.unsecure_files import is_forbidden_file

router = APIRouter()


@router.post("/uploadfile/", response_model=list[dict])
async def upload_file(request: Request, file: UploadFile = File(...)) -> Any:
    if not file:
        raise HTTPException(status_code=400, detail="No file was provided.")

    try:
        if is_forbidden_file(file.filename, file.content_type):
            raise HTTPException(
                status_code=415, detail="File type not allowed."
            )
        content = await file.read()

        memory_file = UploadFile(filename=file.filename, file=BytesIO(content))
        file_service = FileService(file=memory_file)
        response = file_service.get_parsed_file()

        if not response:
            raise HTTPException(
                status_code=422,
                detail="File could not be processed."
            )

        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=(
                f"An error occurred while processing the file: {str(e)}"
            )
        )
