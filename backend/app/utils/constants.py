MAX_UPLOAD_SIZE = 5 * 1024 * 1024
FORBIDDEN_EXTENSIONS = [".exe", ".bat", ".cmd", ".sh", ".js", ".msi"]
FORBIDDEN_MIME_PREFIXES = [
	"application/x-dosexec",
	"application/x-sh",
	"application/x-bat",
]