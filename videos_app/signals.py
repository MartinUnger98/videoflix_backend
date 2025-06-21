from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os
from .tasks import process_video_file
import django_rq

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    After a video is saved, this signal checks if it was newly created.
    If so, it enqueues a background task using Django RQ to process the video.
    """
    print("Video post save signal triggered")
    if created:
        print(f"New video created: {instance.title}")
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(process_video_file, instance.id)

@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    """
    Deletes the associated video file from disk when a Video model is deleted.
    Prevents orphaned media files.
    """
    if instance.video_file and os.path.isfile(instance.video_file.path):
        os.remove(instance.video_file.path)
