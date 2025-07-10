from typing import Dict
from utils.constants import REQUIRED_METADATA_FIELDS
from utils.clean_metadata import clean_metadata_keys


class MetadataParser:

    @staticmethod
    def decode_metadata(header: bytes) -> Dict[str, str]:
        """
        Parse metadata from header bytes.
        Expected format: KEY/VALUE pairs separated by newlines
        """
        try:
            text = header.decode("ascii", errors="ignore")
        except Exception:
            return {}

        metadata = {}
        for line in text.splitlines():
            if "/" in line:
                key, val = line.split("/", 1)
                key = key.strip().upper()
                metadata[key] = val.strip()
        return clean_metadata_keys(metadata)

    @staticmethod
    def validate_required_fields(metadata: Dict[str, str]) -> bool:
        """Check if all required metadata fields are present"""
        return all(field in metadata for field in REQUIRED_METADATA_FIELDS)
