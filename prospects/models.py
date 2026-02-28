from django.db import models
from .services.scoring import calculate_relevance_score

class Prospect(models.Model):
    PLATFORM_CHOICES = [
        ('linkedin', 'LinkedIn'),
        ('reddit', 'Reddit'),
        ('twitter', 'Twitter'),
        ('youtube', 'YouTube'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    headline = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)

    platform = models.CharField(
        max_length=50,
        choices=PLATFORM_CHOICES
    )

    profile_url = models.URLField(unique=True)

    location = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=255, blank=True)

    keyword = models.TextField(blank=True, help_text='Palavras-chave extraídas do perfil')

    relevance_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.platform})"


    def update_relevance_score(self):
        text = " ".join(
            value
            for value in (self.headline, self.bio, self.keyword)
            if value
        )

        score = calculate_relevance_score(text)

        # Blindagem absoluta
        if score is None or not isinstance(score, (int, float)):
            score = 0.0

        self.relevance_score = float(score)
        self.save(update_fields=["relevance_score"])