from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os
from .tasks import process_video_file
import django_rq

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print("Video post save signal triggered")
    if created:
        print(f"New video created: {instance.title}")
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(process_video_file, instance.id)

@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file and os.path.isfile(instance.video_file.path):
        os.remove(instance.video_file.path)
