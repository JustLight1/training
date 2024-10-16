from django.db import models


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
    ]

    task_name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='pending')
    worker_id = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_name
