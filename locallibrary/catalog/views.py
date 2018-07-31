from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic

# @login_required at function based views to require login to view page (will redirect to login page)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

# Use LoginRequiredMixin as parameter in class based views to require login for those pages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

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

# Class based view, using generic list view
class BookListView(generic.ListView):
	model = Book
	paginate_by = 2

# Class based view, using generic list view
class AuthorListView(generic.ListView):
	model = Author
	paginate_by = 2

# Class based view, using generic detail view
class BookDetailView(generic.DetailView):
	model = Book

# Class based view, using generic detail view
class AuthorDetailView(generic.DetailView):
	model = Author

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
		
