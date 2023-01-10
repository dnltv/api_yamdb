from rest_framework.serializers import (ModelSerializer,
                                        ValidationError, CurrentUserDefault,
                                        SlugRelatedField)

from api_yamdb.reviews.models import Review


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, score):
        if not 1 <= score <= 10:
            raise ValidationError(
                'Допустимые значения оценки - от 1 до 10!'
            )
        return score

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data

        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(author=author, title=title_id).exists():
            raise ValidationError(
                'Отзыв к произведению можно оставить только один раз!'
            )
        return data
