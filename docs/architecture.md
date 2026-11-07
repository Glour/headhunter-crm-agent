# Architecture

HeadHunter CRM collects vacancy information, scores it against a candidate profile, stores the results and prepares drafts for review. Chat and external-form workflows use separate entry points. The components are designed to be usable separately: scoring and persistence do not require a browser or an LLM provider.

## Main flow

1. A search client retrieves vacancies and converts them to the `Vacancy` model.
2. `score_vacancy()` produces a deterministic score, decision, reasons and penalties.
3. `CRMRepository` stores vacancies and their scores in SQLite. It records applications, feedback and learning signals separately.
4. The application service creates a draft when it passes the configured thresholds and duplicate checks.
5. FastAPI exposes the CRM data to the React dashboard. Browser-based workflows and Telegram review are separate entry points.

The score is a prioritization aid, not a guarantee of suitability. Profile settings and feedback affect ranking. A failed or uncertain external interaction should be reviewed before taking another action.

## Boundaries

- `domain.py` defines vacancy, candidate and scoring result data structures; `scoring.py` contains deterministic scoring rules and retains the existing model imports for compatibility.
- `repository.py` owns SQLite operations. `text_cleaning.py` contains deterministic text normalization without importing generation providers.
- `agent.py` coordinates search, scoring, deduplication and drafting through a search-client interface.
- `hh_public.py`, `hh_client.py`, `hh_browser.py`, `hh_chat.py` and `telegram_agent.py` implement external integrations.
- `api.py` exposes HTTP endpoints; the dashboard is a separate React/Vite application.
- `demo.py` uses a temporary database and synthetic records. It exposes read-only endpoints and does not register the production routers.

## Operational safety

External actions are configured separately from drafting. Live scripts use explicit gates and may be affected by local configuration, so their behavior should be checked before execution. Captcha, authentication and uncertain delivery states require manual attention. The workspace is intended for a trusted local or appropriately protected deployment; its HTTP endpoints should not be exposed publicly without authentication and network controls.

## Storage and API

SQLite stores vacancies, applications, feedback, learning signals, run logs and interaction records. The production API includes `/api/dashboard`, `/api/vacancies`, `/api/agent/run` and `/api/feedback`. The standalone demo exposes `/` and `/api/vacancies` and removes its database on shutdown.
