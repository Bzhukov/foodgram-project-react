from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(
        error_messages={'unique': 'Пользователь с таким email уже существует'},
        blank=True,
        max_length=100,
        unique=True,
        verbose_name='email',
    )
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', ]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact="me"),
                name="username_is_not_me"
            )
        ]
