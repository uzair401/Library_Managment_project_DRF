from rest_framework import serializers
from .models import Book, Genre, Rack, BorrowedRecord

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
    
    validators = [
        serializers.UniqueTogetherValidator(
            queryset=Book.objects.all(),
            fields=['title', 'author'],
            message='Book with this title and author already exists.'
        )
    ]

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
    
    validators = [
        serializers.UniqueTogetherValidator(
            queryset=Genre.objects.all(),
            fields=['name'],
            message='Genre with this name already exists.'
        )
    ]
        

class RackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rack
        fields = '__all__'
        
    validators = [
        serializers.UniqueTogetherValidator(
            queryset=Rack.objects.all(),
            fields=['number', 'floor', 'section'],
            message='Rack with this number, floor and section already exists.'
        )
    ]   

class BorrowedRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedRecord
        fields = '__all__'
        
    validators = [
        serializers.UniqueTogetherValidator(
            queryset=BorrowedRecord.objects.all(),
            fields=['book', 'borrowed_date'],
            message='This book is already borrowed.'
        )
    ]