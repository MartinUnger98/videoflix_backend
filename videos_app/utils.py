import subprocess
from pathlib import Path
from django.conf import settings


def get_output_dir(input_path: Path) -> Path:
    """
    Creates and returns the output directory for HLS renditions
    based on the original video's filename.
    """
    filename_base = input_path.stem
    output_dir = Path(settings.MEDIA_ROOT) / 'videos' / 'hls' / filename_base
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def create_hls_rendition(input_path, output_dir, label, resolution, bitrate):
    """
    Creates a single HLS video stream (e.g., 360p, 720p) from the input video,
    using the specified resolution and bitrate. Returns metadata for the master playlist.
    """
    stream_path = output_dir / f"{label}.m3u8"
    segment_path = output_dir / f"{label}_%03d.ts"

    cmd = [
        "ffmpeg", "-i", str(input_path),
        "-vf", f"scale={resolution}",
        "-c:v", "libx264", "-b:v", bitrate,
        "-c:a", "aac", "-ac", "2", "-ar", "48000",
        "-f", "hls", "-hls_time", "10", "-hls_playlist_type", "vod",
        "-hls_segment_filename", str(segment_path),
        str(stream_path), "-y"
    ]
    subprocess.run(cmd, check=True)

    return {
        "resolution": resolution,
        "bandwidth": int(bitrate.replace("k", "")) * 1000,
        "playlist": f"{label}.m3u8"
    }


def generate_master_playlist(output_dir: Path, variants: list):
    """
    Creates a master.m3u8 playlist file that references all HLS renditions
    with their respective bandwidths and resolutions.
    """
    master_path = output_dir / "master.m3u8"
    with open(master_path, "w") as f:
        f.write("#EXTM3U\n")
        for variant in variants:
            f.write(f"#EXT-X-STREAM-INF:BANDWIDTH={variant['bandwidth']},RESOLUTION={variant['resolution']}\n")
            f.write(f"{variant['playlist']}\n")
    return master_path


def extract_thumbnail(input_path: Path, filename_base: str) -> Path:
    """
    Extracts a thumbnail image from the 3-second mark of the input video
    and stores it in the thumbnails directory.
    """
    thumbnail_dir = Path(settings.MEDIA_ROOT) / "thumbnails"
    thumbnail_dir.mkdir(parents=True, exist_ok=True)
    thumbnail_path = thumbnail_dir / f"{filename_base}.jpg"

    subprocess.run([
        "ffmpeg", "-i", str(input_path),
        "-ss", "00:00:03.000", "-vframes", "1",
        str(thumbnail_path), "-y"
    ], check=True)

    return thumbnail_path
