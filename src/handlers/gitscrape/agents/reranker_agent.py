import cohere
import yaml

from src.handlers.gitscrape.repo_scraping import Repository

COHERE_RERANKER_MODEL_NAME = "rerank-v4.0-pro"
co = cohere.ClientV2()


async def reranker_agent(
    query: str, repositories: list[Repository], top_n: int = 5
) -> list[Repository]:
    # Convert Repository objects to dictionaries for Co:here
    docs = [
        {
            "Title": repo.name,
            "Description": repo.description,
            "Owner": repo.owner,
            "Language": repo.language,
            "Topics": ", ".join(repo.topics),
        }
        for repo in repositories
    ]

    yaml_docs = [yaml.dump(doc, sort_keys=False) for doc in docs]
    results = co.rerank(
        model=COHERE_RERANKER_MODEL_NAME,
        query=query,
        documents=yaml_docs,
        top_n=top_n,
    )

    rankings = results.results
    rankings.sort(key=lambda x: x.relevance_score, reverse=True)
    top_repositories = [repositories[rank.index] for rank in rankings[:top_n]]
    return top_repositories
