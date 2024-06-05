from rest_framework import serializers

from .models import Snippet, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'tag_title']
        
        extra_kwargs = {
        'tag_title': {'validators': []}
    }

        extra_kwargs = {
            'tag_title': {'validators': []}
        }


class SnippetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %I:%M %p', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %I:%M %p', read_only=True)

    class Meta:
        model = Snippet
        fields = ['id', 'title', 'note', 'created_at', 'updated_at', 'created_by', 'tags']
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        snippet = Snippet.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(tag_title=tag_data['tag_title'])
            snippet.tags.add(tag)
        return snippet

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')
        instance.title = validated_data.get('title', instance.title)
        instance.note = validated_data.get('note', instance.note)
        instance.save()

        # Clear existing tags
        instance.tags.clear()

        # Add new tags
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(tag_title=tag_data['tag_title'])
            instance.tags.add(tag)

        return instance
