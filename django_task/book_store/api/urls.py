from django.urls import path

from api.views import (BookListCreateAPIView,
                       BookRetrieveUpdateDestroyAPIView,
                       BookBuyAPIView,
                       AuthorListCreateAPIView,
                       AuthorRetrieveUpdateAPIView
                       )


urlpatterns = [
    path('books/', BookListCreateAPIView.as_view()),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view()),
    path('books/<int:pk>/buy/', BookBuyAPIView.as_view()),
    path('authors/', AuthorListCreateAPIView.as_view()),
    path('authors/<int:pk>/', AuthorRetrieveUpdateAPIView.as_view())
]
