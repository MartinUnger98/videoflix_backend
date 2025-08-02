from pathlib import Path
from videos_app.models import Video
from django.conf import settings
from .utils import (
    get_output_dir, create_hls_rendition,
    generate_master_playlist, extract_thumbnail
)


def process_video_file(video_id):
    """
    Orchestrates the full video processing workflow:
    - Generate multiple HLS renditions (360p–1080p)
    - Create a master playlist
    - Extract a thumbnail
    - Save the paths to the Video model
    """
    video = Video.objects.get(id=video_id)
    input_path = Path(video.video_file.path)
    output_dir = get_output_dir(input_path)

    renditions = {
        "360p": {"resolution": "640x360", "bitrate": "800k"},
        "480p": {"resolution": "854x480", "bitrate": "1400k"},
        "720p": {"resolution": "1280x720", "bitrate": "2500k"},
        "1080p": {"resolution": "1920x1080", "bitrate": "5000k"},
    }

    variant_playlists = [
        create_hls_rendition(input_path, output_dir, label, config["resolution"], config["bitrate"])
        for label, config in renditions.items()
    ]

    master_playlist = generate_master_playlist(output_dir, variant_playlists)
    video.hls_playlist = str(master_playlist.relative_to(settings.MEDIA_ROOT))

    thumbnail = extract_thumbnail(input_path, input_path.stem)
    video.thumbnail = str(thumbnail.relative_to(settings.MEDIA_ROOT))

    video.save()
