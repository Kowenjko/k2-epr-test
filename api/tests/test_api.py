"""
Інтеграційні тести з SQLite (in-memory) — не потребують PostgreSQL.
"""

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="function")
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with session_factory() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


# ── Клієнти ──────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_create_client(client):
    resp = await client.post(
        "/api/clients/",
        json={
            "name": "Тест Клієнт",
            "email": "test@example.com",
            "phone": "+380501234567",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "test@example.com"
    assert data["id"] > 0


@pytest.mark.asyncio
async def test_create_client_duplicate_email(client):
    payload = {"name": "Клієнт 1", "email": "dup@example.com"}
    await client.post("/api/clients/", json=payload)
    resp = await client.post("/api/clients/", json=payload)
    assert resp.status_code == 409


# ── Товари ────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_create_product(client):
    resp = await client.post(
        "/api/products/",
        json={
            "name": "Ноутбук",
            "price": "25000.00",
            "sku": "LAPTOP-001",
        },
    )
    assert resp.status_code == 201
    assert resp.json()["name"] == "Ноутбук"


# ── Замовлення ────────────────────────────────────────────────────────────────


@pytest.fixture
def base_data():
    return {
        "client": {"name": "Іван", "email": "ivan@example.com"},
        "product": {"name": "Мишка", "price": "500.00"},
    }


@pytest.mark.asyncio
async def test_create_order_calculates_total(client, base_data):
    cl = (await client.post("/api/clients/", json=base_data["client"])).json()
    pr = (await client.post("/api/products/", json=base_data["product"])).json()

    resp = await client.post(
        "/api/orders/",
        json={
            "client_id": cl["id"],
            "items": [{"product_id": pr["id"], "quantity": 3}],
        },
    )
    assert resp.status_code == 201
    order = resp.json()
    # 500.00 × 3 = 1500.00
    assert float(order["total_amount"]) == 1500.0


@pytest.mark.asyncio
async def test_order_requires_existing_client(client, base_data):
    pr = (await client.post("/api/products/", json=base_data["product"])).json()
    resp = await client.post(
        "/api/orders/",
        json={
            "client_id": 99999,
            "items": [{"product_id": pr["id"], "quantity": 1}],
        },
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_order_requires_at_least_one_item(client, base_data):
    cl = (await client.post("/api/clients/", json=base_data["client"])).json()
    resp = await client.post(
        "/api/orders/",
        json={
            "client_id": cl["id"],
            "items": [],
        },
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_get_orders_by_client(client, base_data):
    cl = (await client.post("/api/clients/", json=base_data["client"])).json()
    pr = (await client.post("/api/products/", json=base_data["product"])).json()

    for _ in range(3):
        await client.post(
            "/api/orders/",
            json={
                "client_id": cl["id"],
                "items": [{"product_id": pr["id"], "quantity": 1}],
            },
        )

    resp = await client.get(f"/api/orders/client/{cl['id']}")
    assert resp.status_code == 200
    assert len(resp.json()) == 3
