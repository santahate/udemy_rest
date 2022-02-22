from rest_framework.authentication import TokenAuthentication
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from core.models import Tag
from recipe.serializers import TagSerializer


class TagViewSet(GenericViewSet, ListModelMixin):
    """
    Manage Tags in db
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_queryset(self):
        """
        Return objects for current user only
        """
        return self.queryset.filter(user=self.request.user).order_by('-name')