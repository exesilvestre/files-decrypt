import base64
import io
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from services.file_lookup_service import (
    get_file_metadata_by_guid, 
    get_parsed_file_by_guid
)

router = APIRouter()


@router.get("/file/{guid}")
async def get_file_by_guid(guid: str):
    document = get_parsed_file_by_guid(guid)
    if not document:
        raise HTTPException(status_code=404, detail="File not found")

    document.pop("_id", None)
    return document


@router.get("/downloadFile/{guid}")
async def download_file(guid: str):
    document = get_file_metadata_by_guid(guid)
    if not document:
        raise HTTPException(status_code=404, detail="File not found")

    metadata = document.get("metadata", {})
    content = document.get("content")
    encoded_true = document.get("encoded_true", True)
    filename = metadata.get("FILENAME", "")

    if content is None:
        raise HTTPException(status_code=400, detail="No content found")

    try:
        if encoded_true:
            file_bytes = base64.b64decode(content)
        else:
            file_bytes = content.encode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="Error decoding content")

    file_like = io.BytesIO(file_bytes)

    return StreamingResponse(
        file_like,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
