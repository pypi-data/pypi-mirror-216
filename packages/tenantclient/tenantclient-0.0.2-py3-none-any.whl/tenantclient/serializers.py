from rest_framework import serializers
from .models import TenantInfo


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantInfo
        fields = '__all__'


class TenantSettingsSerializer(serializers.ModelSerializer):
    settings = serializers.DictField()
    # tenant_id = serializers.CharField(read_only=True)

    class Meta:
        model = TenantInfo
        fields = ('settings',)
    
    def update(self, instance, validated_data):
        settings: dict = instance.settings
        settings.update(validated_data)
        validated_data = settings
        return super(TenantSettingsSerializer, self).update(instance=instance, validated_data=validated_data)
