from fastapi import HTTPException
from pymongo.errors import PyMongoError
from db.mongo_client import collection
import xmltodict


def get_file_metadata_by_guid(guid: str) -> dict | None:
    try:
        return collection.find_one({"guid": guid})
    except PyMongoError:
        return None


def get_parsed_file_by_guid(guid: str) -> dict:
    document = get_file_metadata_by_guid(guid)
    if not document:
        raise HTTPException(status_code=404, detail="File not found")
    if document.get("is_xml") and document.get("content"):
        try:
            xml_str = document["content"]
            document["content"] = xmltodict.parse(xml_str)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Invalid XML content: {str(e)}")

    return document