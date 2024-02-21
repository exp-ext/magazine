from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()
    user = UserSerializer()
    average_rating = serializers.FloatField()
    children = serializers.ListField(child=RecursiveField(), required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        comment = representation.pop('comment', None)
        if comment:
            user_representation = comment.pop('user', {})
            representation['user'] = UserSerializer(user_representation).data
            for key, value in comment.items():
                representation[key] = value
        return representation
