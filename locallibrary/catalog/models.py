from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User
from datetime import date



################
# Genre 
################
class Genre(models.Model):
	"""
	Model representing a book genre (e.g. Science Fiction, Non Fiction, Military History)
	"""

	name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

	class Meta:
		ordering = ["name"]

	def __str__(self):
		"""
		String for representing the Model object (in Admin site etc.)
		"""
		return self.name


################
# NaturalLanguage 
################
class NaturalLanguage(models.Model):
	"""
	Model representing the natural language of the book (e.g. English, French, Japanese etc.)
	"""

	name = models.CharField(max_length=200, help_text="Enter the book's natural language (e.g. English, French etc.)")
	
	class Meta:
		ordering = ["name"]

	def __str__(self):
		"""
		String for representing the Model object (in Admin site etc.)
		"""
		return self.name


################
# Book 
################
class Book(models.Model):
	"""
	Model representing a book (but not a specific copy of a book).
	"""

	title = models.CharField(max_length=200)
	summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
	isbn = models.CharField("ISBN", max_length=13, help_text="13 Character <a href='https://www.isbn-international.org/content/what-isbn'>ISBN number</a>")

	# Foreign Key used because Book can only have one natural language.
	language = models.ForeignKey(NaturalLanguage, on_delete=models.SET_NULL, null=True)

	# Author as a string rather than object bc/ it hasn't been declared yet in the file.
	# Foreign Key used because book can only have one author, but authors can have multiple books
	author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

	# ManyToManyField used bc/ genre can contain many books. Books can cover many genres.
	# Genre class has already been defined so we can specify the object above.
	genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")	

	class Meta:
		ordering = ["title"]
	
	def __str__(self):
		"""
		String for representing the Model object.
		"""
		return self.title

	def get_absolute_url(self):
		"""
		Returns the url to access a detail record for this book.
		"""
		return reverse('book-detail', args=[str(self.id)])


################
# BookInstance 
################
import uuid # Required for unique book instances


class BookInstance(models.Model):
	"""
	Model representing a a specific copy of a book (i.e that can be borrowed from the library).
	"""

	# List of book's loan statuses, default to Maintenance when book is created (until it is stocked)
	LOAN_STATUS = (
		('m', 'Maintenance'),
		('o', 'On Loan'),
		('a', 'Available'),
		('r', 'Reserved'),
	)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
	book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
	imprint = models.CharField(max_length=200)
	due_back = models.DateField(null=True, blank=True)
	status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text="Book availability")
	borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	@property
	def is_overdue(self):
		if self.due_back and date.today() > self.due_back:
			return True
		return False
	

	class Meta:
		ordering = ["due_back"]
		permissions = (
			("can_mark_returned", "Set book as returned"),
			)

	def __str__(self):
		"""
		String for representing the Model object
		"""
		return f'{self.id} ({self.book.title})'


################
# Author 
################
class Author(models.Model):
	"""
	Model representing an author.
	"""

	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	date_of_birth = models.DateField(null=True, blank=True)
	date_of_death = models.DateField('Died', null=True, blank=True)

	class Meta:
		ordering = ["last_name"]

	def get_absolute_url(self):
		"""
		Returns the url to access a particular author instance.
		"""
		return reverse('author-detail', args=[str(self.id)])

	def __str__(self):
		"""
		String for representing the Model object.
		"""
		return f'{self.last_name}, {self.first_name}'