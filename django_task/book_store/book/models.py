from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Book(models.Model):
    title = models.CharField(max_length=64, verbose_name='Название')
    author = models.ForeignKey(
        User,
        related_name='books',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    count = models.PositiveSmallIntegerField(default=0, verbose_name='Остаток')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title
