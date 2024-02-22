from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()


class CommentTreeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()
    average_rating = serializers.FloatField()
    user = UserSerializer()

    def get_fields(self):
        fields = super(CommentTreeSerializer, self).get_fields()
        fields['children'] = CommentTreeSerializer(many=True, required=False)
        return fields
