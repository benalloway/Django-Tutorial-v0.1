from django.db import models

# Create your models here.

################
# Genres of books 
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