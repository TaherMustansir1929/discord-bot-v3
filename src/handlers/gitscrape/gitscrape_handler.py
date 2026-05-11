from discord import Interaction

from .agents import query_expansion_agent, reranker_agent
from .repo_scraping import scrape_repositories
from .utils import create_repo_embed


async def gitscrape_handler(interaction: Interaction, query: str):
    await interaction.response.defer()

    # Expand user query to 5
    queries = await query_expansion_agent(query)
    print(f"Expanded queries: {queries}")

    # Scrape GitHub repositories + calculate relevance scores
    repositories = await scrape_repositories(queries=queries)
    print(f"Total repositories found: {len(repositories)}")

    if len(repositories) == 0:
        await interaction.followup.send(
            content=f"No repositories found for query: `{query}`"
        )
        return

    if len(repositories) <= 10:
        top_reranked_repositories = repositories
    else:
        # rerank top repositories using Cohere Reranker
        top_reranked_repositories = await reranker_agent(
            query=query, repositories=repositories
        )

    embeds = []
    for index, repo in enumerate(top_reranked_repositories, start=1):
        embeds.append(create_repo_embed(repo, index))

    await interaction.followup.send(
        content=f"**GitScrape Results for:** `{query}`", embeds=embeds
    )
