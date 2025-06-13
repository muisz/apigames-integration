from rest_framework import serializers


class CheckAccountSerializer(serializers.Serializer):
    id = serializers.CharField()
    server_id = serializers.CharField()
