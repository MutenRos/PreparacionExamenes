"""Document storage helper for attachments."""

from pathlib import Path
import hashlib
from typing import Optional

from fastapi import UploadFile

from dario_app.database import DATA_DIR


class DocumentStorageService:
    """Store attachment files locally (pluggable for S3/Azure)."""

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = Path(base_dir) if base_dir else DATA_DIR / "docs"
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _build_path(self, org_id: int, doc_type: str, doc_id: int, version_number: int, filename: str) -> Path:
        safe_name = Path(filename).name
        dir_path = self.base_dir / f"org_{org_id}" / doc_type / str(doc_id) / f"v{version_number}"
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path / safe_name

    def compute_checksum(self, content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    def _scan_content(self, content: bytes) -> tuple[str, str]:
        # Stub for antivirus integration; replace with real scanner (ClamAV/S3 AV) when available.
        if not content:
            return "clean", "empty_file"
        return "clean", "scan_stub"

    async def store_upload_file(
        self,
        file: UploadFile,
        org_id: int,
        doc_type: str,
        doc_id: int,
        version_number: int,
        storage_provider: str = "local",
    ) -> dict:
        content = await file.read()
        return await self.store_bytes(
            content=content,
            filename=file.filename,
            content_type=file.content_type or "application/octet-stream",
            org_id=org_id,
            doc_type=doc_type,
            doc_id=doc_id,
            version_number=version_number,
            storage_provider=storage_provider,
        )

    async def store_bytes(
        self,
        content: bytes,
        filename: str,
        content_type: str,
        org_id: int,
        doc_type: str,
        doc_id: int,
        version_number: int,
        storage_provider: str = "local",
    ) -> dict:
        path = self._build_path(org_id, doc_type, doc_id, version_number, filename)
        path.write_bytes(content)

        checksum = self.compute_checksum(content)
        scan_status, scan_message = self._scan_content(content)

        return {
            "storage_path": str(path),
            "size_bytes": len(content),
            "checksum": checksum,
            "scan_status": scan_status,
            "scan_message": scan_message,
            "content_type": content_type,
            "storage_provider": storage_provider,
        }

    async def load_file(self, storage_path: str) -> bytes:
        path = Path(storage_path)
        if not path.exists():
            raise FileNotFoundError(f"No existe el archivo: {storage_path}")
        return path.read_bytes()
