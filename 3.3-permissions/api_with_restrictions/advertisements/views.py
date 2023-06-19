from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q

from .filters import AdvertisementFilter
from .models import Advertisement, AdvertisementStatusChoices, Favorite
from .permissions import IsOwnerOrAdminOrReadOnly
from .serializers import AdvertisementSerializer, FavoriteSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    def get_queryset(self):
        user_ = self.request.user
        queryset = Advertisement.objects.filter(Q(status=AdvertisementStatusChoices.OPEN)
                                                | Q(status=AdvertisementStatusChoices.CLOSED))

        if user_.is_authenticated:
            draft_query = Q(status=AdvertisementStatusChoices.DRAFT) & Q(creator=user_)
            queryset |= Advertisement.objects.filter(draft_query)

        return queryset

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrAdminOrReadOnly()]
        return []

    @action(detail=True, methods=["post"])
    def add_favorite(self, request, pk=None):
        advertisement = self.get_object()
        user = self.request.user
        if not user.is_authenticated:
            return Response({"error": "You must be logged in to add favorites."})
        favorite = Favorite.objects.create(author=user, advertisement=advertisement)
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def get_favorites(self, request, pk=None):
        user = self.request.user
        if not user.is_authenticated:
            return Response({"error": "You must be logged in to add favorites."})
        favorites = Favorite.objects.filter(author=user)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)