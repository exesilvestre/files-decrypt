

class FileService:
    def __init__(self, file):
        self.file = file

    def get_parsed_file(self, file):
        try:
            return {"status": "success", "data": file.filename}
        except Exception as e:
            return {"status": "error", "message": str(e)}