from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
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

	# Render the HTML template index.html with the data in the context variable
	return render(
		request,
		'index.html',
		context = {'num_books':num_books, 'num_instances':num_instances, 'num_instances_available':num_instances_available, 'num_authors':num_authors, 'num_genres':num_genres, 'num_books_summary':num_books_summary, 'summary_search':summary},
	)

class BookListView(generic.ListView):
	model = Book

class BookDetailView(generic.DetailView):
	model = Book