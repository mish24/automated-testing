from datetime import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.six import BytesIO
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APITestCase

from pcsa.models import PcsaPost
from pcsa.serializers import PcsaPostSerializer
from pcsa.views import delete_post_by_id, get_post_by_id
from signup.models import Pcuser


# Create your tests here.

class PcsaTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_superuser(username='admin',
                                                password='password',
                                                email='')

        self.user2 = User.objects.create_superuser(username='admin2',
                                                password='password2',
                                                email='')

        self.user1.save()
        self.user2.save()

        self.o1 = Pcuser(user=self.user1)
        self.o2 = Pcuser(user=self.user2)

        self.o1.save()
        self.o2.save()

        self.post1 = PcsaPost(owner=self.o1,
                       title="Title 1",
                       description="Description 1")

        self.post2 = PcsaPost(owner=self.o2,
                       title="Title 2",
                       description="Description 2")

        self.post3 = PcsaPost(owner=self.o1,
                       title="Title 3",
                       description="Description 3")

        self.post4 = PcsaPost(owner=self.o2,
                       title="Title 4",
                       description="Description 4")

        self.post5 = PcsaPost(owner=self.o1,
                       title="Title 5",
                       description="Description 5")

        self.post1.save()
        self.post2.save()
        self.post3.save()
        self.post4.save()
        self.post5.save()

        self.data_1 = {'owner': 1,
                       'title': 'Test 1',
                       'description': 'Test 1',
                       'created': datetime.now(),
                       'id': '1'}

        self.data_2 = {'owner': 1,
                       'title': 'Test 2',
                       'description': 'Test 2',
                       'created': datetime.now(),
                       'id': '2'}

        self.data_3 = {'owner': 1,
                       'title': 'Test 3',
                       'description': 'Test 3',
                       'created': datetime.now(),
                       'id': '3'}

        self.authenticate()


    def test_delete_post_by_id(self):

        self.assertTrue(delete_post_by_id(self.post1.id))
        self.assertTrue(delete_post_by_id(self.post2.id))
        self.assertTrue(delete_post_by_id(self.post3.id))

        self.assertFalse(delete_post_by_id(-999999))
        self.assertFalse(delete_post_by_id(-1))
        self.assertFalse(delete_post_by_id(100))
        self.assertFalse(delete_post_by_id(200))
        self.assertFalse(delete_post_by_id(300))
        self.assertFalse(delete_post_by_id(400))
        self.assertFalse(delete_post_by_id(500))
        self.assertFalse(delete_post_by_id(600))
        self.assertFalse(delete_post_by_id(999))
        self.assertFalse(delete_post_by_id(999999))

    def test_get_post_by_id(self):

       post = get_post_by_id(self.post1.id)
       self.assertIsNotNone(post)
       self.assertEqual(post, self.post1)
       self.assertEqual(post.id, self.post1.id)
       self.assertEqual(post.owner, self.post1.owner)
       self.assertEqual(post.title, self.post1.title)
       self.assertEqual(post.description, self.post1.description)

       post = get_post_by_id(self.post2.id)
       self.assertIsNotNone(post)
       self.assertEqual(post, self.post2)
       self.assertEqual(post.id, self.post2.id)
       self.assertEqual(post.owner, self.post2.owner)
       self.assertEqual(post.title, self.post2.title)
       self.assertEqual(post.description, self.post2.description)

       post = get_post_by_id(self.post3.id)
       self.assertIsNotNone(post)
       self.assertEqual(post, self.post3)
       self.assertEqual(post.id, self.post3.id)
       self.assertEqual(post.owner, self.post3.owner)
       self.assertEqual(post.title, self.post3.title)
       self.assertEqual(post.description, self.post3.description)

       self.assertIsNone(get_post_by_id(-999999))
       self.assertIsNone(get_post_by_id(-1))
       self.assertIsNone(get_post_by_id(100))
       self.assertIsNone(get_post_by_id(200))
       self.assertIsNone(get_post_by_id(300))
       self.assertIsNone(get_post_by_id(999))
       self.assertIsNone(get_post_by_id(999999))

       self.assertNotEqual(get_post_by_id(-999999), self.post1)
       self.assertNotEqual(get_post_by_id(-1), self.post1)
       self.assertNotEqual(get_post_by_id(100), self.post1)
       self.assertNotEqual(get_post_by_id(200), self.post1)
       self.assertNotEqual(get_post_by_id(300), self.post1)
       self.assertNotEqual(get_post_by_id(999), self.post1)
       self.assertNotEqual(get_post_by_id(999999), self.post1)

       self.assertNotEqual(get_post_by_id(-999999), self.post2)
       self.assertNotEqual(get_post_by_id(-1), self.post2)
       self.assertNotEqual(get_post_by_id(100), self.post2)
       self.assertNotEqual(get_post_by_id(200), self.post2)
       self.assertNotEqual(get_post_by_id(300), self.post2)
       self.assertNotEqual(get_post_by_id(999), self.post2)
       self.assertNotEqual(get_post_by_id(999999), self.post2)

       self.assertNotEqual(get_post_by_id(-999999), self.post3)
       self.assertNotEqual(get_post_by_id(-1), self.post3)
       self.assertNotEqual(get_post_by_id(100), self.post3)
       self.assertNotEqual(get_post_by_id(200), self.post3)
       self.assertNotEqual(get_post_by_id(300), self.post3)
       self.assertNotEqual(get_post_by_id(999), self.post3)
       self.assertNotEqual(get_post_by_id(999999), self.post3)

       self.assertNotEqual(get_post_by_id(self.post1.id), self.post2)
       self.assertNotEqual(get_post_by_id(self.post1.id), self.post3)

       self.assertNotEqual(get_post_by_id(self.post2.id), self.post1)
       self.assertNotEqual(get_post_by_id(self.post2.id), self.post3)

       self.assertNotEqual(get_post_by_id(self.post3.id), self.post1)
       self.assertNotEqual(get_post_by_id(self.post3.id), self.post2)

#tests for pcsa serializer
    def authenticate(self):
        """Authenticate with the API using a username and password"""
        self.client.login(username='admin', password='password')

    def unauthenticate(self):
        """Unauthenticate with the API"""
        self.client.force_authenticate(user=None)

    def test_detail_delete_cases(self):
        """Test HTTP DELETE API calls to post-detail endpoint"""

        post_list = PcsaPost.objects.all().order_by('id')

        for post in post_list:
            post_id = str(post.id)
            url = reverse('post-detail', args=[post_id])
            response = self.client.delete(url)
            self.assertEqual(response.status_code,
                             status.HTTP_405_METHOD_NOT_ALLOWED)
            self.assertIsNotNone(PcsaPost.objects.get(id=post_id))

    def test_detail_head_cases(self):
        """Test HTTP HEAD API calls to post-detail endpoint"""

        post_list = PcsaPost.objects.all().order_by('id')

        for post in post_list:
            post_id = str(post.id)
            url = reverse('post-detail', args=[post_id])
            response = self.client.head(url)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_negative_cases(self):
        """Test negative API calls to post-detail endpoint"""

        nonexistant_post_ids = [99, 100, 101, 1000, 1001, 1002, -1, -99, -100]

        for post_id in nonexistant_post_ids:
            url = reverse('post-detail', args=[post_id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_options_cases(self):
        """Test HTTP OPTIONS API calls to post-detail endpoint"""

        post_list = PcsaPost.objects.all().order_by('id')

        for post in post_list:
            post_id = str(post.id)
            url = reverse('post-detail', args=[post_id])
            response = self.client.options(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_positive_cases(self):
        """Test positive API calls to post-detail endpoint"""

        post_list = PcsaPost.objects.all().order_by('id')

        for post in post_list:

            post_id = str(post.id)
            serializer = PcsaPostSerializer(post)
            content = JSONRenderer().render(serializer.data)

            url = reverse('post-detail', args=[post_id])
            response = self.client.get(url)

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(response.accepted_media_type, 'application/json')

    def test_detail_post_cases(self):
        """Test HTTP POST API calls to post-detail endpoint"""

        post_list_before = PcsaPost.objects.all().order_by('id')

        for post in post_list_before:
            post_id = str(post.id)
            url = reverse('post-detail', args=[post_id])
            response = self.client.post(url, self.data_1, format='json')
            self.assertEqual(response.status_code,
                             status.HTTP_405_METHOD_NOT_ALLOWED)

        post_list_after = PcsaPost.objects.all().order_by('id')
        self.assertEqual(len(post_list_before), len(post_list_after))

        for post in post_list_before:
            self.assertEqual(PcsaPost.objects.get(id=post.id), post)

    def test_detail_put_cases(self):
        """Test HTTP PUT API calls to post-detail endpoint"""

        post_list_before = PcsaPost.objects.all().order_by('id')

        for post in post_list_before:
            post_id = str(post.id)
            url = reverse('post-detail', args=[post_id])
            response = self.client.put(url, self.data_1, format='json')
            self.assertEqual(response.status_code,
                             status.HTTP_405_METHOD_NOT_ALLOWED)

        post_list_after = PcsaPost.objects.all().order_by('id')
        self.assertEqual(len(post_list_before), len(post_list_after))

        for post in post_list_before:
            self.assertEqual(PcsaPost.objects.get(id=post.id), post)

    def test_detail_unauthenticated_cases(self):
        """Test unauthenticated API calls to post-detail endpoint"""

        self.unauthenticate()
        post_list_before = PcsaPost.objects.all().order_by('id')

        for post in post_list_before:

            post_id = str(post.id)
            url = reverse('post-detail', args=[post_id])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            response = self.client.head(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            response = self.client.options(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            response = self.client.post(url, self.data_1, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            response = self.client.put(url, self.data_1, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        post_list_after = PcsaPost.objects.all().order_by('id')
        self.assertEqual(len(post_list_before), len(post_list_after))

        for post in post_list_before:
            self.assertEqual(PcsaPost.objects.get(id=post.id), post)

    def test_list_delete_cases(self):
        """Test HTTP DELETE API calls to post-list endpoint"""

        url = reverse('post-list')
        post_list = PcsaPost.objects.all().order_by('id')
        response = self.client.delete(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        for post in post_list:
            self.assertIsNotNone(PcsaPost.objects.get(id=post.id))

    def test_list_get_cases(self):
        """Test HTTP GET API calls to post-list endpoint"""

        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        post_list = PcsaPost.objects.all().order_by('id')
        stream = BytesIO(response.render().content)
        data = JSONParser().parse(stream)
        results = data['results']
        i = 0

        for post in results:
            serializer = PcsaPostSerializer(post_list[i])
            content_db = JSONRenderer().render(serializer.data)
            serializer = PcsaPostSerializer(post)
            content_api = JSONRenderer().render(serializer.data)
            i = i + 1

    def test_list_head_cases(self):
        """Test HTTP HEAD API calls to post-list endpoint"""

        url = reverse('post-list')
        response = self.client.head(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_options_cases(self):
        """Test HTTP OPTIONS API calls to post-list endpoint"""

        url = reverse('post-list')
        response = self.client.options(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_post_cases(self):
        """Test HTTP POST API calls to post-list endpoint"""

        url = reverse('post-list')
        post_list_before = PcsaPost.objects.all().order_by('id')

        response = self.client.post(url, self.data_1, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.post(url, self.data_2, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.post(url, self.data_3, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        post_list_after = PcsaPost.objects.all().order_by('id')
        self.assertEqual(len(post_list_before), len(post_list_after))

        for post in post_list_before:
            self.assertEqual(PcsaPost.objects.get(id=post.id), post)

    def test_list_put_cases(self):
        """Test HTTP PUT API calls to post-list endpoint"""

        url = reverse('post-list')
        post_list_before = PcsaPost.objects.all().order_by('id')

        response = self.client.put(url, self.data_1, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(url, self.data_2, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(url, self.data_3, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        post_list_after = PcsaPost.objects.all().order_by('id')
        self.assertEqual(len(post_list_before), len(post_list_after))

        for post in post_list_before:
            self.assertEqual(PcsaPost.objects.get(id=post.id), post)

    def test_list_unauthenticated_cases(self):
        """Test unauthenticated API calls to post-list endpoint"""

        self.unauthenticate()
        url = reverse('post-list')
        post_list_before = PcsaPost.objects.all().order_by('id')

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.head(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.options(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(url, self.data_1, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.put(url, self.data_1, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        post_list_after = PcsaPost.objects.all().order_by('id')
        self.assertEqual(len(post_list_before), len(post_list_after))

        for post in post_list_before:
		self.assertEqual(PcsaPost.objects.get(id=post.id), post)
