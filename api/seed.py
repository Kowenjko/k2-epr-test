"""
seed.py — заповнює базу тестовими даними.

Запуск:
    uv run python seed.py
    uv run python seed.py --reset   # спочатку видалить усі наявні дані
"""

import asyncio
import argparse
from decimal import Decimal

from sqlalchemy import delete, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal, engine, Base
from app.modules.client.models import Client
from app.modules.product.models import Product
from app.modules.order.models import Order, OrderItem

from app.modules.order.enums import OrderStatus

# ── Seed data ─────────────────────────────────────────────────────────────────

CLIENTS = [
    {
        "name": "Іван Петренко",
        "email": "ivan.petrenko@example.com",
        "phone": "+380501234567",
    },
    {
        "name": "Олена Коваль",
        "email": "olena.koval@example.com",
        "phone": "+380671234567",
    },
    {
        "name": "Михайло Бондар",
        "email": "mykhailo.bondar@example.com",
        "phone": "+380931234567",
    },
    {"name": "Софія Мельник", "email": "sofia.melnyk@example.com", "phone": None},
    {
        "name": "Андрій Шевченко",
        "email": "andriy.shevchenko@example.com",
        "phone": "+380631234567",
    },
]

PRODUCTS = [
    {
        "name": "Ноутбук Dell XPS 15",
        "description": '15.6" OLED, Intel Core i7, 32 GB RAM, 1 TB SSD',
        "price": Decimal("54999.00"),
        "sku": "DELL-XPS15-I7",
    },
    {
        "name": "Механічна клавіатура Keychron K2",
        "description": "Бездротова, RGB підсвітка, switches Brown",
        "price": Decimal("3299.00"),
        "sku": "KEYCHRON-K2-BR",
    },
    {
        "name": 'Монітор LG UltraWide 34"',
        "description": "3440×1440, IPS, 144Hz, HDR10",
        "price": Decimal("18750.00"),
        "sku": "LG-34UM88-W",
    },
    {
        "name": "Миша Logitech MX Master 3",
        "description": "Бездротова, 7 кнопок, для Mac та Windows",
        "price": Decimal("2450.00"),
        "sku": "LOGI-MXM3",
    },
    {
        "name": "Веб-камера Logitech C920",
        "description": "Full HD 1080p, вбудований мікрофон",
        "price": Decimal("2890.00"),
        "sku": "LOGI-C920",
    },
    {
        "name": "USB-хаб Anker 7-in-1",
        "description": "USB-C, HDMI 4K, 3×USB-A, SD, PD 100W",
        "price": Decimal("1199.00"),
        "sku": "ANKER-7IN1-HUB",
    },
    {
        "name": "SSD Samsung 970 EVO 1TB",
        "description": "M.2 NVMe, 3500 MB/s read, 3300 MB/s write",
        "price": Decimal("3850.00"),
        "sku": "SAM-970EVO-1TB",
    },
    {
        "name": "Навушники Sony WH-1000XM5",
        "description": "Бездротові, ANC, 30 год автономності",
        "price": Decimal("9999.00"),
        "sku": "SONY-WH1000XM5",
    },
]


ORDERS = [
    (
        0,
        OrderStatus.DELIVERED,
        "Термінова доставка",
        [(0, 1), (1, 1), (3, 1)],
    ),
    (
        0,
        OrderStatus.CONFIRMED,
        None,
        [(6, 2), (5, 1)],
    ),
    (
        1,
        OrderStatus.PENDING,
        "Передзвонити перед доставкою",
        [(2, 1), (3, 1), (4, 1)],
    ),
    (
        1,
        OrderStatus.SHIPPED,
        None,
        [(7, 1)],
    ),
    (
        2,
        OrderStatus.CONFIRMED,
        "Доставка до офісу",
        [(0, 2), (2, 1)],
    ),
    (
        3,
        OrderStatus.PENDING,
        None,
        [(1, 1), (3, 1), (5, 2)],
    ),
    (
        4,
        OrderStatus.DELIVERED,
        "Корпоративне замовлення",
        [(0, 3), (1, 3), (3, 3), (4, 2)],
    ),
    (
        4,
        OrderStatus.CANCELLED,
        "Клієнт відмовився",
        [(7, 1), (2, 1)],
    ),
]


# ── Helpers ───────────────────────────────────────────────────────────────────


async def reset_db(session: AsyncSession) -> None:
    """Видаляє всі рядки у зворотному порядку залежностей."""
    print("  🗑  Очищення бази…")
    await session.execute(delete(OrderItem))
    await session.execute(delete(Order))
    await session.execute(delete(Product))
    await session.execute(delete(Client))
    await session.commit()
    print("  ✓  Базу очищено")


async def seed(reset: bool = False) -> None:
    async with AsyncSessionLocal() as session:
        if reset:
            await reset_db(session)

        # ── Clients ──────────────────────────────────────────────────────────
        print("\n👤 Створення клієнтів…")
        clients: list[Client] = []
        for data in CLIENTS:
            client = Client(**data)
            session.add(client)
            clients.append(client)
        await session.flush()

        for c in clients:
            print(f"  ✓  [{c.id:>2}] {c.name} <{c.email}>")

        # ── Products ─────────────────────────────────────────────────────────
        print("\n📦 Створення товарів…")
        products: list[Product] = []
        for data in PRODUCTS:
            product = Product(**data)
            session.add(product)
            products.append(product)
        await session.flush()

        for p in products:
            print(f"  ✓  [{p.id:>2}] {p.name} — {p.price} грн  (SKU: {p.sku})")

        # ── Orders ────────────────────────────────────────────────────────────
        print("\n🛒 Створення замовлень…")
        for client_idx, status, notes, items_data in ORDERS:
            client = clients[client_idx]
            order = Order(
                client_id=client.id,
                status=status,
                notes=notes,
                total_amount=0,
            )
            session.add(order)
            await session.flush()

            total = Decimal("0")
            for product_idx, qty in items_data:
                product = products[product_idx]
                unit_price = product.price
                subtotal = unit_price * qty
                total += subtotal
                session.add(
                    OrderItem(
                        order_id=order.id,
                        product_id=product.id,
                        quantity=qty,
                        unit_price=unit_price,
                    )
                )

            order.total_amount = total
            await session.flush()

            items_desc = ", ".join(f"{products[pi].name} ×{q}" for pi, q in items_data)
            print(
                f"  ✓  Замовлення #{order.id:>2}  [{status.value:<10}]"
                f"  {total:>10.2f} грн  →  {client.name}"
            )
            print(f"            {items_desc}")

        await session.commit()

    print("\n✅ Seed завершено!")
    print(f"   Клієнтів : {len(CLIENTS)}")
    print(f"   Товарів  : {len(PRODUCTS)}")
    print(f"   Замовлень: {len(ORDERS)}")


# ── Entry point ───────────────────────────────────────────────────────────────


async def main() -> None:
    parser = argparse.ArgumentParser(description="Seed demo data")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Видалити наявні дані перед заповненням",
    )
    args = parser.parse_args()
    await seed(reset=args.reset)


if __name__ == "__main__":
    asyncio.run(main())
