"""Domain models shared by search, scoring and persistence."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class CandidateProfile:
    target_roles: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    preferred_keywords: list[str] = field(default_factory=list)
    stop_keywords: list[str] = field(default_factory=list)
    min_monthly_salary: int | None = None
    learning_weights: dict[str, float] = field(default_factory=dict)


@dataclass(slots=True)
class Vacancy:
    external_id: str
    title: str
    company: str
    description: str
    url: str
    salary_from: int | None = None
    salary_to: int | None = None
    currency: str | None = None
    schedule: str | None = None
    employment: str | None = None
    skills: list[str] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ScoreResult:
    score: int
    decision: str
    reasons: list[str] = field(default_factory=list)
    penalties: list[str] = field(default_factory=list)
