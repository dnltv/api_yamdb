from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from ..reviews.models import Title
from .serializers import ReviewSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_query_set(self):
        title = get_object_or_404(
            Title, id=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
