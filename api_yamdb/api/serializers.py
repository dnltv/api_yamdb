from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=(
            UnicodeUsernameValidator(),
            UniqueValidator(queryset=User.objects.all())
        ),
        max_length=150,
        required=True
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserEditSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=(
            UnicodeUsernameValidator(),
            UniqueValidator(queryset=User.objects.all()),
        ),
        required=True,
    )
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('username', 'email', 'bio', 'role',
                  'first_name', 'last_name')
        model = User


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=(UnicodeUsernameValidator(),),
        required=True
    )
    email = serializers.EmailField(max_length=254, required=True)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Username "me" is not allowed.')
        return value

    def validate(self, data):
        user = User.objects.filter(username=data['username']).exists()
        email = User.objects.filter(email=data['email']).exists()
        if user:
            if not email:
                raise serializers.ValidationError(
                    'This username already exists'
                )
        if email:
            if not user:
                raise serializers.ValidationError(
                    'This email has already been used'
                )
        return data

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    slug = serializers.SlugField(
        max_length=30,
        validators=(UniqueValidator(queryset=Category.objects.all()),)
    )

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    slug = serializers.SlugField(
        max_length=30,
        validators=(UniqueValidator(queryset=Genre.objects.all()),)
    )

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        current_year = timezone.now().year
        if not -4000 <= value <= current_year:
            raise serializers.ValidationError(
                'Check the year of title release!'
            )
        return value


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, score):
        if not 1 <= score <= 10:
            raise serializers.ValidationError(
                'Acceptable evaluation are from 1 to 10!'
            )
        return score

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data

        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'You can leave a review to the title only once!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
