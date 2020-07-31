from django.test import TestCase
from books.models import Book, Rental


class BookTest(TestCase):
    """ Test module for Book model """
    def setUp(self):
        Book.objects.create(
            title='Gifted Hands', code='Biography101', book_type='regular',daily_rental_charge=1.5)
    
    def test_book_created(self):
        gifted_book = Book.objects.get(title='Gifted Hands')
        self.assertIsNotNone(gifted_book)

class RentalTest(TestCase):
    """
    Test module for Rental model
    """
    def setUp(self):
        Rental.objects.create(
        customer= "Cynthia Awuor",
        books_data= [
            {
                "id": 1,
                "duration": 10,
                "rental_charge": 10
            },
            {
                "id": 2,
                "duration": 30,
                "rental_charge": 30
            }
        ],
        total_rental_charge= 40.00
        )
    
    def test_rental_created(self):
        rental = Rental.objects.get(customer="Cynthia Awuor")
        self.assertIsNotNone(rental)
    
