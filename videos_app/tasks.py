import subprocess
from pathlib import Path
from django.conf import settings
from videos_app.models import Video


def process_video_file(video_id):
    video = Video.objects.get(id=video_id)
    input_path = Path(video.video_file.path)
    filename_base = input_path.stem
    output_dir = Path(settings.MEDIA_ROOT) / 'videos' / 'hls' / filename_base
    output_dir.mkdir(parents=True, exist_ok=True)

    # Auflösungen und Bitraten definieren
    renditions = {
        '360p':  {'resolution': '640x360',   'bitrate': '800k'},
        '480p':  {'resolution': '854x480',   'bitrate': '1400k'},
        '720p':  {'resolution': '1280x720',  'bitrate': '2500k'},
        '1080p': {'resolution': '1920x1080', 'bitrate': '5000k'},
    }


    variant_playlists = []

    for label, config in renditions.items():
        stream_path = output_dir / f"{label}.m3u8"
        segment_path = output_dir / f"{label}_%03d.ts"

        cmd = [
            'ffmpeg',
            '-i', str(input_path),
            '-vf', f"scale={config['resolution']}",
            '-c:v', 'libx264',
            '-b:v', config['bitrate'],
            '-c:a', 'aac',
            '-ac', '2',
            '-ar', '48000',
            '-f', 'hls',
            '-hls_time', '10',
            '-hls_playlist_type', 'vod',
            '-hls_segment_filename', str(segment_path),
            str(stream_path),
            '-y'
        ]

        print(f"🎞️ Generiere HLS: {label}")
        subprocess.run(cmd, check=True)

        variant_playlists.append({
            'resolution': config['resolution'],
            'bandwidth': int(config['bitrate'].replace('k', '')) * 1000,
            'playlist': f"{label}.m3u8"
        })

    # Master playlist
    master_path = output_dir / 'master.m3u8'
    with open(master_path, 'w') as f:
        f.write("#EXTM3U\n")
        for variant in variant_playlists:
            f.write(f"#EXT-X-STREAM-INF:BANDWIDTH={variant['bandwidth']},RESOLUTION={variant['resolution']}\n")
            f.write(f"{variant['playlist']}\n")

    # Setze master.m3u8 im Modell
    video.hls_playlist = str(master_path.relative_to(settings.MEDIA_ROOT))

    # Generiere Thumbnail bei Sekunde 3
    thumbnail_dir = Path(settings.MEDIA_ROOT) / 'thumbnails'
    thumbnail_dir.mkdir(parents=True, exist_ok=True)
    thumbnail_path = thumbnail_dir / f"{filename_base}.jpg"

    try:
        subprocess.run([
            'ffmpeg',
            '-i', str(input_path),
            '-ss', '00:00:03.000',
            '-vframes', '1',
            str(thumbnail_path),
            '-y'
        ], check=True)
        video.thumbnail = str(thumbnail_path.relative_to(settings.MEDIA_ROOT))
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Fehler beim Generieren des Thumbnails: {e}")

    video.save()
    print(f"✅ Videoverarbeitung abgeschlossen: {video.title}")
