from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import F

from book.models import Book, User
from .serializers import BookSerializer, UserSerializer


class BookListCreateAPIView(APIView):

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookRetrieveUpdateDestroyAPIView(APIView):

    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookBuyAPIView(APIView):

    @transaction.atomic
    def post(self, request, pk):
        book = get_object_or_404(Book.objects.select_for_update(), pk=pk)
        if book.count <= 0:
            return Response(
                {'detail': 'Книги нет в наличии'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            Book.objects.filter(pk=book.pk).update(count=F('count') - 1)
            book.refresh_from_db()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorListCreateAPIView(APIView):

    def get(self, request):
        authors = User.objects.all()
        serializer = UserSerializer(authors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorRetrieveUpdateAPIView(APIView):
    def get(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(author)
        return Response(serializer.data)

    def put(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(author, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
