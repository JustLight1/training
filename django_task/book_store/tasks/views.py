from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from tasks.models import Task


def fetch_task(worker_id):
    with transaction.atomic():
        stale_time = timezone.now() - timezone.timedelta(minutes=5)
        task = Task.objects.select_for_update(skip_locked=True).filter(
            Q(status='processing',
              updated_at__lt=stale_time) | Q(status='pending')
        ).order_by('created_at').first()

        if task:
            if task.status == 'processing':
                task.status = 'pending'
                task.worker_id = None
            else:
                task.worker_id = 'processing'
                task.worker_id = worker_id
            task.save()

    return task


def complete_task(task_id):
    with transaction.atomic():
        task = Task.objects.select_for_update().get(id=task_id)
        if task.status == 'processing':
            task.status = 'completed'
            task.save()
