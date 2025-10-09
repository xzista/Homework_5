from rest_framework.serializers import ValidationError


def validate_video_url(value):
    if "youtube.com" not in value:
        raise ValidationError("Ссылка на видео может быть только с youtube.com")
