from django.db import models
from django.contrib.auth import get_user_model
from main.models import Vacancy

User = get_user_model()


class Application(models.Model):
    """Отклик на вакансию"""

    class Status(models.TextChoices):
        PENDING = 'pending', '⏳ Ожидает'
        ACCEPTED = 'accepted', '✅ Принят'
        REJECTED = 'rejected', '❌ Отклонен'

    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        related_name='applications',  # ← Вот это нужно для vacancy.applications!
        verbose_name='Вакансия'
    )
    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='Соискатель'
    )
    cover_letter = models.TextField('Сопроводительное письмо', blank=True)
    status = models.CharField(
        'Статус',
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField('Дата отклика', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
        ordering = ['-created_at']
        unique_together = ['vacancy', 'applicant']  # Один отклик на вакансию

    def __str__(self):
        return f'{self.applicant.username} → {self.vacancy.title}'
