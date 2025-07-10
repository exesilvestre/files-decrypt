from pydantic import BaseModel
from typing import Dict, Any


class ParsedFileModel(BaseModel):
    guid: str
    filename: str
    metadata: Dict[str, Any]
    category: str
    is_xml: bool
    content: Any
