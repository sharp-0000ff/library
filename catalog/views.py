from django.shortcuts import render
from . import models
from . import forms
from django.views import generic
from django.views.generic import edit
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import datetime


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


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(models.BookInstance, pk=pk)
    if request.method == 'POST':
        form = forms.RenewBookModelForm(request.POST)
        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = forms.RenewBookModelForm(initial={'renewal_date': proposed_renewal_date,})
    return render(request,
                  'catalog/book_renew_librarian.html',
                  {'form': form,
                   'bookinst': book_inst},
                  )


class AuthorCreate(edit.CreateView):
    model = models.Author
    fields = '__all__'


class AuthorUpdate(edit.UpdateView):
    model = models.Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(edit.DeleteView):
    model = models.Author
    success_url = reverse_lazy('authors')


class BookCreate(edit.CreateView):
    model = models.Book
    fields = '__all__'


class BookUpdate(edit.UpdateView):
    model = models.Book
    fields = '__all__'


class BookDelete(edit.DeleteView):
    model = models.Book
    success_url = reverse_lazy('books')
