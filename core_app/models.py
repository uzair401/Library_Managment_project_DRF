from django.db import models

# Create your models here.

class Rack(models.Model):
    name = models.CharField(max_length=200)
    number = models.IntegerField(unique=True)
    floor = models.IntegerField()
    section = models.CharField(max_length=200)
    capacity = models.IntegerField()
    current_count = models.IntegerField()
    
    def __str__(self):
        return self.name
    


class Genre(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name



class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    copies_available = models.IntegerField()
    total_copies = models.IntegerField()
    genre = models.ForeignKey('Genre', on_delete= models.CASCADE)
    rack = models.ForeignKey('Rack', on_delete= models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[
            ('available', 'Available'),
            ('borrowed', 'Boroorwed'),
        ],
        default='available'
    )
    
    def __str__(self):
        return self.title
    

class BorrowedRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned_date = models.DateTimeField(null=True)
    status = models.CharField(
         max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('returned', 'Returned'),
            ('overdue', 'Overdue'),
        ],
        default='pending'
    )
    def __str__(self):
        return self.book.title 
