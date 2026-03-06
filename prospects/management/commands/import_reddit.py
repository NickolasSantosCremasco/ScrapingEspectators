from django.core.management.base import BaseCommand
from prospects.services.reddit_collector import sync_reddit_prospects


class Command(BaseCommand):
    help = 'Busca novos leads no Reddit por subreddit e palavra-chave'

    def add_arguments(self, parser):
        parser.add_argument('--sub', type=str, help='Nome do subreddit', default='saas')
        parser.add_argument('--key', type=str, help='Palavra-chave', default='python')

    def handle(self, *args, **options):
        sub = options['sub']
        key = options['key']

        self.stdout.write(self.style.WARNING(f"Iniciando busca por '{key}' em r/{sub}..."))

        count = sync_reddit_prospects(sub, key, limit=15)

        self.stdout.write(self.style.SUCCESS(f"Finalizado! {count} novos prospects importados."))