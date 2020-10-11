from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
	"""new visitor's test"""

	def setUp(self):
		"""installation"""
		self.browser = webdriver.Firefox()

	def tearDown(self):
		"""demontaj"""
		# close browser
		self.browser.quit()


	def test_can_start_a_list_and_retrieve_it_later(self):
		"""test: can start a list and get it later"""
		# Эдит слышала про крутое новое онлайн-приложение со
		# списком неотложных дел. Она решает оценить его
		# домашнюю страницу
		self.browser.get('http://localhost:8000')

		# Она видит, что заголовок и шапка страницы говорят о
		# списках неотложных дел
		print(self.browser.title, 'To-Do')
		self.assertIn('To-Do', self.browser.title)
		self.fail(self.browser.title)
		# comments...

if __name__ == '__main__':
	unittest.main(warnings='ignore')
