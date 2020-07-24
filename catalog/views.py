from django.shortcuts import render
from . import models
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


def index(request):
    num_books = models.Book.objects.all().count()
    num_instances = models.BookInstance.objects.all().count()
    num_instances_available = models.BookInstance.objects.filter(status__exact='a').count()
    num_authors = models.Author.objects.count()
    num_genre = models.Genre.objects.all().count()
    num_books_dota = models.Book.objects.filter(title__icontains='dota').count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(request,
                  'index.html',
                  context={'num_books': num_books,
                           'num_instances': num_instances,
                           'num_instances_available': num_instances_available,
                           'num_authors': num_authors,
                           'num_genre': num_genre,
                           'num_books_dota': num_books_dota,
                           'num_visits': num_visits,
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


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = models.BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 5

    def get_queryset(self):
        return models.BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksAllListView(LoginRequiredMixin, generic.ListView):
    model = models.BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 5

    def get_queryset(self):
        return models.BookInstance.objects.filter(status__exact='o').order_by('due_back')
