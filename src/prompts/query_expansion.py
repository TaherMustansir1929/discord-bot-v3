QUERY_EXPANSION_PROMPT = """
    Generate 5 GitHub repository search queries related to:
    "{query}"

    Rules:
    - concise
    - technical
    - GitHub searchable
    - mix broad and specific
    - no numbering
    - one per line

    Example:
    For "machine learning", good queries would be:
    ['machine learning', 'deep learning', 'neural networks', 'tensorflow', 'pytorch']
    see how it is a mix of broad and specific, and all are concise and technical. Avoid queries like "best machine learning projects" or "machine learning for beginners" as they are not concise or technical enough.

    IMPORTANT NOTE: if the query is very specific, like the name of a GitHub user or exact name of a repository, then don't generate any queries, just return a list with single element of the original query, as the original query is already very specific and doesn't need expansion.
    """
