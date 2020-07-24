from django.shortcuts import render
from . import models
from django.views import generic

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


class BookListView(generic.ListView):
    model = models.Book
    paginate_by = 3


class BookDetailView(generic.DetailView):
    model = models.Book


class AuthorListView(generic.ListView):
    model = models.Author


class AuthorDetailView(generic.DetailView):
    model = models.Author
