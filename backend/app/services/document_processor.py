from typing import Optional, Tuple, Dict, Any
from bson import Binary
from entities.document_model import DocumentResponseModel
from db.mongo_client import collection
from utils.detect_category import get_category
from utils.unsecure_files import is_forbidden_filetype
from .metadata_parser import MetadataParser
from .content_extractor import ContentExtractor
from .document_block_extractor import DocumentBlockExtractor


class DocumentProcessor:
    def __init__(self):
        self.metadata_parser = MetadataParser()
        self.content_extractor = ContentExtractor()
        self.block_extractor = DocumentBlockExtractor()

    def process_document(
        self, raw: bytes, start: int, end: int
    ) -> Tuple[Optional[DocumentResponseModel], int]:
        """
        Process a single document block from raw file data.
        Returns processed document and next position to continue parsing.
        """
        # Find signature marker, this inidcates a document begins - if not found, skip this block
        sig_pos = self.block_extractor.find_signature_position(raw, start, end)
        if sig_pos == -1:
            return None, start + 6
        # Find where metadata ends (null byte delimiter)
        content_start = self.content_extractor.find_metadata_delimiter(
            raw, sig_pos, end
        )
        if content_start == -1:
            return None, end

        # Parse and validate metadata
        metadata = self.metadata_parser.decode_metadata(raw[start:content_start])
        if not metadata or not self.metadata_parser.validate_required_fields(metadata):
            return None, end

        # Security check for forbidden file types
        self._validate_file_security(metadata)

        # Extract and validate content
        expected_sha1 = metadata.get("SHA1", "").upper()
        content, content_end = self.content_extractor.extract_content(
            raw, content_start, end, expected_sha1
        )

        # If content validation fails, skip this document
        if content is None:
            return None, end

        # Build, save and return document
        document = self._build_document(metadata, content)
        self._save_document(document)

        response_doc = self._build_response_document(document)
        next_pos = self._calculate_next_position(content_end, end)
        return response_doc, next_pos

    def _validate_file_security(self, metadata: Dict[str, str]) -> None:
        """Check if file type is allowed based on extension and content type"""
        file_extension = metadata.get("EXT", "")
        filename = metadata.get("FILENAME", "")
        content_type = metadata.get("CONTENTTYPE", "")

        if file_extension and content_type and is_forbidden_filetype(file_extension):
            raise Exception(f"Forbidden file detected inside container: {filename}")

    def _build_document(self, metadata: Dict[str, str], content: bytes) -> dict:
        """Construct document object with all required fields"""
        return {
            "guid": metadata.get("GUID"),
            "filename": metadata.get("FILENAME", ""),
            "metadata": metadata,
            "category": get_category(metadata.get("DOCTYPE", "")),
            "is_xml": self.content_extractor.is_xml(content),
            "content": Binary(content),
        }

    def _save_document(self, document: Dict[str, Any]):
        """Save document to MongoDB if it has a GUID"""
        if document["guid"]:
            collection.update_one(
                {"guid": document["guid"]}, {"$set": document}, upsert=True
            )

    def _build_response_document(
        self, document: Dict[str, Any]
    ) -> DocumentResponseModel:
        """Create response document without binary content for API response"""
        return DocumentResponseModel(
            guid=document["guid"],
            filename=document["filename"],
            category=document["category"],
            metadata=document["metadata"],
        )

    def _calculate_next_position(self, content_end: int, document_end: int) -> int:
        """
        Calculate where to continue parsing after current document.
        Skip 2 bytes after content end marker to avoid parsing the "**" marker.
        """
        offset = 2  # Skip the "**" marker
        candidate_pos = content_end + offset
        # Ensure we don't go past the document boundary
        return min(candidate_pos, document_end)
