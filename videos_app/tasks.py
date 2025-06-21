import os
import subprocess
from django.conf import settings
from videos_app.models import Video


def process_video_file(video_id):
    video = Video.objects.get(id=video_id)
    input_path = video.video_file.path
    filename_base = os.path.splitext(os.path.basename(input_path))[0]

    resolutions = {
        '120p': '160x120',
        '360p': '640x360',
        '720p': '1280x720',
        '1080p': '1920x1080'
    }

    for label, res in resolutions.items():
        output_dir = os.path.join(settings.MEDIA_ROOT, f'videos/{label}')
        os.makedirs(output_dir, exist_ok=True)

        output_file = os.path.join(output_dir, f'{filename_base}_{label}.mp4')

        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-vf', f'scale={res}',
            '-c:a', 'copy',
            output_file
        ]
        subprocess.run(cmd, check=True)
        setattr(video, f'file_{label}', f'videos/{label}/{filename_base}_{label}.mp4')

    # Thumbnail (bei Sekunde 3)
    thumbnail_dir = os.path.join(settings.MEDIA_ROOT, 'thumbnails')
    os.makedirs(thumbnail_dir, exist_ok=True)
    thumbnail_path = os.path.join(thumbnail_dir, f'{filename_base}.jpg')

    subprocess.run([
        'ffmpeg',
        '-i', input_path,
        '-ss', '00:00:03.000',
        '-vframes', '1',
        thumbnail_path
    ], check=True)

    video.thumbnail = f'thumbnails/{filename_base}.jpg'

    # HLS-Konvertierung
    hls_dir = os.path.join(settings.MEDIA_ROOT, 'videos/hls', filename_base)
    os.makedirs(hls_dir, exist_ok=True)

    hls_output = os.path.join(hls_dir, 'output.m3u8')

    hls_command = [
        'ffmpeg',
        '-i', input_path,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-strict', '-2',
        '-start_number', '0',
        '-hls_time', '10',
        '-hls_list_size', '0',
        '-f', 'hls',
        hls_output
    ]

    subprocess.run(hls_command, check=True)

    video.hls_playlist = f'videos/hls/{filename_base}/output.m3u8'
    video.save()
