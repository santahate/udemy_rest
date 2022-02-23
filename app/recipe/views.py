from rest_framework.authentication import TokenAuthentication
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from core.models import Tag, Ingredient
from recipe.serializers import TagSerializer, IngredientSerializer


class TagViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
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

    def perform_create(self, serializer):
        """
        Create new Tag
        """
        serializer.save(user=self.request.user)


class IngredientViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    """
    Manage ingredients in db
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        """
        Return objects for current user only
        """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """
        Create new ingredient
        """
        serializer.save(user=self.request.user)