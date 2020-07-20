from django.db import models
from django.urls import reverse
import uuid

# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=200,
                            help_text='Enter a book genre')

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language"
                                      " (English, French, Japanese etc.)")

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True,
                                     blank=True)
    date_of_death = models.DateField('Died',
                                     null=True,
                                     blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def display_full_name(self):
        return f'{self.first_name} {self.last_name}'
    display_full_name.short_description = 'Name'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author',
                               on_delete=models.SET_NULL,
                               null=True)
    summary = models.TextField(max_length=1000,
                               help_text='Enter the description of the book')
    isbn = models.CharField('ISBN',
                            max_length=13,
                            help_text='13 character')
    genre = models.ManyToManyField(Genre,
                                   help_text='Select a genre for this book')
    language = models.ForeignKey('Language',
                                 on_delete=models.SET_NULL,
                                 null=True)

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()])
    display_genre.short_description = 'Genre'

    def __str__(self):
        return self.title


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          help_text='Unique ID for this particular'
                                    ' book across whole library')
    book = models.ForeignKey('Book',
                             on_delete=models.SET_NULL,
                             null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),

    )

    status = models.CharField(max_length=1,
                              choices=LOAN_STATUS,
                              blank=True,
                              default='m',
                              help_text='Book availability')

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id}. Name book: {self.book.title}'
