from django.shortcuts import render
from . import models

# Create your views here.


def index(request):
    num_books = models.Book.objects.all().count()
    num_instances = models.BookInstance.objects.all().count()
    num_instances_available = models.BookInstance.objects.filter(status__exact='a').count()
    num_authors = models.Author.objects.count()
    num_genre = models.Genre.objects.all().count()
    num_books_dota = models.Book.objects.filter(title__icontains='dota').count()

    return render(request,
                  'index.html',
                  context={'num_books': num_books,
                           'num_instances': num_instances,
                           'num_instances_available': num_instances_available,
                           'num_authors': num_authors,
                           'num_genre': num_genre,
                           'num_books_dota': num_books_dota,
                           }
                  )