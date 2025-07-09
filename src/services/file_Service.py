import hashlib
import base64
import xml.etree.ElementTree as ET

class FileService:
    def __init__(self, file):
        self.file = file

    def sha1_bytes(self, data: bytes) -> str:
        return hashlib.sha1(data).hexdigest().upper()

    def get_category(self, doctype: str) -> str:
        if not doctype:
            return "Unknown"
        doctype = doctype.upper()
        if "APPRAISERSIGNATURE" in doctype:
            return "Appraiser Signature"
        if "FORM/1004" in doctype:
            return "Residential Form"
        if "FORM/REO" in doctype:
            return "REO Form"
        if "FORM/MISMO" in doctype:
            return "MISMO Form"
        if doctype.startswith("IMAGE"):
            return "Image"
        if doctype.startswith("FORM"):
            return "Generic Form"
        return "Other"

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

    def _find_content_end(self, raw: bytes, start: int, end: int, expected_sha1: str) -> tuple[bytes, int] | tuple[None, None]:
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

    def _resumen_xml(self, content_bytes: bytes) -> dict:
        """Extrae resumen simple: etiqueta raíz y etiquetas hijas (puedes usar para mostrar)."""
        try:
            text = content_bytes.decode("utf-8", errors="ignore").strip()
            root = ET.fromstring(text)
            children_tags = [child.tag for child in root]
            return {"root_tag": root.tag, "children_tags": children_tags}
        except ET.ParseError:
            return {"error": "No se pudo parsear el XML"}
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}

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
            content, content_end = self._find_content_end(raw, content_start, doc_end, sha1_expected)
            if content is None:
                pos = doc_end
                continue

            # Detectar si el contenido es XML para poder luego mostrar resumen
            is_xml = self._es_xml(content)

            result = {
                "metadata": metadata,
                "category": self.get_category(metadata.get("DOCUDOCTYPE", "")),
                "content": base64.b64encode(content).decode("ascii"),
                "is_xml": is_xml,
            }

            # Si es XML, agregamos resumen simple para usar en frontend (opcional)
            if is_xml:
                result["xml_summary"] = self._resumen_xml(content)

            results.append(result)

            pos = content_end + 2 if content_end + 2 <= length else doc_end

        return results
