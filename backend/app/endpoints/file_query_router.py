import io
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from entities.parsed_file_model import ParsedFileModel
from services.file_lookup_service import (
    get_file_metadata_by_guid,
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
    document = get_file_metadata_by_guid(guid)
    if not document:
        raise HTTPException(status_code=404, detail="File not found")

    metadata = document.get("metadata", {})
    content = document.get("content")
    filename = metadata.get("FILENAME", "unknown_file")

    if content is None:
        raise HTTPException(status_code=400, detail="No content found")

    try:
        file_bytes = content
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error processing content: {str(e)}"
        )

    # Crear stream para descarga
    file_like = io.BytesIO(file_bytes)

    # Determinar content type
    content_type = metadata.get("CONTENTTYPE", "application/octet-stream")

    return StreamingResponse(
        file_like,
        media_type=content_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
