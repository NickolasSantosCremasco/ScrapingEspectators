from collections import defaultdict

from django.core.management.base import BaseCommand
from prospects.services.reddit_collector import sync_reddit_prospects

class Command(BaseCommand):
    help = 'Busca leads no Reddit por subreddit e palavra-chave'

    def add_arguments(self, parser):
        parser.add_argument('--sub', type=str, help='Nome do subreddit', default='saas')
        parser.add_argument('--key', type=str, help='Palavra-Chave', default='python')
        parser.add_argument('--limit', type=int, help='Limite de posts', default='10')
    def handle(self, *args, **options):
        sub = options['sub']
        key = options['key']
        limit = options['limit']

        self.stdout.write(self.style.WARNING(f'Iniciando busca em r/{sub} por "{key}"...'))

        total_criado = sync_reddit_prospects(sub, key, limit=limit)

        if total_criado > 0:
            self.stdout.write(self.style.SUCESS(f'Sucesso! {total_criado} novos leads importados.'))
        else:
            self.stdout.write(self.style.NOTICE('Nenhum lead novo encontrado (Possivelmente já existem no banco).'))