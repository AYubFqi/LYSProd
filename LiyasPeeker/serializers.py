from .models import Param_Societe
from rest_framework import serializers


class paramSocieteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Param_Societe
        fields = "__all__"

    def create(self, validated_data):
        param = Param_Societe(**validated_data)
        param.save()
        return param

    def update(self, instance, validated_data):
        instance.Raison_social = validated_data.get('Raison_social', instance.Raison_social)
        instance.Activ = validated_data.get('Activ', instance.Activ)
        instance.ICE = validated_data.get('ICE', instance.ICE)
        instance.IFS = validated_data.get('IFS', instance.IFS)
        instance.Centre_RC = validated_data.get('Centre_RC', instance.Centre_RC)
        instance.Num_RC = validated_data.get('Num_RC', instance.Num_RC)
        instance.ADS = validated_data.get('ADS', instance.ADS)
        instance.save()
        return instance

    def delete(self, pk):
        param = Param_Societe.objects.get(id=pk)
        param.delete()
        return True
