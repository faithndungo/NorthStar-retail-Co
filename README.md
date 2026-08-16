# NorthStar Retail Customer Support

NorthStar is a React and Django application for customer order tracking,
inventory checks, restock alerts, and return requests.

## Local setup

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

The API runs at `http://127.0.0.1:8000/api/`.

### Frontend

In another terminal:

```bash
cd NorthStar-frontend
cp .env.example .env
pnpm install
pnpm dev
```

The site runs at `http://localhost:5173`. Vite proxies `/api` requests to the
local Django server.

Demo order details after running `seed_demo`:

- Order number: `NS-10023`
- Email: `demo@northstar.test`

## Verification

```bash
cd backend
python manage.py check
python manage.py test

cd ../NorthStar-frontend
pnpm lint
pnpm test
pnpm build
```

## Configuration

Production deployments must set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false`, and
`DJANGO_ALLOWED_HOSTS`. `RETURN_WINDOW_DAYS` defaults to 30. The frontend uses
`VITE_API_BASE`, which defaults to `/api`.

Do not commit local databases, virtual environments, `.env` files, or Python
cache files. The root `.gitignore` excludes these artifacts.
