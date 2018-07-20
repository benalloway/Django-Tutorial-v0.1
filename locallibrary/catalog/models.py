from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns


################
# Genre 
################
class Ganre(models.Model):
	"""
	Model representing a book genre (e.g. Science Fiction, Non Fiction, Military History)
	"""

	name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

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
	author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
	# Foreign Key used because book can only have one author, but authors can have multiple books
	# Author as a string rather than object bc/ it hasn't been declared yet in the file.
	summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
	isbn = models.CharField("ISBN", max_length=13, help_text="13 Character <a href='https://www.isbn-international.org/content/what-isbn'>ISBN number</a>")
	genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
	# ManyToManyField used bc/ genre can contain many books. Books can cover many genres.
	# Genre class has already been defined so we can specify the object above.

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