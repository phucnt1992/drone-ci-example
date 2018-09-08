from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

import factory
import faker

from .models import Book
# Create your tests here.


class BookFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: 'book_%s' % n)

    class Meta:
        model = Book
        django_get_or_create = ('title',)


class BookAPITestCase(APITestCase):

    def setUp(self):
        self.faker = faker.Faker()

    def test_get_book_list(self):
        BookFactory.generate_batch(factory.enums.CREATE_STRATEGY, size=10)
        response = self.client.get(reverse('api:book-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 10)

    def test_get_book_detail(self):
        book = BookFactory.create()
        response = self.client.get(reverse('api:book-detail', args=[book.id]))
        book_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(book_json.get('id'), book.id)

    def test_post_book(self):
        response = self.client.post(reverse('api:book-list'), data={
            'title': 'batman',
            'description': self.faker.text(),
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_book(self):
        book = BookFactory.create()
        self.assertNotEqual(Book.objects.get(id=book.id).title, 'batman')
        response = self.client.put(reverse('api:book-detail', args=[book.id]), data={
            'title': 'batman',
            'description': self.faker.text(),
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get(id=book.id).title, 'batman')

    def test_patch_book(self):
        book = BookFactory.create()
        self.assertEqual(Book.objects.count(), 1)
        self.assertNotEqual(Book.objects.get(id=book.id).title, 'batman')
        response = self.client.patch(reverse('api:book-detail', args=[book.id]), data={
            'title': 'batman',
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get(id=book.id).title, 'batman')

    def test_delete_book(self):
        book = BookFactory.create()
        self.assertEqual(Book.objects.count(), 1)
        response = self.client.delete(reverse('api:book-detail', args=[book.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
