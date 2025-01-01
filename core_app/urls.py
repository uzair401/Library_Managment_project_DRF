from django.urls import path
from . import views

urlpatterns = [
    # Genre URLs
    path('genres/', views.genre_list, name='genre-list'),
    path('genres/<int:pk>/', views.genre_detail, name='genre-detail'),
    
    # Rack URLs
    path('racks/', views.rack, name='rack-list'),
    path('racks/<int:pk>/', views.rack_list, name='rack-detail'),
    
    # Book URLs
    path('books/', views.book, name='book-list'),
    path('books/<int:pk>/', views.book_list, name='book-detail'),
    path('books/search/', views.book_search, name='book-search'),
    
    # Borrowed Books URLs
    path('borrowed/', views.borrowed_books, name='borrowed-books'),
    path('borrowed/<int:pk>/', views.update_borrow_data, name='update-borrow'),
    path('borrowed/<int:pk>/return/', views.return_book, name='return-book'),
    path('borrowed/overdue/', views.overdue_books, name='overdue-books'),
]