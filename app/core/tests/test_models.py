from django.test import TestCase
from django.contrib.auth import get_user_model


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

	def test_new_user_email_normalizedd(self):
		"""Test email for new user is notmalized"""
		email = 'test@GMAIL.COM'
		user = get_user_model().objects.create_user(
			email=email,
			password='x'
		)
		self.assertEqual(user.email, email.lower())
