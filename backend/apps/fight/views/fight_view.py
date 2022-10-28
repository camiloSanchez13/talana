from _testcapi import raise_exception

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models.fight import Fight
from ..serializers.fight_serializer import FightSerializer, HistorySerializer


class FigthViewSet(viewsets.GenericViewSet):


    #TODO retornar los relatos de los movimientos ej pego una patada, tiro un haduken
    def create(self, request):

        serializer = FightSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(HistorySerializer(instance.history.all(), many=True).data, status=status.HTTP_200_OK)

