from rest_framework import serializers

from ...character.models.powers import Power


class PowerSerializer(serializers.ModelSerializer):


    class Meta:
        model = Power
        fields = '__all__'


