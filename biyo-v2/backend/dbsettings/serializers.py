
from rest_framework import serializers

from models import DBSettings
from terminalapi.serializers import PaginationWithDbSerializer


class DBSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DBSettings
        fields = ("name", "value", "terminal_id")


class PaginatedDBSettingSerializer(PaginationWithDbSerializer):
    class Meta:
        object_serializer_class = DBSettingSerializer
