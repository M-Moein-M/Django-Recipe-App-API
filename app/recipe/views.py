from rest_framework import viewsets, mixins, authentication, permissions
from recipe.serializers import TagSerializer
from core.models import Tag


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = TagSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Tag.objects.all()

    def get_queryset(self):
        """Return tags for current authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
