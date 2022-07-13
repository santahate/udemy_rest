from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from core.models import Tag, Ingredient, Recipe


class TagSerializer(ModelSerializer):
    """
    Serializer for Tag objects
    """
    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id', )


class IngredientSerializer(ModelSerializer):
    """
    Serializer for Ingredient objects
    """
    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id', )


class RecipeSerializer(ModelSerializer):
    """
    Serializer for Recipe
    """
    ingredients = PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tag = PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )


    class Meta:
        model = Recipe
        fields = ('id', 'title', 'ingredients', 'tag', 'time', 'price', 'link')
        read_only_fields = ('id', )
