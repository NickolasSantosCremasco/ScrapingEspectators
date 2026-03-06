import logging
from django.db import transaction
from prospects.models import Prospect
from prospects.collectors.reddit import fetch_posts_from_subreddit

logger = logging.getLogger(__name__)


def sync_reddit_prospects(subreddit_name: str, keyword: str, limit: int = 20):
    """
    Orquestra a coleta do Reddit e a persistência no Django.
    """
    # 1. Coleta os dados brutos usando sua função existente
    raw_posts = fetch_posts_from_subreddit(subreddit_name, keyword, limit)

    prospects_created = 0

    # Usamos uma transação para garantir integridade, embora para SQLite o ganho seja menor
    with transaction.atomic():
        for post in raw_posts:
            try:
                # 2. Deduplicação por URL (evita duplicar o mesmo post/perfil)
                prospect, created = Prospect.objects.get_or_create(
                    profile_url=post['url'],
                    defaults={
                        'name': post['author'],
                        'headline': post['title'],
                        'bio': post['body'][:1000],  # Proteção contra textos gigantes
                        'platform': 'reddit',
                        'keyword': keyword,
                    }
                )

                # 3. Dispara o Scoring (seu método que já funciona no shell)
                # Como o scoring depende de headline/bio, garantimos que ele rode aqui
                prospect.update_relevance_score()
                prospect.save()

                if created:
                    prospects_created += 1

            except Exception as e:
                logger.error(f"Erro ao processar post {post['url']}: {e}")
                continue

    return prospects_created