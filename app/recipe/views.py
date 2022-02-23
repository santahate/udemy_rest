from rest_framework.authentication import TokenAuthentication
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from core.models import Tag, Ingredient
from recipe.serializers import TagSerializer, IngredientSerializer


class BaseRecipeAttr(GenericViewSet, ListModelMixin, CreateModelMixin):
    """
    Base clas for Tags and Ingredients
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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


class TagViewSet(BaseRecipeAttr):
    """
    Manage Tags in db
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(BaseRecipeAttr):
    """
    Manage ingredients in db
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
