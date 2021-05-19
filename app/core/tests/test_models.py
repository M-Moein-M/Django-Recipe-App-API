from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@gmail.com', password='test-password'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_create_user_with_email(self):
        """Test creating new user with email"""
        email = 'test@gmail.com'
        password = 'tESt1!1'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email for new user is normalized"""
        email = 'test@GMAIL.COM'
        user = get_user_model().objects.create_user(
            email=email,
            password='x'
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """New user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password='tESt1!1'
            )

    def test_create_new_super_user(self):
        """Test creating new super user"""
        user = get_user_model().objects.create_superuser(
            email='test@gmail.com',
            password='tESt1!1'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Italian'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredients_str(self):
        """Test ingredients string representation"""
        ingredients = models.Ingredient.objects.create(
            user=sample_user(),
            name='Apple'
        )

        self.assertEqual(str(ingredients), ingredients.name)

    def test_recipe_str(self):
        """Test recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Recipe Title',
            time=5,
            price=10.2,
        )
        self.assertEqual(str(recipe), recipe.title)
