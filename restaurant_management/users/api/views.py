from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from restaurant_management.users.models import User

from .serializers import UserCreateSerializer, UserRetrievingSerializer


class UserRetrievingViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = UserRetrievingSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserRetrievingSerializer(
            request.user,
            context={"request": request},
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
