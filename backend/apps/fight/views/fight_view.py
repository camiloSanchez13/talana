from _testcapi import raise_exception

from rest_framework import viewsets, status
from rest_framework.response import Response

from ..serializers.fight_serializer import FightSerializer


class FigthViewSet(viewsets.GenericViewSet):


    def create(self, request):

        serializer = FightSerializer(data=request.data)#Donde pedire los personajes y sus golpes
        serializer.is_valid(raise_exception=True)

        resp = serializer.save()

        return Response(self.get_serializer(resp).data, status=status.HTTP_200_OK)
