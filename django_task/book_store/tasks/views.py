from django.db import transaction
from django.utils import timezone

from tasks.models import Task


def fetch_task(worker_id):
    with transaction.atomic():
        stale_time = timezone.now() - timezone.timedelta(minutes=5)
        stale_task = Task.objects.select_for_update(skip_locked=True).filter(
            status='processing',
            updated_at__lt=stale_time
        ).order_by('created_at').first()

        if stale_task:
            stale_task.status = 'pending'
            stale_task.worker_id = None
            stale_task.save()

        task = Task.objects.select_for_update(skip_locked=True).filter(
            status='pending'
        ).order_by('created_at').first()

        if task:
            task.status = 'processing'
            task.worker_id = worker_id
            task.save()

    return task


def complete_task(task_id):
    with transaction.atomic():
        task = Task.objects.select_for_update().get(id=task_id)
        task.status = 'completed'
        task.save()
