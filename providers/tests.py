from django.test import Client, TestCase
from django.urls import reverse
from providers.models import Providers


class ProvidersTestCase(TestCase):
    client = Client()

    def setUp(self):
        Providers.objects.create(
            id=0,
            first_name='Firstname',
            last_name='Lastname',
            birth_date='1900-01-01',
            sex='Female',
            rating=10.0,
            primary_skills=['baseball'],
            secondary_skills=['soccer'],
            company='Company',
            country='USA',
            language='English',
            active=True,
            search_returns=10,
        )
        Providers.objects.create(
            id=1,
            first_name='Firstname2',
            last_name='Lastname2',
            birth_date='2000-01-01',
            sex='Male',
            rating=5.0,
            primary_skills=['running'],
            secondary_skills=['walking'],
            company='Hi',
            country='Spain',
            language='Spanish',
            active=False,
            search_returns=5,
        )

    def test_get_all(self):
        response = self.client.get(reverse('get_providers'))

        self.assertEqual(len(response.json()), 2)

        self.assertEqual(response.json()[0]['first_name'], 'Firstname2')
        self.assertEqual(response.json()[0]['last_name'], 'Lastname2')
        self.assertEqual(response.json()[0]['country'], 'Spain')

        self.assertEqual(response.json()[1]['first_name'], 'Firstname')
        self.assertEqual(response.json()[1]['last_name'], 'Lastname')
        self.assertEqual(response.json()[1]['country'], 'USA')

    def test_get_active(self):
        response = self.client.get(reverse('get_providers'), {'active': 'true'})

        self.assertEqual(len(response.json()), 1)

        self.assertEqual(response.json()[0]['first_name'], 'Firstname')
        self.assertEqual(response.json()[0]['last_name'], 'Lastname')
        self.assertEqual(response.json()[0]['country'], 'USA')

    def test_get_not_active(self):
        response = self.client.get(reverse('get_providers'), {'active': 'false'})

        self.assertEqual(len(response.json()), 1)

        self.assertEqual(response.json()[0]['first_name'], 'Firstname2')
        self.assertEqual(response.json()[0]['last_name'], 'Lastname2')
        self.assertEqual(response.json()[0]['country'], 'Spain')

    def test_get_user_traits(self):
        response = self.client.get(reverse('get_providers'), {'language': 'pan'})
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['language'], 'Spanish')

    def test_search_by_primary_skill(self):
        response = self.client.get(reverse('get_providers'), {'primary_skills': 'running'})
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['primary_skills'], ['running'])

    def test_search_by_secondary_skill(self):
        response = self.client.get(reverse('get_providers'), {'secondary_skills': 'soccer'})
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['secondary_skills'], ['soccer'])


class ProvidersSortByRatingsTestCase(TestCase):
    client = Client()

    def setUp(self):
        Providers.objects.create(
            id=0,
            first_name='Firstname',
            last_name='Lastname',
            birth_date='1900-01-01',
            sex='Female',
            rating=5.0,
            primary_skills=['baseball'],
            secondary_skills=['soccer'],
            company='Company',
            country='USA',
            language='English',
            active=True,
            search_returns=1,
        )
        Providers.objects.create(
            id=1,
            first_name='Firstname2',
            last_name='Lastname2',
            birth_date='2000-01-01',
            sex='Male',
            rating=6.0,
            primary_skills=['running'],
            secondary_skills=['walking'],
            company='Hi',
            country='Spain',
            language='Spanish',
            active=True,
            search_returns=1,
        )

    def test_higher_rating(self):
        response = self.client.get(reverse('get_providers'))

        self.assertEqual(response.json()[0]['first_name'], 'Firstname2')
        self.assertEqual(response.json()[0]['last_name'], 'Lastname2')
        self.assertEqual(response.json()[0]['country'], 'Spain')
        self.assertEqual(response.json()[0]['rating'], 6.0)

        self.assertEqual(response.json()[1]['first_name'], 'Firstname')
        self.assertEqual(response.json()[1]['last_name'], 'Lastname')
        self.assertEqual(response.json()[1]['country'], 'USA')
        self.assertEqual(response.json()[1]['rating'], 5.0)


class ProvidersSortBySearchResultsTestCase(TestCase):
    client = Client()

    def setUp(self):
        Providers.objects.create(
            id=0,
            first_name='Firstname',
            last_name='Lastname',
            birth_date='1900-01-01',
            sex='Female',
            rating=5.0,
            primary_skills=['baseball'],
            secondary_skills=['soccer'],
            company='Company',
            country='USA',
            language='English',
            active=True,
            search_returns=1,
        )
        Providers.objects.create(
            id=1,
            first_name='Firstname2',
            last_name='Lastname2',
            birth_date='2000-01-01',
            sex='Male',
            rating=5.0,
            primary_skills=['running'],
            secondary_skills=['walking'],
            company='Hi',
            country='Spain',
            language='Spanish',
            active=True,
            search_returns=2,
        )

    def test_search_results(self):
        response = self.client.get(reverse('get_providers'))

        self.assertEqual(response.json()[0]['first_name'], 'Firstname')
        self.assertEqual(response.json()[0]['last_name'], 'Lastname')
        self.assertEqual(response.json()[0]['country'], 'USA')
        self.assertEqual(response.json()[0]['search_returns'], 2)  # It jumps up 1

        self.assertEqual(response.json()[1]['first_name'], 'Firstname2')
        self.assertEqual(response.json()[1]['last_name'], 'Lastname2')
        self.assertEqual(response.json()[1]['country'], 'Spain')
        self.assertEqual(response.json()[1]['search_returns'], 3)  # It jumps up 1
