from django.contrib import admin


# Register your models here.
from .models import Author, NaturalLanguage, Genre, Book, BookInstance

# Register inline classes for inline editing within admin pages
class BooksInstanceInline(admin.TabularInline):
	model = BookInstance
	# extra attribute determines extra placeholder items to show. setting to 0 makes it so that you have to click +add to add new one
	extra = 0


class BooksInline(admin.TabularInline):
	model = Book
	# extra attribute determines extra placeholder items to show. setting to 0 makes it so that you have to click +add to add new one
	extra = 0

##################
# Register Admin Pages for the following models
# Decided to go with decorator registerations. For all desired changes to admin views, modify the associated class.
##################

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	"""
	Modify the Author admin view below
	"""
	list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
	# "fields" lists the fields you want displayed in detailed view, tuples put fields on same lines.
	fields = [('first_name', 'last_name'), ('date_of_birth', 'date_of_death')]

	inlines = [BooksInline]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	"""
	Modify the Book admin view below
	"""
	list_display = ('title', 'language', 'author', 'isbn')
	list_filter = ('language', 'author')

	inlines = [BooksInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
	"""
	Modify the BookInstance admin view below
	"""
	list_display = ('book', 'status', 'borrower', 'due_back', 'id')
	list_filter = ('status', 'due_back')

	# 'fieldsets' break view into segments, with bar/title breaking it.
	fieldsets = (
		('Book Information', {
			'fields': ('book', 'imprint', 'id')
		}),
		('Availability', {
			'fields': ('status', 'due_back', 'borrower')
		}),
		)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
	"""
	Genre is a Single Field Model, no need to modify
	"""
	pass


@admin.register(NaturalLanguage)
class NaturalLanguageAdmin(admin.ModelAdmin):
	"""
	NaturalLanguage is a Single Field Model, no need to modify
	"""
	pass