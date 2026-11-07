"""Read-only, offline demonstration of the scoring and CRM repository."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from app.repository import CRMRepository
from app.scoring import CandidateProfile, Vacancy, score_vacancy


def _seed_repository(repo: CRMRepository) -> None:
    profile = CandidateProfile(
        target_roles=["Python backend"],
        skills=["Python", "FastAPI", "PostgreSQL"],
        preferred_keywords=["удаленно"],
        stop_keywords=["холодные звонки"],
        min_monthly_salary=150_000,
    )
    vacancies = [
        Vacancy(
            external_id="demo-1",
            title="Python backend developer",
            company="Пример Лаб",
            description="Удаленно. Разработка API на Python и FastAPI, PostgreSQL.",
            url="",
            salary_from=180_000,
            salary_to=220_000,
            currency="RUR",
            skills=["Python", "FastAPI", "PostgreSQL"],
        ),
        Vacancy(
            external_id="demo-2",
            title="Backend developer",
            company="Пример Продукт",
            description="Внутренние сервисы на Python и FastAPI. Частично удаленно, Москва.",
            url="",
            salary_from=140_000,
            salary_to=170_000,
            currency="RUR",
            skills=["Python", "FastAPI"],
            raw={"area": {"name": "Москва"}},
        ),
        Vacancy(
            external_id="demo-3",
            title="Менеджер по продажам",
            company="Пример Сервис",
            description="Офис, холодные звонки и работа с клиентами.",
            url="",
            salary_from=70_000,
            salary_to=90_000,
            currency="RUR",
        ),
        Vacancy(
            external_id="demo-4",
            title="Backend developer",
            company="Пример Системы",
            description="Разработка внутренних сервисов на Python. Гибридный формат, Москва.",
            url="",
            salary_from=140_000,
            salary_to=170_000,
            currency="RUR",
            skills=["Python"],
            raw={"area": {"name": "Москва"}},
        ),
    ]
    for vacancy in vacancies:
        repo.upsert_vacancy(vacancy, score_vacancy(vacancy, profile))


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Never read the configured production path or reuse an existing database.
    with TemporaryDirectory(prefix="hh-crm-demo-") as directory:
        app.state.repository = CRMRepository(Path(directory) / "demo.sqlite3")
        _seed_repository(app.state.repository)
        yield


app = FastAPI(title="HeadHunter CRM — демо", lifespan=_lifespan, docs_url=None, redoc_url=None)


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return Path(__file__).with_name("demo.html").read_text(encoding="utf-8")


@app.get("/api/vacancies")
def vacancies(request: Request) -> list[dict]:
    return request.app.state.repository.list_vacancies(limit=50)
