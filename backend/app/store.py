from functools import lru_cache
from typing import Any, Protocol

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from app.config import get_settings


class Store(Protocol):
    def list(self, collection: str) -> list[dict[str, Any]]: ...

    def get(self, collection: str, item_id: str) -> dict[str, Any] | None: ...

    def create(self, collection: str, data: dict[str, Any]) -> dict[str, Any]: ...

    def replace(
        self, collection: str, item_id: str, data: dict[str, Any]
    ) -> dict[str, Any] | None: ...

    def delete(self, collection: str, item_id: str) -> bool: ...

    def exists(self, collection: str, field: str, value: Any) -> bool: ...


class FirestoreStore:
    def __init__(self) -> None:
        settings = get_settings()
        try:
            app = firebase_admin.get_app()
        except ValueError:
            options = (
                {"projectId": settings.firebase_project_id}
                if settings.firebase_project_id
                else None
            )
            credential = (
                credentials.Certificate(str(settings.google_application_credentials))
                if settings.google_application_credentials
                else None
            )
            app = firebase_admin.initialize_app(credential=credential, options=options)
        self.db = firestore.client(app)

    def list(self, collection: str) -> list[dict[str, Any]]:
        return [self._document(snapshot) for snapshot in self.db.collection(collection).stream()]

    def get(self, collection: str, item_id: str) -> dict[str, Any] | None:
        snapshot = self.db.collection(collection).document(item_id).get()
        return self._document(snapshot) if snapshot.exists else None

    def create(self, collection: str, data: dict[str, Any]) -> dict[str, Any]:
        reference = self.db.collection(collection).document()
        reference.set(data)
        return {"id": reference.id, **data}

    def replace(
        self, collection: str, item_id: str, data: dict[str, Any]
    ) -> dict[str, Any] | None:
        reference = self.db.collection(collection).document(item_id)
        if not reference.get().exists:
            return None
        reference.set(data)
        return {"id": item_id, **data}

    def delete(self, collection: str, item_id: str) -> bool:
        reference = self.db.collection(collection).document(item_id)
        if not reference.get().exists:
            return False
        reference.delete()
        return True

    def exists(self, collection: str, field: str, value: Any) -> bool:
        query = (
            self.db.collection(collection)
            .where(filter=FieldFilter(field, "==", value))
            .limit(1)
        )
        return any(query.stream())

    @staticmethod
    def _document(snapshot: Any) -> dict[str, Any]:
        return {"id": snapshot.id, **snapshot.to_dict()}


@lru_cache
def get_store() -> Store:
    return FirestoreStore()
