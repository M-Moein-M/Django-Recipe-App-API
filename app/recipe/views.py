from rest_framework import viewsets, mixins, authentication, permissions
from recipe.serializers import TagSerializer, IngredientSerializer
from core.models import Tag, Ingredient


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manage tags objects"""
    serializer_class = TagSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Tag.objects.all()

    def get_queryset(self):
        """Return tags for current authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create new tag"""
        serializer.save(user=self.request.user)


class IngredientViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin):
    """Manage ingredient objects"""
    serializer_class = IngredientSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Ingredient.objects.all()

    def get_queryset(self):
        """Return ingredients for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
