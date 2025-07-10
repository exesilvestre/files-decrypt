import io
import mimetypes
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from entities.parsed_file_model import ParsedFileModel
from services.file_lookup_service import (
    get_by_guid,
    get_parsed_file_by_guid,
)

router = APIRouter()


@router.get("/file/{guid}", response_model=ParsedFileModel)
async def get_file_by_guid(guid: str):
    document = get_parsed_file_by_guid(guid)
    if not document:
        raise HTTPException(status_code=404, detail="File not found")

    return document


@router.get("/downloadFile/{guid}")
async def download_file(guid: str):
    document = get_by_guid(guid)
    if not document:
        raise HTTPException(status_code=404, detail="File not found")

    metadata = document.get("metadata", {})
    content = document.get("content")

    filename = metadata.get("FILENAME", "unknown_file")

    if content is None:
        raise HTTPException(status_code=400, detail="No content found")

    file_like = io.BytesIO(content)

    # Guess the content type based on the filename
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

    return StreamingResponse(
        file_like,
        media_type=content_type,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "X-Filename": filename,
            "Access-Control-Expose-Headers": "X-Filename" 
        },
    )
