from rest_framework import serializers
from videos_app.models import Video, VideoProgress
from genres_app.models import Genre


class VideoSerializer(serializers.ModelSerializer):
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), write_only=True)
    genre_name = serializers.StringRelatedField(source='genre', read_only=True)
    video_file = serializers.FileField()
    thumbnail = serializers.FileField(read_only=True)

    file_120p = serializers.FileField(read_only=True)
    file_360p = serializers.FileField(read_only=True)
    file_720p = serializers.FileField(read_only=True)
    file_1080p = serializers.FileField(read_only=True)
    hls_playlist = serializers.CharField(read_only=True)
    class Meta:
        model = Video
        fields = [
            'id',
            'title',
            'description',
            'video_file',
            'thumbnail',
            'file_120p',
            'file_360p',
            'file_720p',
            'file_1080p',
            'hls_playlist',
            'genre',       
            'genre_name', 
            'created_at'
        ]


class VideoProgressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = VideoProgress
        fields = [
            'id',
            'user',
            'video',
            'timestamp',
            'updated_at'
        ]
        read_only_fields = ['updated_at']
