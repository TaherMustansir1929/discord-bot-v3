import math
from datetime import datetime, timezone

from .Repository import Repository


def days_since(date_string: str) -> int:
    dt = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    return (now - dt).days


def calculate_repo_rank(repo: Repository) -> float:
    """
    repo -> Items dataclass
    """

    stars = repo.stars
    forks = repo.forks
    watchers = repo.watchers

    # -------------------------
    # Popularity
    # -------------------------
    popularity = 0.7 * math.log1p(stars) + 0.3 * math.log1p(watchers)

    # -------------------------
    # Engagement
    # -------------------------
    engagement = math.log1p(forks) * (1 + (forks / (stars + 1)))

    # -------------------------
    # Activity
    # -------------------------
    inactive_days = days_since(repo.updated_at)

    activity = math.exp(-inactive_days / 365)

    # -------------------------
    # Health
    # -------------------------
    has_license = 1 if repo.license else 0
    has_description = 1 if repo.description else 0
    issues_enabled = 1 if repo.has_issues else 0
    topics_score = min(len(repo.topics) / 10, 1)

    health = (
        0.4 * has_license
        + 0.2 * has_description
        + 0.2 * issues_enabled
        + 0.2 * topics_score
    )

    # -------------------------
    # Final Score
    # -------------------------
    final_score = (
        0.35 * popularity + 0.25 * engagement + 0.25 * activity + 0.15 * health
    )

    return round(final_score * 100, 2)
