import base64
from fastapi import HTTPException
from pymongo.errors import PyMongoError
from bson import Binary
from entities.parsed_file_model import ParsedFileModel
from db.mongo_client import collection
import xmltodict


def get_file_metadata_by_guid(guid: str) -> dict | None:
    try:
        return collection.find_one({"guid": guid})
    except PyMongoError:
        return None


def get_parsed_file_by_guid(guid: str) -> ParsedFileModel:
    document = get_file_metadata_by_guid(guid)
    if not document:
        raise HTTPException(status_code=404, detail="File not found")

    content = document.get("content")

    if not isinstance(content, (bytes, Binary)):
        raise HTTPException(
            status_code=500, detail="Invalid content type: not binary data"
        )

    raw_bytes = bytes(content)
    try:
        text = raw_bytes.decode("utf-8")
        if document.get("is_xml"):
            document["content"] = xmltodict.parse(text)
        else:
            document["content"] = text

    except UnicodeDecodeError:
        document["content"] = base64.b64encode(raw_bytes).decode("utf-8")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unable to process content: {str(e)}"
        )

    return ParsedFileModel(**document)
