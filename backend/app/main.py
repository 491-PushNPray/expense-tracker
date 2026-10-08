from datetime import UTC, datetime

from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.models import (
    Category,
    CategoryCreate,
    CategoryUpdate,
    Transaction,
    TransactionCreate,
    TransactionUpdate,
)
from app.store import Store, get_store

settings = get_settings()
app = FastAPI(title="Expense Tracker API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/categories", response_model=list[Category])
def list_categories(store: Store = Depends(get_store)) -> list[dict]:
    return store.list("categories")


@app.get("/categories/{category_id}", response_model=Category)
def get_category(category_id: str, store: Store = Depends(get_store)) -> dict:
    return require_item(store, "categories", category_id)


@app.post("/categories", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, store: Store = Depends(get_store)) -> dict:
    return store.create("categories", payload.model_dump(mode="json"))


@app.put("/categories/{category_id}", response_model=Category)
def update_category(
    category_id: str,
    payload: CategoryUpdate,
    store: Store = Depends(get_store),
) -> dict:
    current = require_item(store, "categories", category_id)
    if current["type"] != payload.type.value and store.exists(
        "transactions", "category_id", category_id
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category type cannot change while transactions use it",
        )
    updated = store.replace("categories", category_id, payload.model_dump(mode="json"))
    return updated


@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, store: Store = Depends(get_store)) -> Response:
    require_item(store, "categories", category_id)
    if store.exists("transactions", "category_id", category_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category cannot be deleted while transactions use it",
        )
    store.delete("categories", category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/transactions", response_model=list[Transaction])
def list_transactions(store: Store = Depends(get_store)) -> list[dict]:
    return store.list("transactions")


@app.get("/transactions/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: str, store: Store = Depends(get_store)) -> dict:
    return require_item(store, "transactions", transaction_id)


@app.post(
    "/transactions", response_model=Transaction, status_code=status.HTTP_201_CREATED
)
def create_transaction(
    payload: TransactionCreate,
    store: Store = Depends(get_store),
) -> dict:
    validate_category(store, payload.category_id, payload.type.value)
    now = datetime.now(UTC)
    data = payload.model_dump(mode="json") | {"created_at": now, "updated_at": now}
    return store.create("transactions", data)


@app.put("/transactions/{transaction_id}", response_model=Transaction)
def update_transaction(
    transaction_id: str,
    payload: TransactionUpdate,
    store: Store = Depends(get_store),
) -> dict:
    current = require_item(store, "transactions", transaction_id)
    validate_category(store, payload.category_id, payload.type.value)
    data = payload.model_dump(mode="json") | {
        "created_at": current["created_at"],
        "updated_at": datetime.now(UTC),
    }
    updated = store.replace("transactions", transaction_id, data)
    return updated


@app.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: str, store: Store = Depends(get_store)
) -> Response:
    if not store.delete("transactions", transaction_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def require_item(store: Store, collection: str, item_id: str) -> dict:
    item = store.get(collection, item_id)
    if item is None:
        resource = collection.removesuffix("s").capitalize()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found",
        )
    return item


def validate_category(store: Store, category_id: str, transaction_type: str) -> None:
    category = require_item(store, "categories", category_id)
    if category["type"] != transaction_type:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Transaction type must match category type",
        )

