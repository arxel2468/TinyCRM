TinyCRM — Architecture, Decisions, and How Things Work

1) What we built
- Goal: A production-ready, minimal CRM backend with a simple web UI.
- Stack:
  - Backend: Django + Django REST Framework (DRF), JWT auth (simplejwt), Postgres
  - Infra: Render Web Service + Render Postgres (Internal URL)
  - Frontend: Next.js (Pages Router) deployed to Vercel
  - CI: GitHub Actions (pytest + SQLite)
  - Docs: drf-spectacular (OpenAPI) → Swagger UI at /api/docs

Deliverables
- REST API with Contacts, Companies, Deals
- JWT auth + user data isolation
- Filtering, search, ordering, pagination with page_size
- Tests (pytest-django), CI green, deploy to production
- Minimal Next.js UI: login, contacts CRUD-lite, companies & deals (create/list), deployed and integrated via CORS

2) High-level architecture (how pieces talk)
- Browser (Next.js @ Vercel) → HTTPS → Django API @ Render → Postgres
- Auth: UI obtains JWT from /api/token, stores in localStorage (demo), sends as Authorization: Bearer <token> on each request
- CORS: Backend allows the Vercel domain; denies others
- Docs: /api/docs (Swagger) and /api/schema (OpenAPI)
- CI: On each PR/push, GitHub Actions runs tests with SQLite to avoid external DB

3) Data model (crm/models.py)
- Contact
  - user (FK to auth user; ownership)
  - name, email, tags (comma-separated string)
  - Constraints: Unique (user, email)
  - Ordering: by -updated_at

- Company
  - user (owner), name (unique per user), website, created_at
  - Constraints: Unique (user, name)
  - Ordering: name

- Deal
  - user (owner), company (FK to Company), title, amount (decimal), stage (new/qualified/won/lost), close_date
  - Ordering: -updated_at

Why: The “owned-by-user” pattern gives a clean multi-tenant model where each user sees only their data.

4) API design and DRF patterns
- URL routing
  - Router-registered endpoints:
    - /api/contacts/
    - /api/companies/
    - /api/deals/
  - Auth:
    - POST /api/token/ → {access, refresh}
    - POST /api/token/refresh/
  - Utility: GET /api/me/ (returns username/email for the current user)
  - Docs: /api/schema/, /api/docs/

- Viewsets and permissions
  - OwnedModelViewSet base:
    - get_queryset() filters by request.user
    - perform_create() sets user=request.user
  - IsOwner object permission:
    - Enforces per-object ownership (403/404 for foreign objects)
  - All endpoints default to IsAuthenticated + JWTAuthentication

- Serializers
  - Simple ModelSerializer for Contact, Company
  - DealSerializer:
    - company_name read-only
    - __init__ restricts company queryset to the current user’s companies (prevents cross-tenant reference on create)

- Filtering, search, ordering, pagination
  - Search: SearchFilter on relevant fields (e.g., name/email)
  - Ordering: OrderingFilter with explicit ordering_fields
  - Filtering: django-filter FilterSet classes:
    - ContactFilter: name/email icontains, tags multi-term, created_before/after
    - CompanyFilter: name icontains
    - DealFilter: min/max amount, stage, close_before/after
  - Pagination:
    - Custom PageNumberPagination with page_size_query_param="page_size"
    - Default page_size=20, client can request ?page_size=10 (capped by max_page_size=100)

- OpenAPI docs (drf-spectacular)
  - Auto-generated schema + Swagger UI at /api/docs
  - Bearer JWT security scheme displayed via SPECTACULAR_SETTINGS

5) Authentication and session flow (JWT)
- Endpoints:
  - POST /api/token/ with username/password → returns access and refresh
  - POST /api/token/refresh/ with refresh → returns new access
- UI stores access in localStorage (demo-simple).
  - Production note: prefer HttpOnly cookies via a proxy route to avoid XSS exposure
- DRF config:
  - DEFAULT_AUTHENTICATION_CLASSES = JWT
  - DEFAULT_PERMISSION_CLASSES = IsAuthenticated
- Browsable API:
  - Requires manual “Authorize” in Swagger (Bearer <token>)

6) Ownership and data isolation
- How we enforce isolation:
  - Queryset filtered by request.user everywhere
  - IsOwner permission checks object.user_id == request.user.id
  - Foreign keys constrained at serializer level (deal.company must belong to the same user)
- Result: Users can’t view/edit objects created by others, and can’t link deals to other users’ companies

7) Settings, env vars, and configuration (config/settings.py)
- Environment parsing:
  - SECRET_KEY (random, long string; no quotes)
  - DEBUG (False in prod)
  - ALLOWED_HOSTS (comma-separated hostnames; no scheme)
  - DATABASE_URL (dj-database-url parses; prefer Render Internal URL in prod)
  - CSRF_TRUSTED_ORIGINS (https://your-domain)
  - TIME_ZONE (Asia/Kolkata)

- CORS
  - django-cors-headers
  - Strategy used:
    - CORS_ALLOWED_ORIGINS from env (comma-separated)
    - CORS_ALLOW_ALL_ORIGINS = not bool(CORS_ALLOWED_ORIGINS) → wide-open in dev, restricted in prod
  - For Vercel UI: set CORS_ALLOWED_ORIGINS=https://<vercel-app>.vercel.app

- Security/middleware
  - SECURE_PROXY_SSL_HEADER for Render
  - Whitenoise for static files (admin assets)
  - CSRF: trust the Render domain for admin; not used for API since we rely on JWT

- Logging
  - Root logger sends INFO to console (visible in Render logs)
  - Easy to extend with Sentry later

- DRF throttling (rate limiting)
  - DEFAULT_THROTTLE_CLASSES: UserRateThrottle
  - DEFAULT_THROTTLE_RATES: {"user": "1000/day"} (example)

- Static files
  - STATIC_ROOT staticfiles
  - Create staticfiles/.gitkeep to silence warnings in dev

8) Database: Render Postgres (Internal vs External)
- Internal Database URL:
  - Only accessible from other Render services
  - Preferred for the deployed web service (fast, private)
- External Database URL:
  - Public hostname, ?sslmode=require
  - Use only if connecting from your laptop (not needed here)
- Local dev:
  - Either local Postgres with DATABASE_URL in .env
  - Or SQLite fallback if no DATABASE_URL set

9) Deployment — Render (backend)
- Build command:
  - pip install -r requirements.txt && python manage.py collectstatic --noinput
- Start command:
  - bash -c "python manage.py migrate && python manage.py create_default_superuser && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT"
  - create_default_superuser is a custom management command that reads DJANGO_SUPERUSER_* env vars and creates the admin user if missing
- Required env vars on Render:
  - SECRET_KEY=<long random>
  - DEBUG=False
  - ALLOWED_HOSTS=tinycrm-xxxx.onrender.com
  - DATABASE_URL=<Render Internal DB URL>
  - CSRF_TRUSTED_ORIGINS=https://tinycrm-xxxx.onrender.com
  - CORS_ALLOWED_ORIGINS=https://<vercel-app>.vercel.app (and optionally http://localhost:3000)
  - DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD
- Common deploy issues we solved:
  - 400 Bad Request: ALLOWED_HOSTS was set with scheme; fix to hostname only
  - DB connection failing in CI: force SQLite in CI (DATABASE_URL=sqlite:////tmp/ci.sqlite3)
  - Staticfiles warning: added staticfiles/.gitkeep
  - Admin CSRF: added CSRF_TRUSTED_ORIGINS with https:// scheme

10) CI — GitHub Actions
- Why SQLite in CI:
  - Fast, no external network dependency (Render Internal DB not reachable)
- Workflow highlights:
  - Install deps
  - cp .env.example .env and set DEBUG=False
  - Set env for test step:
    - DATABASE_URL=sqlite:////tmp/ci.sqlite3
    - SECRET_KEY=ci-secret
    - DJANGO_SETTINGS_MODULE=config.settings
  - Run migrate and pytest -q
- Optional: Add ruff and black checks before tests

11) Testing — pytest-django
- Fixtures
  - user: creates a test user
  - auth_client: APIClient with a JWT access token for the user (using RefreshToken.for_user)
- Tests we included
  - Auth required for endpoints (401 without token)
  - Create contact (201), isolation across users (403/404)
  - Filters/search/pagination (including page_size param)
  - Company/Deal flow: create company → create deal → filter by min_amount
  - Prevent cross-tenant referencing another user’s company (400)
  - /api/me returns current user info
- Lessons
  - DRF default pagination ignores page_size unless you enable it in a custom pagination class
  - Small typos in tests can block collection; formatters/linters help catch this early

12) Frontend — Next.js (Pages Router) on Vercel
- Directory structure (monorepo):
  - Backend (root): Django app
  - Frontend: tinycrm-ui/ (Next.js)
- Key pages/components
  - pages/login.js: POST /api/token → store access in localStorage → redirect
  - pages/contacts.js: list + create; uses apiGet/apiPost with Authorization header
  - pages/companies.js: list + create
  - pages/deals.js: list with min_amount filter + create (select company)
  - components/Nav.js: uses next/link for navigation; logout clears token
  - utils/api.js: fetch helpers; redirects to /login on 401
- Env var
  - NEXT_PUBLIC_API_BASE_URL=https://<render-app>.onrender.com
- Lint/build gotchas we fixed
  - Use <Link> instead of <a href> for internal nav (Next.js ESLint rule)
  - Manage useEffect dependencies to avoid exhaustive-deps warnings
- Security note for demo
  - localStorage for JWT is acceptable for demo
  - Production-grade approach: HttpOnly cookie via Next API route proxy

13) CORS and CSRF interplay
- API only (JWT) → CSRF not required for API calls (no session auth)
- Admin needs CSRF_TRUSTED_ORIGINS with https://your-domain
- CORS settings
  - In dev: allow all (or include localhost:3000)
  - In prod: CORS_ALLOWED_ORIGINS = https://<vercel-app>.vercel.app
- Preflight: Django-cors-headers handles OPTIONS if origin and headers are allowed

14) Git workflow we used
- One feature per branch (feat/…, fix/…, ci/…)
- Small commits with clear messages (feat(api): …, test: …, ci: …)
- PR even for solo dev → CI runs → squash & merge
- Rebase branch if it lives >1 day (git fetch; git rebase origin/main; resolve; push --force-with-lease)
- Post-merge: delete branch to keep the repo clean
- Monorepo: Vercel points to tinycrm-ui/ subdirectory; Render builds from root

15) Common pitfalls we hit and how we fixed them
- 401 in browser: no Authorization header → use Swagger Authorize or curl with Bearer token
- page_size not working: added custom pagination class to enable page_size_query_param
- CI DB error: forced SQLite via env in workflow
- 400 on prod: ALLOWED_HOSTS included scheme; must be hostname only
- CORS misconfig: tried setting CORS_ALLOW_ALL_ORIGINS as string → use CORS_ALLOWED_ORIGINS list, and fallback logic
- Next.js build failed on Vercel: ESLint errors (no-html-link-for-pages); fixed by using <Link> and correcting hooks
- Staticfiles warning: added staticfiles/.gitkeep

16) Useful commands (cheat sheet)
- Generate SECRET_KEY:
  - python -c "import secrets; print(secrets.token_urlsafe(64))"
- Local run:
  - python manage.py migrate
  - python manage.py runserver
- Create superuser (prod without shell):
  - Add DJANGO_SUPERUSER_* envs, then run on start:
    - python manage.py create_default_superuser
- JWT curl:
  - curl -s -X POST https://<domain>/api/token/ -H "Content-Type: application/json" -d '{"username":"admin","password":"pass"}'
- Authenticated curl:
  - curl -H "Authorization: Bearer <ACCESS>" https://<domain>/api/contacts/
- CI with SQLite (environment)
  - DATABASE_URL=sqlite:////tmp/ci.sqlite3

17) Future improvements (backlog)
- Background jobs with Celery + Redis (weekly deals digest, CSV export)
- More tests (error cases, permission edge cases, serializer validation)
- Sentry for error tracking
- Docker for local parity with prod
- HttpOnly cookie auth via Next.js API routes
- Better tags model (ManyToMany) and bulk import/export
- Role-based permissions (teams) and audit logs
- Rate-limit tuning per endpoint and IP throttles
