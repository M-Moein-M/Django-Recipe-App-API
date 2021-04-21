from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag
from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """Test publicly available tags api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for listing tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test authorized tags api"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'test-password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.objects.create(user=self.user, name='Persian')
        Tag.objects.create(user=self.user, name='Italian')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that returned tags are only for authenticated user"""
        user2 = get_user_model().objects.create_user(
            'user2@gmail.com',
            'user2-password'
        )
        Tag.objects.create(user=user2, name='Dessert')
        tag = Tag.objects.create(user=self.user, name='Mexican')

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

        t_user = Tag.objects.filter(id=res.data[0]['id'])[0]
        self.assertEqual(t_user.user.id, self.user.id)

    def test_create_tag_successful(self):
        """Test creating new tag"""
        payload = {'name': 'TestName'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating new tag with invalid data"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
