from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


User = get_user_model()


class Review(models.Model):
    """
    Model representing a Review on Title from auth users.
    """
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Отзыв')
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(auto_now=True, verbose_name='Опубликовано')

    class Meta:
        ordering = ('id',)
        constraint = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique review'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text
