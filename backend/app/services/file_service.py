from typing import List, Dict, Any
from .document_processor import DocumentProcessor
from .document_block_extractor import DocumentBlockExtractor


class FileService:
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.block_extractor = DocumentBlockExtractor()

    def get_parsed_file(self, file) -> List[Dict[str, Any]]:
        """
        Parse uploaded file and extract all documents.
        Returns list of processed documents.
        """
        raw = file.file.read()
        results = []
        pos = 0
        length = len(raw)

        # Process file sequentially, document by document
        while pos < length:
            start, end = self.block_extractor.extract_document_boundaries(
                raw, pos, length
            )
            if start == -1:
                break  # No more documents found

            result, next_pos = self.document_processor.process_document(raw, start, end)
            if result:
                results.append(result)

            pos = next_pos

        return results
