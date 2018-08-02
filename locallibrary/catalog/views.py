from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import datetime

# import Model for Create Update Delte Requests
from .models import Author
from .models import Book
from django.contrib.auth.models import User

# @login_required at function based views to require login to view page (will redirect to login page)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

# Use LoginRequiredMixin as parameter in class based views to require login for those pages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

# For views handling Django Forms
from .forms import RenewBookForm

# Create your views here.

################
# Index Page
################
def index(request):
    """
    View functionf or home page of site
    """

    # GET summary from front end form input to search DB for books containing key words within their summary.
    try:
        summary = request.GET["summary"]
        num_books_summary = Book.objects.filter(summary__icontains=summary).count()
    except:
        summary = 0
        num_books_summary = 0
    # Generate counts of asome of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_authors = Author.objects.count() # the .all() is implied by defult, example.
    num_genres = Genre.objects.count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context = {
        'num_books':num_books, 
        'num_instances':num_instances, 
        'num_instances_available':num_instances_available, 
        'num_authors':num_authors, 
        'num_genres':num_genres, 
        'num_books_summary':num_books_summary, 
        'summary_search':summary, 
        'num_visits':num_visits,},
    )

######################
# Book views
#######################

# Class based view, using generic list view
class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


# Class based view, using generic detail view
class BookDetailView(generic.DetailView):
    model = Book


class BookCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Book
    permission_required = 'catalog.can_add_book'
    fields = '__all__'
    # this demonstrates setting initial values
    # proposed_date_of_death = datetime.date.today()
    # initial = {'date_of_death': proposed_date_of_death}


class BookUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Book
    permission_required = 'catalog.can_change_book'
    fields = ['title', 'author', 'summary', 'language', 'genre']


class BookDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Book
    permission_required = 'catalog.can_delete_book'
    template_name_suffix = '_delete'
    success_url = reverse_lazy('books')

######################
# Book Instance views
#######################

# Class based view, using generic list view
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    """docstring for LoanedBooksListView"""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_librarian.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


# function that handles renewing a book (updating the due_back field of BookInstance model)
@permission_required('catalog.can_renew')
def renew_book_librarian(request, pk):
    """
       View function for renewing a specific BookInstance by librarian
    """

    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})


#########################################
# Author Create Read Update Delete Views
#########################################

# Class based view, using generic list view
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


# Class based view, using generic detail view
class AuthorDetailView(generic.DetailView):
    model = Author


class AuthorCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Author
    permission_required = 'catalog.can_add_author'
    fields = '__all__'
    # this demonstrates setting initial values
    # proposed_date_of_death = datetime.date.today()
    # initial = {'date_of_death': proposed_date_of_death}


class AuthorUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Author
    permission_required = 'catalog.can_change_author'
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Author
    permission_required = 'catalog.can_delete_author'
    template_name_suffix = '_delete'
    success_url = reverse_lazy('authors')


#########################################
# Account Read Update Views
#########################################

class MyAccountView(LoginRequiredMixin, generic.DetailView):
    model = User

class MyAccountEditView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    success_url = reverse_lazy('index' )