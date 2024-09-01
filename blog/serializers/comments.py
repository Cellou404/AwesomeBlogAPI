from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "body", "date_created"]
        read_only_fields = ["id", "date_created"]

    def create(self, validated_data):
        post = self.context["post"]
        user = self.context["user"]
        comment = Comment.objects.create(user=user, post=post, **validated_data)

        return comment
