import praw


def fetch_posts_from_subreddit(subreddit_name: str, keyword: str, limit: int = 20):
    """
    Busca posts do Reddit e retorna dados brutos normalizados.
    """

    reddit = praw.Reddit(
        client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_CLIENT_SECRET",
        user_agent="prospect_collector_v1",
    )

    subreddit = reddit.subreddit(subreddit_name)

    results = []

    for submission in subreddit.search(keyword, limit=limit):
        results.append({
            "author": str(submission.author) if submission.author else "unknown",
            "title": submission.title or "",
            "body": submission.selftext or "",
            "url": submission.url,
        })

    return results