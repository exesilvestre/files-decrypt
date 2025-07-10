from typing import Tuple


class DocumentBlockExtractor:
    def extract_document_boundaries(
        self, raw: bytes, pos: int, length: int
    ) -> Tuple[int, int]:
        """
        Find start and end positions of a document block.
        Documents are delimited by "%%DOCU" markers.
        """
        start = raw.find(b"%%DOCU", pos)
        if start == -1:
            return -1, -1

        # Find next document marker or use end of file
        end = raw.find(b"%%DOCU", start + 1)
        return start, end if end != -1 else length

    def find_signature_position(self, raw: bytes, start: int, end: int) -> int:
        """Find the signature marker that indicates start of metadata section"""
        return raw.find(b"_SIG/D.C.", start, end)
