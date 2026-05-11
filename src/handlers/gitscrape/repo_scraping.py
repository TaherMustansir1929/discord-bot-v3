import asyncio
import os

import httpx
from dotenv import load_dotenv

from src.utils import fetch_url_httpx

from .utils import Items, License, Main, Owner, Repository, calculate_repo_rank

load_dotenv()


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable is not set")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}

BASE_URL = "https://api.github.com/search/repositories"


# === Main scraping function ===
async def scrape_repositories(queries: list[str]) -> list[Repository]:

    params = [
        {
            "q": f"{query} archived:false",
        }
        for query in queries
    ]

    async with httpx.AsyncClient(headers=HEADERS, timeout=20) as client:
        tasks = [
            fetch_url_httpx(client, BASE_URL, params[i]) for i in range(len(queries))
        ]
        raw_results = await asyncio.gather(*tasks)

        raw_results = [
            Main(
                total_count=result["total_count"],
                incomplete_results=result["incomplete_results"],
                items=[
                    Items(
                        id=item["id"],
                        node_id=item["node_id"],
                        name=item["name"],
                        full_name=item["full_name"],
                        private=item["private"],
                        owner=Owner(**item["owner"]),
                        html_url=item["html_url"],
                        description=item.get("description"),
                        fork=item["fork"],
                        url=item["url"],
                        forks_url=item["forks_url"],
                        keys_url=item["keys_url"],
                        collaborators_url=item["collaborators_url"],
                        teams_url=item["teams_url"],
                        hooks_url=item["hooks_url"],
                        issue_events_url=item["issue_events_url"],
                        events_url=item["events_url"],
                        assignees_url=item["assignees_url"],
                        branches_url=item["branches_url"],
                        tags_url=item["tags_url"],
                        blobs_url=item["blobs_url"],
                        git_tags_url=item["git_tags_url"],
                        git_refs_url=item["git_refs_url"],
                        trees_url=item["trees_url"],
                        statuses_url=item["statuses_url"],
                        languages_url=item["languages_url"],
                        stargazers_url=item["stargazers_url"],
                        contributors_url=item["contributors_url"],
                        subscribers_url=item["subscribers_url"],
                        subscription_url=item["subscription_url"],
                        commits_url=item["commits_url"],
                        git_commits_url=item["git_commits_url"],
                        comments_url=item["comments_url"],
                        issue_comment_url=item["issue_comment_url"],
                        contents_url=item["contents_url"],
                        compare_url=item["compare_url"],
                        merges_url=item["merges_url"],
                        archive_url=item["archive_url"],
                        downloads_url=item["downloads_url"],
                        issues_url=item["issues_url"],
                        pulls_url=item["pulls_url"],
                        milestones_url=item["milestones_url"],
                        notifications_url=item["notifications_url"],
                        labels_url=item["labels_url"],
                        releases_url=item["releases_url"],
                        deployments_url=item["deployments_url"],
                        created_at=item["created_at"],
                        updated_at=item["updated_at"],
                        pushed_at=item["pushed_at"],
                        git_url=item["git_url"],
                        ssh_url=item["ssh_url"],
                        clone_url=item["clone_url"],
                        svn_url=item["svn_url"],
                        homepage=item.get("homepage"),
                        size=item["size"],
                        stargazers_count=item["stargazers_count"],
                        watchers_count=item["watchers_count"],
                        language=item.get("language"),
                        has_issues=item["has_issues"],
                        has_projects=item["has_projects"],
                        has_wiki=item["has_wiki"],
                        has_pages=item["has_pages"],
                        has_discussions=item["has_discussions"],
                        forks_count=item["forks_count"],
                        mirror_url=item.get("mirror_url"),
                        archived=item["archived"],
                        disabled=item["disabled"],
                        open_issues_count=item["open_issues_count"],
                        license=License(**item["license"])
                        if item.get("license")
                        else None,
                        allow_forking=item["allow_forking"],
                        is_template=item["is_template"],
                        web_commit_signoff_required=item["web_commit_signoff_required"],
                        has_pull_requests=item["has_pull_requests"],
                        pull_request_creation_policy=item[
                            "pull_request_creation_policy"
                        ],
                        topics=item["topics"],
                        visibility=item["visibility"],
                        forks=item["forks"],
                        open_issues=item["open_issues"],
                        watchers=item["watchers"],
                        default_branch=item["default_branch"],
                        score=item["score"],
                    )
                    for item in result["items"]
                ],
            )
            for result in raw_results
        ]

        repositories = [
            Repository(
                id=repo.id,
                name=repo.name,
                owner=repo.owner.login,
                owner_avatar=repo.owner.avatar_url,
                stars=repo.stargazers_count,
                forks=repo.forks_count,
                watchers=repo.watchers_count,
                description=repo.description or "No description available",
                language=repo.language or "Unknown",
                topics=repo.topics,
                updated_at=repo.updated_at,
                url=repo.html_url,
                license=repo.license.name if repo.license else "No license",
                has_issues=repo.has_issues,
            )
            for result in raw_results
            for repo in result.items
        ]

        repositories.sort(key=calculate_repo_rank, reverse=True)

        if len(repositories) > 50:
            return repositories[:50]
        else:
            return repositories
