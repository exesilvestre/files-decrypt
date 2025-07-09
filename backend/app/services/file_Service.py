import hashlib
import base64
from db.mongo_client import collection
from utils.detect_category import get_category
from utils.unsecure_files import is_forbidden_file


class FileService:
    def __init__(self, file):
        self.file = file

    def sha1_bytes(self, data: bytes) -> str:
        return hashlib.sha1(data).hexdigest().upper()

    def _extract_metadata(self, header: bytes) -> dict:
        try:
            text = header.decode("ascii", errors="ignore")
        except Exception:
            return {}
        metadata = {}
        for line in text.splitlines():
            if "/" in line:
                key, val = line.split("/", 1)
                key = ''.join(filter(str.isalnum, key.strip().upper()))
                metadata[key] = val.strip()
        return metadata

    def _find_content_end(
        self,
        raw: bytes,
        start: int,
        end: int,
        expected_sha1: str
    ) -> tuple[bytes, int] | tuple[None, None]:
        last_marker = raw.rfind(b"**", start, end)
        if last_marker == -1:
            last_marker = end
        content = raw[start:last_marker]
        if self.sha1_bytes(content) == expected_sha1:
            return content, last_marker
        return None, None

    def _es_xml(self, content_bytes: bytes) -> bool:
        """Detecta si el contenido parece ser XML (por encabezado típico)."""
        try:
            text = content_bytes.decode("utf-8", errors="ignore").strip()
            return text.startswith("<?xml") or text.startswith("<")
        except Exception:
            return False

    def is_text(self, data: bytes) -> bool:
        """Detecta si bytes representan texto UTF-8 válido."""
        try:
            data.decode("utf-8")
            return True
        except UnicodeDecodeError:
            return False

    def get_parsed_file(self):
        raw = self.file.file.read()
        results = []
        pos = 0
        length = len(raw)

        while True:
            doc_start = raw.find(b"%%DOCU", pos)
            if doc_start == -1:
                break

            doc_end = raw.find(b"%%DOCU", doc_start + 1)
            if doc_end == -1:
                doc_end = length

            sig_pos = raw.find(b"_SIG/D.C.", doc_start, doc_end)
            if sig_pos == -1:
                pos = doc_start + 6
                continue

            nulls_pos = raw.find(b"\x00\x00", sig_pos, doc_end)
            if nulls_pos == -1:
                pos = doc_end
                continue

            metadata = self._extract_metadata(raw[doc_start:nulls_pos])
            if not metadata:
                pos = doc_end
                continue

            sha1_expected = metadata.get("SHA1", "").upper()
            content_start = nulls_pos + 2

            content, content_end = self._find_content_end(
                raw, content_start, doc_end, sha1_expected
            )
            if content is None:
                pos = doc_end
                continue

            filename = metadata.get("FILENAME", "")
            content_type = metadata.get("CONTENTTYPE", "")

            if is_forbidden_file(filename, content_type):
                raise Exception(f"Forbidden file detected inside container:" 
                                f"{filename}")

            is_xml = self._es_xml(content)

            if self.is_text(content):
                content_to_store = content.decode("utf-8", errors="ignore")
                encoded = False
            else:
                content_to_store = base64.b64encode(content).decode("ascii")
                encoded = True

            full_result = {
                "metadata": metadata,
                "category": get_category(metadata.get("DOCUDOCTYPE", "")),
                "is_xml": is_xml,
                "content": content_to_store,
                "encoded_true": encoded
            }

            guid = metadata.get("GUID")

            if guid:
                full_result["guid"] = guid
                collection.update_one(
                    {"guid": guid},
                    {"$set": full_result},
                    upsert=True
                )

            results.append({
                "guid": guid,
                "filename": metadata.get("FILENAME"),
                "category": get_category(metadata.get("DOCUDOCTYPE", "")),
                "metadata": metadata
            })

            pos = content_end + 2 if content_end + 2 <= length else doc_end

        return results
