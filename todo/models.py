from django.db import models


class Task(models.Model):
    STATUS_CHOICE = (
        ('todo', 'TODO'),
        ('done', 'DONE'),
    )
    description = models.CharField(max_length=225)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE)

    def __str__(self):return self.description
