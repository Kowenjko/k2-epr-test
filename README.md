# K2 ERP Test — Order Service

**Backend:** FastAPI · PostgreSQL · SQLAlchemy 2 (async) · Alembic · Pydantic v2 · uv  
**Frontend:** Nuxt 4 · Pinia · Tailwind CSS · shadcn-vue · TypeScript


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
│   ├── seed.py                  # seed
│   └── pyproject.toml
├── client/                      # Nuxt 4
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
make c.install
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

---
 
## Чому саме такий підхід
 
| Рішення | Причина |
|---|---|
| **FastAPI**  | В тестовому вказано що можна використовувати інший близький Python web framework|
| **Alembic**  | Дозволяє контролювати міграціїї до бази даних|
| **Pydantic**  | Використовував для валідації даних|
| **SQLAlchemy**  |Для спрощеної роботи з базами даних|
| **uv** замість pip | 10-100× швидше, `uv.lock` — детерміновані збірки |
| **Nuxt 4**  | Новітня версія, `app/` директорія|
| **Tailwind CSS**  | Стилі можна прописувати класами |
| **shadcn-vue**  | Компоненти —  легко кастомізувати |
| **Pinia**  | Глобальний стан менеджер для vue |
| **TypeScript**  | Типізована мова програмування, яка дозволяє уникнути багів під час розробки |

 
---
