from src.agents import query_expansion_agent, reranker_agent
from src.repo_scraping import scrape_repositories
from src.utils import Repository


async def repo_controller(query: str, token: str) -> list[Repository]:

    # Expand user query to 5
    queries = await query_expansion_agent(query)
    print(f"Expanded queries: {queries}")

    # Scrape GitHub repositories + calculate relevance scores
    repositories = await scrape_repositories(queries=queries, token=token)
    print(f"Total repositories found: {len(repositories)}")

    if len(repositories) == 0:
        raise ValueError("No repositories found for query")

    if len(repositories) <= 10:
        top_reranked_repositories = repositories
    else:
        # rerank top repositories using Cohere Reranker
        top_reranked_repositories = await reranker_agent(
            query=query, repositories=repositories
        )

    return top_reranked_repositories
