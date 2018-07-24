from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre

# Create your views here.


################
# Index Page
################
def index(request):
	"""
	View functionf or home page of site
	"""

	# Generate counts of asome of the main objects
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()
	num_authors = Author.objects.count() # the .all() is implied by defult, example.
	# Available books (status = 'a')
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()

	# Render the HTML template index.html with the data in the context variable
	return render(
		request,
		'index.html',
		context = {'num_books':num_books, 'num_instances':num_instances, 'num_instances_available':num_instances_available, 'num_authors':num_authors},
	)