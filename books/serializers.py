from rest_framework import serializers
from books.models import Book, Rental
from django.http import Http404
from pprint import pprint
import json
from decimal import Decimal
import decimal


class BookSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(required=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    created = serializers.DateTimeField(read_only=True)
    book_type =serializers.CharField(required=True, max_length=100)
    daily_rental_charge =serializers.JSONField(required=True, allow_null=False)


    def create(self, validated_data):
        """
        Create and return a new `Book` instance, given the validated data.
        """
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Book` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.save()
        return instance


class RentalSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    customer = serializers.CharField(max_length=100, required=True)
    books_data  = serializers.JSONField(required=False, allow_null=True)
    total_rental_charge = serializers.DecimalField(required=False,max_digits=5, decimal_places=2)
    created = serializers.DateTimeField(read_only=True)

    
    def get_book(self, id):
        try:
            return Book.objects.get(pk=id)
        except Book.DoesNotExist:
            raise Http404
    
    def _convert_decimal_to_float(self,value):
        if isinstance(value, decimal.Decimal):
            return float(value)
        return value
    
    def _calculate_per_book_charge(self,book_rental_charges,duration):
        print(book_rental_charges)
        rate_type = book_rental_charges['rate']['type']
        fixed_rate_rate = book_rental_charges['rate']['fixed_rate_rate']
        rental_charge = 0
        
        if rate_type=='fixed':
            rental_charge = fixed_rate_rate * duration
        else:
            min_charge = book_rental_charges['minimum_rental_charge']
            fixed_rate_days = book_rental_charges['rate']['fixed_rate_days']
            extra_days_daily_charge = book_rental_charges['rate']['extra_days_daily_charge']
            if fixed_rate_days > duration:
                rental_charge = min_charge
            else:
                rental_charge = (fixed_rate_days* fixed_rate_rate) + ((duration-fixed_rate_days)*extra_days_daily_charge)
                if min_charge > rental_charge:
                    rental_charge = min_charge
        
        return rental_charge

    def _calculate_rental_cost(self, validated_data):
        basic_cost = 0
        total_cost = 0
        books = validated_data["books_data"]
        books_data = []
        for book in books:
            query_filter = dict(id=book["id"])
            bookModel = self.get_book(book["id"])
            book_data = book
            basic_cost = self._calculate_per_book_charge(bookModel.daily_rental_charge,book["duration"])
            total_cost = total_cost + basic_cost
            book_data.update(
                {
                "rental_charge": self._convert_decimal_to_float(basic_cost),
                "book_title":bookModel.title,
                "book_type":bookModel.book_type
                }
            )
            books_data.append(book_data)
        validated_data["total_rental_charge"] = total_cost
        return validated_data

    def create(self, validated_data):
        """
        Create and return a new `Book` instance, given the validated data.
        """
        validated_data = self._calculate_rental_cost(validated_data)
        return Rental.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Book` instance, given the validated data.
        """
        validated_data = self._calculate_rental_cost(validated_data)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.total_rental_charge = validated_data.get('total_rental_charge',instance.total_rental_charge)
        instance.books_data = validated_data.get('books_data',instance.books_data)
        instance.save()
        return instance
    
    

