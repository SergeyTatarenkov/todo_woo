from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Заголовок:', max_length=100)
    memo = models.TextField('Описание:', max_length=1000, blank=True)
    created_at = models.DateTimeField('Заматка создана', auto_now_add=True)
    datecomplited = models.DateTimeField('Срок исполнения:', null=True, blank=True)
    important = models.BooleanField('ВАЖНОЕ', default=False)

    def __str__(self):
        return self.title