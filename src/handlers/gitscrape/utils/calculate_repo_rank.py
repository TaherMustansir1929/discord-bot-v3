import math
from datetime import datetime, timezone

from .Repository import Repository


def calculate_repo_rank(
    repo: Repository,
) -> float:
    """
    Generate a weighted GitHub repository quality score (0-100).

    Weight distribution:
    - Popularity  -> 40%
    - Activity    -> 40%
    - Engagement  -> 15%
    - Health      -> 5%
    """

    stars = repo.stars
    watchers = repo.watchers
    forks = repo.forks
    updated_at = repo.updated_at
    has_license = repo.license is not None
    has_description = repo.description is not None
    has_issues = repo.has_issues

    # -----------------------------
    # 1. Popularity (40%)
    # watchers + stars
    # logarithmic scaling prevents giant repos from dominating
    # -----------------------------
    popularity_raw = stars + watchers
    popularity_score = min(
        math.log1p(popularity_raw) / math.log1p(100_000),
        1.0,
    )

    # -----------------------------
    # 2. Engagement (15%)
    # forks
    # -----------------------------
    engagement_score = min(
        math.log1p(forks) / math.log1p(50_000),
        1.0,
    )

    # -----------------------------
    # 3. Activity (40%)
    # recently updated
    # decay based on days since last update
    # -----------------------------
    updated_dt = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)

    days_since_update = (now - updated_dt).days

    if days_since_update <= 7:
        activity_score = 1.0
    elif days_since_update <= 30:
        activity_score = 0.85
    elif days_since_update <= 90:
        activity_score = 0.65
    elif days_since_update <= 180:
        activity_score = 0.4
    elif days_since_update <= 365:
        activity_score = 0.2
    else:
        activity_score = 0.05

    # -----------------------------
    # 4. Health (5%)
    # repo hygiene signals
    # -----------------------------
    health_checks = [
        has_license,
        has_description,
        has_issues,
    ]

    health_score = sum(health_checks) / len(health_checks)

    # -----------------------------
    # Final weighted score
    # -----------------------------
    final_score = (
        popularity_score * 0.40
        + activity_score * 0.40
        + engagement_score * 0.15
        + health_score * 0.05
    )

    return round(final_score * 100, 2)
