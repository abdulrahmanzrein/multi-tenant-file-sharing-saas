import uuid
from abc import ABC, abstractmethod
from pathlib import Path

from fastapi import UploadFile


class StorageBackend(ABC):

    @abstractmethod
    def save_file(self, upload: UploadFile, tenant_id: uuid.UUID) -> tuple[str, int]:
        ...

    @abstractmethod
    def get_file_path(self, storage_path: str) -> Path:
        ...

    @abstractmethod
    def delete_file(self, storage_path: str) -> None:
        ...
