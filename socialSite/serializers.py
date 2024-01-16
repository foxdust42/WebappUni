from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(source='user.username', read_only=True)
    # id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        return Post(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
