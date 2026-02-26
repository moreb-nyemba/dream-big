from rest_framework import serializers
from .models import MemeTemplate, GeneratedMeme


class MemeTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemeTemplate
        fields = ['id', 'name', 'image', 'created_at']


class GeneratedMemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedMeme
        fields = ['id', 'template', 'top_text', 'bottom_text', 'image', 'created_at']
        read_only_fields = ['image', 'created_at']


class GenerateMemeRequestSerializer(serializers.Serializer):
    template_id = serializers.IntegerField(required=False)
    image_url = serializers.URLField(required=False)
    top_text = serializers.CharField(max_length=300, required=False, default='', allow_blank=True)
    bottom_text = serializers.CharField(max_length=300, required=False, default='', allow_blank=True)

    def validate(self, data):
        if not data.get('template_id') and not data.get('image_url'):
            raise serializers.ValidationError(
                'Provide either template_id or image_url.'
            )
        return data


class StickerRequestSerializer(serializers.Serializer):
    template_id = serializers.IntegerField(required=False)
    image_url = serializers.URLField(required=False)
    top_text = serializers.CharField(max_length=300, required=False, default='', allow_blank=True)
    bottom_text = serializers.CharField(max_length=300, required=False, default='', allow_blank=True)

    def validate(self, data):
        if not data.get('template_id') and not data.get('image_url'):
            raise serializers.ValidationError(
                'Provide either template_id or image_url.'
            )
        return data
