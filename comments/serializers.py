from rest_framework import serializers
from django.contrib.humanize.templatetags.humanize import naturaltime
from .models import Comment
from posts.models import BasePost


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    post = serializers.PrimaryKeyRelatedField(queryset=BasePost.objects.all())
    profile_id = serializers.ReadOnlyField(source='owner.trainerprofile.id')
    profile_avatar = serializers.ReadOnlyField(
        source='owner.trainerprofile.avatar.url'
        )
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Comment
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_avatar', 'created_at', 'updated_at',
            'post', 'content'
        ]


class CommentDetailSerializer(CommentSerializer):
    post = serializers.ReadOnlyField(source='post.id')
