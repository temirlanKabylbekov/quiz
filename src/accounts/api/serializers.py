from django.contrib.auth.models import User
from rest_framework import serializers


class UserDetailSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'name',
        ]

    def get_name(self, obj):
        return ' '.join([obj.first_name, obj.last_name]).strip()
