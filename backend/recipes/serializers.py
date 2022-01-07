from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import (CustomUser, Ingredient, Recipe, Tag, Follow, IngredientInRecipe, Favorite, PurchaseList)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = '__all__'


class FavouriteRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class PurchaseListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class IngredientInRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = IngredientInRecipe
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    is_follower = serializers.SerializerMethodField('check_if_is_follower')

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_follower')

    def check_if_is_follower(self, user):
        current_user = self.context['request'].user
        other_user = user.following.all()
        if other_user == 0:
            return False
        return Follow.objects.filter(user=user, author=current_user).exists()


class RecipeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None,
        required=True,
        allow_empty_file=False,
        use_url=True,
    )
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'


class ListRecipeSerializers(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None:
            return False
        user = request.user
        return Favorite.objects.filter(recipe=obj, user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None:
            return False
        user = request.user
        return PurchaseList.objects.filter(recipe=obj, user=user).exists()


class AddIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class LookRecipeSerializers(serializers.ModelSerializer):



class CreateRecipeSerializers(serializers.ModelSerializer):
    ingredients = AddIngredientSerializer
    image = Base64ImageField()
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time')

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        author = self.context.get('request').user
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=author, **validated_data)
        recipe.save()
        recipe.tags.set(tags_data)
        for ingredient in ingredients_data:
            ingredient_model = ingredient['id']
            amount = ingredient['amount']
            IngredientInRecipe.objects.create(
                ingredient=ingredient_model,
                recipe=recipe,
                amount=amount
            )
        return recipe

    def update(self, instance, validated_data):
        ingredient_data = validated_data.pop('ingredients')
        IngredientInRecipe.objects.filter(recipe=instance).delete()
        for new_ingredient in ingredient_data:
            IngredientInRecipe.objects.create(
                ingredient=new_ingredient['id'],
                recipe=instance,
                amount=new_ingredient['amount']
            )
        instance.name = validated_data.pop('name')
        instance.text = validated_data.pop('text')
        instance.image = validated_data.pop('image')
        instance.cooking_time = validated_data.pop('cooking_time')
        instance.save()
        return instance

    def to_representation(self, instance):
        return ShowRecipeSerializer(instance, context={'request': self.context.get('request')}).data


