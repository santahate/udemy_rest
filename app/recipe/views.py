from rest_framework.authentication import TokenAuthentication
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from core.models import Tag, Ingredient, Recipe
from recipe.serializers import TagSerializer, IngredientSerializer, RecipeSerializer


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


class RecipeViewSet(ModelViewSet):
    """
    Manage Recipes in db
    """
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """
        Retrieve Recipes for authenticated user
        """
        return self.queryset.filter(user=self.request.user)

