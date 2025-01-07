from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view 
from rest_framework import status
from .models import Book, Genre, Rack, BorrowedRecord
from .serializers import BookSerializer, GenreSerializer, RackSerializer, BorrowedRecordSerializer
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET', 'POST'])
def genre_list(request):
    if request.method == 'GET':
        genres = Genre.objects.all()
        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(genres, request)
        serializer = GenreSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    if request.method == 'POST':
        if isinstance(request.data, list):
            serializer = GenreSerializer(data=request.data, many=True)
        else:
            serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def genre_detail(request, pk):
    try:
        genre = Genre.objects.get(pk=pk)
    except Genre.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = GenreSerializer(genre)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = GenreSerializer(genre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def rack(request):
    if request.method == 'GET':
        racks = Rack.objects.all()
        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(racks, request)
        serializer = RackSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    if request.method == 'POST':
        if isinstance(request.data, list):
            serializer = RackSerializer(data=request.data, many=True)
        else:
            serializer = RackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def rack_list(request, pk):
    try:
        rack = Rack.objects.get(pk=pk)
    except Rack.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = RackSerializer(rack)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = RackSerializer(rack, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        rack.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def book(request):
    if request.method == 'GET':
        books = Book.objects.all()
        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(books, request)
        serializer = BookSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    if request.method == 'POST':
        if isinstance (request.data, list):
            serializer = BookSerializer(data = request.data, many=True)
        else:
            serializer = BookSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "Book has been added to the Library"}, serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def book_list(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def book_search(request):
    title = request.query_params.get('title')
    author = request.query_params.get('author')
    genre = request.query_params.get('genre')
    rack = request.query_params.get('rack')
    books = Book.objects.all()
    query = {}
    
    if title:
        query['title__icontains'] = title
    if author:
        query['author__icontains'] = author
    if genre:
        query['genre__name__icontains'] = genre
    if rack:
        query['rack__name__icontains'] = rack
    books = books.filter(**query)
    paginator = StandardResultsSetPagination()
    result_page = paginator.paginate_queryset(books, request)
    serializer = BookSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET', 'POST'])
def borrowed_books(request):
    if request.method == 'GET':
        borrowed_books = BorrowedRecord.objects.all()
        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(borrowed_books, request)
        serializer = BorrowedRecordSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    if request.method == 'POST':
        book_id = request.data.get('book')
        try:
            book = Book.objects.get(id=book_id)
            if book.available_copies <= 0:
                return Response(
                    {"error": "Book not available"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = BorrowedRecordSerializer(data=request.data)
            if serializer.is_valid():
                borrowed = serializer.save()
                book.available_copies -= 1
                book.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

@api_view(['GET', 'PUT'])
def update_borrow_data(request, pk):
    try:
        requested_book = BorrowedRecord.objects.get(pk=pk)
    except BorrowedRecord.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = BorrowedRecordSerializer(requested_book)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = BorrowedRecordSerializer(requested_book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def return_book(request, pk):
    try:
        borrowed_book = BorrowedRecord.objects.get(pk=pk)
        if borrowed_book.status == 'returned':
            return Response(
                {"error": "Book already returned"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        borrowed_book.status = 'returned'
        borrowed_book.returned_date = timezone.now()
        borrowed_book.save()
        
        book = borrowed_book.book
        book.available_copies += 1
        book.save()
        
        return Response(
            {"message": "Book has been returned successfully"}, 
            status=status.HTTP_200_OK
        )
    except BorrowedRecord.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def overdue_books(request):
    overdue = BorrowedRecord.objects.filter(
        status='approved',
        due_date__lt=timezone.now(),
        returned_date__isnull=True
    )
    paginator = StandardResultsSetPagination()
    result_page = paginator.paginate_queryset(overdue, request)
    serializer = BorrowedRecordSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)