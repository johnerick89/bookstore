from django.test import TestCase
from books.models import Book, Rental
from books.serializers import BookSerializer, RentalSerializer
from rest_framework.test import APIClient,RequestsClient
from django.urls import reverse
from rest_framework import status
import json


class GetAllBooksTest(TestCase):
    """ Test module for GET all books API """
    def setUp(self):
        Book.objects.create(
            title='Gifted Hands', code='Biography101')
        Book.objects.create(
            title='A grain of wheat', code='Novel101')
        Book.objects.create(
            title='Encounters from Africa', code='Fiction101')
        Book.objects.create(
            title='Introduction to Deep Learning', code='Technology101')
    
    def test_get_all_books(self):
        # get API response
        client = APIClient()
        response = client.get(
            f"/api/v1/books/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
class RentalsTest(TestCase):
    """
    Test book rental serilizers
    """
    def test_create_rental_record(self):
        client = APIClient()
        payload = {
            "customer": "Cynthia Awuor",
            "books_data": [
                {"id": 1,"duration": 10},
                {"id": 2, "duration": 30}
            ]
        }
        data =  json.dumps(payload)
        
        response = client.post(
            f"/api/v1/books/",data=json.loads(data),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
