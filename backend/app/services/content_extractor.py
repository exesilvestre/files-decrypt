import hashlib
from typing import Optional, Tuple


class ContentExtractor:
    def find_metadata_delimiter(self, raw: bytes, start: int, end: int) -> int:
        """
        Find the position where metadata ends and content begins.
        Looks for two consecutive null bytes (\x00\x00) as delimiter.
        Returns position of last consecutive null byte.
        """
        # Find first occurrence of two consecutive null bytes
        pos = raw.find(b"\x00\x00", start, end)
        if pos == -1:
            return -1

        # Skip any additional null bytes after the initial pair
        # This handles cases where there are more than 2 consecutive nulls
        next_pos = pos + 2
        while next_pos < end and raw[next_pos] == 0x00:
            next_pos += 1

        # Return position of the last consecutive null byte
        # Metadata ends before this, content starts at next_pos
        return next_pos

    def extract_content(
        self, raw: bytes, start: int, end: int, expected_sha1: str
    ) -> Tuple[Optional[bytes], Optional[int]]:
        """
        Extract content from raw bytes and validate against expected SHA1.
        Content ends at the last occurrence of "**" marker.
        """
        # Look for the last occurrence of the content marker "**"
        # This indicates the end of the actual content
        last_marker = raw.rfind(b"**", start, end)
        if last_marker == -1:
            last_marker = end

        content = raw[start:last_marker]

        # Validate content integrity by comparing SHA1 hashes
        if expected_sha1 == hashlib.sha1(content).hexdigest().upper():
            return content, last_marker
        return None, None

    @staticmethod
    def is_xml(data: bytes) -> bool:
        """Check if content appears to be XML based on common XML patterns"""
        try:
            text = data.decode("utf-8", errors="ignore").strip()
            return text.startswith("<?xml") or text.startswith("<")
        except Exception:
            return False
