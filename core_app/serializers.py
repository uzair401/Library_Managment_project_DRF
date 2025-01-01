from rest_framework import serializers
from .models import Book, Genre, Rack, BorrowedRecord
from django.utils import timezone


class GenreSerializer(serializers.ModelSerializer):
    book_count = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = '__all__'
    
    def get_book_count(self, obj):
        return obj.book_set.count()

    validators = [
        serializers.UniqueTogetherValidator(
            queryset=Genre.objects.all(),
            fields=['name'],
            message='Genre with this name already exists.'
        )
    ]

class RackSerializer(serializers.ModelSerializer):
    available_space = serializers.SerializerMethodField()

    class Meta:
        model = Rack
        fields = '__all__'

    def get_available_space(self, obj):
        return obj.capacity - obj.book_set.count()
        
    validators = [
        serializers.UniqueTogetherValidator(
            queryset=Rack.objects.all(),
            fields=['number', 'floor', 'section'],
            message='Rack with this number, floor and section already exists.'
        )
    ]   

class BookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    rack = RackSerializer(read_only=True)
    
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    validators = [
        serializers.UniqueTogetherValidator(
            queryset=Book.objects.all(),
            fields=['title', 'author'],
            message='Book with this title and author already exists.'
        )
    ]

class BorrowedRecordSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    is_overdue = serializers.SerializerMethodField()
    
    class Meta:
        model = BorrowedRecord
        fields = '__all__'
        read_only_fields = ['borrowed_date']
    
    def get_is_overdue(self, obj):
        return obj.due_date < timezone.now() if obj.due_date else False
        
    validators = [
        serializers.UniqueTogetherValidator(
            queryset=BorrowedRecord.objects.all(),
            fields=['book', 'borrowed_date'],
            message='This book is already borrowed.'
        )
    ]