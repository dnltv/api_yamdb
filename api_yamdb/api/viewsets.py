from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               GenericViewSet):
    """
    A viewset that provides `create`, `list` and `destroy` actions.
    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
