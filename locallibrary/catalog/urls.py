from django.urls import path
from . import views

#####################
# Base url patterns
#####################
urlpatterns = [
	path('', views.index, name='index'),
	path('myaccount/<int:pk>', views.MyAccountView.as_view(), name='myaccount'),
	path('myaccount/<int:pk>/edit/', views.MyAccountEditView.as_view(), name='myaccount-edit'),
]


########################
# Author url patterns
########################
urlpatterns += [
	path('authors/', views.AuthorListView.as_view(), name='authors'),
	path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
	path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
	path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
	path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
]


#######################
# Book url patterns
#######################
urlpatterns += [
	path('books/', views.BookListView.as_view(), name='books'),
	path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
	path('book/create/', views.BookCreate.as_view(), name='book_create'),
	path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
	path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
	path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
	path('myborrowedbooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
	path('allborrowedbooks/', views.LoanedBooksListView.as_view(), name='all-borrowed'),
]


#######################
# BookInstance url patterns
#######################
urlpatterns += [
	path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
	path('myborrowedbooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
	path('allborrowedbooks/', views.LoanedBooksListView.as_view(), name='all-borrowed'),
]