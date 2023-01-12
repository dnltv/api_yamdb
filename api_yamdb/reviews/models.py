from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    """
    Model representing a Category of Title.
    """
    name = models.CharField(
        'Category name',
        help_text='Enter the category name',
        max_length=256
    )
    slug = models.SlugField(
        'Slug',
        help_text='Enter the category slug',
        max_length=30,
        unique=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name} | {self.slug}'


class Genre(models.Model):
    """
    Model representing a genre of Title.
    """
    name = models.CharField(
        'Genre name',
        help_text='Enter the name of the genre',
        max_length=256
    )
    slug = models.SlugField(
        'Genre slug',
        help_text='Enter the genre slug',
        max_length=30,
        unique=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return f'{self.name} | {self.slug}'


class GenreTitle(models.Model):
    """
    Model representing ManyToMany relationship between Genre and Title.
    """
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey('Title', on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
        verbose_name = 'genre_title'
        verbose_name_plural = 'genres_titles'
        constraints = (
            models.UniqueConstraint(
                fields=('genre', 'title'),
                name='unique_genre_title'
            ),
        )

    def __str__(self):
        return f'{self.genre} | {self.title}'


class Title(models.Model):
    """
    Model representing a Title.
    """
    name = models.CharField(
        'Title name',
        help_text='Enter the name of the title',
        max_length=256,
    )
    year = models.IntegerField(
        'Release year of the title',
        help_text='Enter release year',
        db_index=True
    )
    description = models.TextField(
        'Title description',
        help_text='Enter title description'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        help_text='Enter the genre'
    )
    category = models.ForeignKey(
        Category,
        help_text='Select a category',
        related_name='titles',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Category'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    Model representing a Review on Title from auth users.
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Title',
    )
    text = models.TextField(verbose_name='Review')
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Author'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Score'
    )
    pub_date = models.DateTimeField(auto_now=True, verbose_name='Published')

    class Meta:
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review'
            )
        ]
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """
    Model representing a Comment on Review from auth users.
    """
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Review'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Author'
    )
    text = models.TextField(verbose_name='Comment')
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Published'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.text
