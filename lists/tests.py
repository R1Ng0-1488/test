from django.test import TestCase

# Create your tests here.
class SmokeTest(TestCase):
	"""toxic test"""

	def test_bad_maths(self):
		"""test: wrong maths counts"""
		self.assertEqual(1 + 1, 3)