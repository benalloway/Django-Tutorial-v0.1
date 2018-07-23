from django.contrib import admin


# Register your models here.
from .models import Author, NaturalLanguage, Genre, Book, BookInstance


##################
# Register Admin Pages for the following models
# Decided to go with decorator registerations. For all desired changes to admin views, modify the associated class.
##################

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	pass


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
	pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
	pass


@admin.register(NaturalLanguage)
class NaturalLanguageAdmin(admin.ModelAdmin):
	pass