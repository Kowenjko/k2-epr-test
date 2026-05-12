# K2 ERP Test — Order Service

Full-stack модуль для обліку клієнтів, товарів і замовлень. Проєкт складається з FastAPI бекенду, PostgreSQL бази даних і Nuxt 4 фронтенду.

## Стек

| Частина | Технології |
|---|---|
| API | FastAPI, SQLAlchemy 2 async, Alembic, Pydantic v2, uv |
| Database | PostgreSQL 16 |
| Frontend | Nuxt 4, Vue 3, TypeScript, Pinia, Tailwind CSS 4, shadcn-vue |
| Tests | pytest, pytest-asyncio, SQLite in-memory |
| DevOps | Docker Compose, Dockerfile для API і client, Makefile |

## Можливості

- створення, перегляд і видалення клієнтів;
- створення, перегляд і видалення товарів;
- створення замовлення для конкретного клієнта;
- додавання одного або кількох товарів у замовлення;
- автоматичний розрахунок суми замовлення;
- фіксація `unit_price` у позиції замовлення, щоб старі замовлення не залежали від майбутніх змін ціни товару;
- перегляд замовлень за клієнтом;
- валідація вхідних даних на бекенді через Pydantic;
- базова обробка API-помилок на фронтенді з toast-повідомленнями.

## Структура

```text
.
├── api/                         # FastAPI застосунок
│   ├── app/
│   │   ├── core/                # config, database, router, базові моделі
│   │   └── modules/
│   │       ├── client/          # clients API, schemas, service, repository
│   │       ├── product/         # products API, schemas, service, repository
│   │       ├── order/           # orders API, schemas, service, repository
│   │       └── system/          # health endpoint
│   ├── alembic/                 # міграції БД
│   ├── tests/                   # pytest тести
│   ├── run.py                   # запуск API
│   ├── seed.py                  # demo data
│   └── pyproject.toml
├── client/                      # Nuxt 4 застосунок
│   ├── app/
│   │   ├── components/          # app та shadcn-vue компоненти
│   │   ├── layouts/default.vue  # основний layout
│   │   ├── pages/               # orders, clients, products
│   │   ├── plugins/api.ts       # typed $fetch wrapper
│   │   ├── stores/              # Pinia stores
│   │   └── utils/               # API services, links, helpers
│   ├── nuxt.config.ts
│   └── package.json
├── docker/
│   ├── api/Dockerfile
│   └── client/Dockerfile
├── docker-compose.yml           # PostgreSQL + API + client
├── Makefile
└── README.md
```

## API

Базовий префікс: `http://localhost:8000/api`

| Метод | Endpoint | Опис |
|---|---|---|
| `GET` | `/health` | health check |
| `GET` | `/clients/` | список клієнтів |
| `POST` | `/clients/` | створити клієнта |
| `GET` | `/clients/{client_id}` | отримати клієнта |
| `DELETE` | `/clients/{client_id}` | видалити клієнта |
| `GET` | `/products/` | список товарів |
| `POST` | `/products/` | створити товар |
| `GET` | `/products/{product_id}` | отримати товар |
| `DELETE` | `/products/{product_id}` | видалити товар |
| `POST` | `/orders/` | створити замовлення |
| `GET` | `/orders/{order_id}` | отримати замовлення |
| `GET` | `/orders/client/{client_id}` | замовлення клієнта |

Swagger доступний за адресою:

```text
http://localhost:8000/docs
```

## Швидкий запуск через Docker

### Варіант 1: повна інсталяція

```bash
make install
```

Ця команда:

- створює `api/.env` і `client/.env`, якщо їх ще немає;
- збирає Docker images;
- запускає контейнери у фоні;
- застосовує Alembic міграції;
- очищає і заповнює базу demo-даними.

Після цього застосунок доступний тут:

| Сервіс | URL |
|---|---|
| Frontend | http://localhost:3000 |
| API | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |

### Варіант 2: звичайний dev-запуск

```bash
make dev
```

Або напряму:

```bash
docker compose up --build
```

Після першого запуску застосуй міграції і, за потреби, заповни базу:

```bash
make migrate
make seed-reset
```

Сервіси в Docker Compose:

| Сервіс | URL |
|---|---|
| Frontend | http://localhost:3000 |
| API | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |

## Локальний запуск без Docker

### Backend

Потрібні Python `>=3.14`, `uv` і доступна PostgreSQL база.

```bash
cd api
cp .env.example .env
uv sync
uv run alembic upgrade head
uv run python run.py
```

Приклад `api/.env`:

```env
DATABASE_URL=postgresql+asyncpg://k2epr:k2epr@localhost:5432/k2epr
```

### Frontend

Потрібні Node.js 22 і Yarn.

```bash
cd client
cp .env.example .env
yarn install
yarn dev
```

Приклад `client/.env`:

```env
NUXT_API_BASE_URL=http://localhost:8000/api/
NUXT_API_URL_SERVER=http://api:8000/api/
```

Якщо запускаєш API локально без Docker, для SSR-запитів можна поставити:

```env
NUXT_API_URL_SERVER=http://localhost:8000/api/
```

## Тести

Тести бекенду використовують SQLite in-memory, тому PostgreSQL для них не потрібен.

```bash
make test
```
або локально

```bash
cd api
uv run pytest -v
```

Покриті базові сценарії:

- створення клієнта;
- перевірка дублювання email;
- створення товару;
- створення замовлення з розрахунком `total_amount`;
- помилка для неіснуючого клієнта;
- помилка для замовлення без товарів;
- отримання замовлень за клієнтом.

## Корисні команди

| Команда | Опис |
|---|---|
| `make install` | створити env-файли, зібрати images, підняти контейнери, виконати міграції і seed |
| `make dev` | запустити Docker Compose з rebuild |
| `make up` | запустити контейнери у фоні |
| `make build` | зібрати Docker images |
| `make down` | зупинити контейнери |
| `make restart` | перезапустити контейнери |
| `make logs` | дивитися логи |
| `make ps` | статус контейнерів |
| `make migrate` | застосувати Alembic міграції |
| `make revision msg="..."` | створити нову autogenerate-міграцію |
| `make downgrade` | відкотити останню міграцію |
| `make seed` | додати demo-дані |
| `make seed-reset` | очистити дані і заново заповнити demo-даними |
| `make test` | запустити тести |
| `make env-api` | створити `api/.env` з прикладу, якщо файла ще немає |
| `make env-client` | створити `client/.env` з прикладу, якщо файла ще немає |

## Приклад створення замовлення

```json
{
  "client_id": 1,
  "notes": "Передзвонити перед доставкою",
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 3,
      "quantity": 1
    }
  ]
}
```

API перевіряє існування клієнта і товарів, бере поточну ціну товару, записує її в `OrderItem.unit_price`, рахує subtotal для кожної позиції і фінальний `total_amount`.

## Нотатки по реалізації

- API має модульну структуру: `client`, `product`, `order`, `system`.
- Бізнес-логіка винесена в service layer, робота з БД — у repository layer.
- Для моделей використовується SQLAlchemy ORM з async session.
- Frontend має окремі service-файли для API-запитів: `client.services.ts`, `product.services.ts`, `order.services.ts`.
- Кошик замовлення реалізований через Pinia store `cart.ts`.
- Runtime API URL налаштовуються через `NUXT_API_BASE_URL` і `NUXT_API_URL_SERVER`.
