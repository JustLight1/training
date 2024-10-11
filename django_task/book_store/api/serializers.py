from rest_framework import serializers
from django.db import transaction
from django.db.models import F

from book.models import Book, User


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class BookSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

    @transaction.atomic
    def update(self, instance, validate_data):
        if instance.count <= 0:
            raise serializers.ValidationError(
                {'detail': 'Книги нет в наличии'}
            )

        Book.objects.filter(pk=instance.pk).update(count=F('count') - 1)
        instance.refresh_from_db()
        return instance
