from pydantic import BaseModel
from typing import Optional, Dict


class DocumentResponseModel(BaseModel):
    guid: Optional[str]
    filename: str
    category: str
    metadata: Dict[str, str]
