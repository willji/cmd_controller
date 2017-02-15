__author__ = 'jinhongjun'
from rest_framework import serializers
from salt_api.models import Minion, Master, Module, Log


class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master


class MinionSerializer(serializers.ModelSerializer):
    master = serializers.SlugRelatedField(queryset=Master.objects.all(), many=True, slug_field='ip')

    class Meta:
        model = Minion


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
