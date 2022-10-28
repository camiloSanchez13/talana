from rest_framework import viewsets, status
from rest_framework.response import Response

from ..serializers.fight_serializer import FightSerializer, HistorySerializer


class FigthViewSet(viewsets.GenericViewSet):

    """
    Se Crea la batalla y ademas crea el historial, que es donde se ubican los relatos para
    devolverlos en la respuesta del servicio

    """
    def create(self, request):
        serializer = FightSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(HistorySerializer(instance.history.all(), many=True).data, status=status.HTTP_200_OK)

