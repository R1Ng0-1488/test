from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
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
		self.assertIn('To-Do', self.browser.title)
		# test header
		header_text = self.browser.find_element_by_tag_name('h1').text 
		self.assertIn('To-Do', header_text)
		# test placeholder of inputbox
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
			)
		# test 
		# Она набирате в текстовом поле "Купить павлиные перья"
		inputbox.send_keys('Купить павлиные крылья')
		# Когда она нажимает энтер страница обновляется, и теперь страница
		# содержит "1: Купить павлиньи перья" в качестве элемента списка
		inputbox.send_keys(Keys.ENTER)
		time.sleep()

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue(
			any(row.text == '1: Купить павлиные крылья' for row in rows)
		)
		self.fail('Finish the test!')


if __name__ == '__main__':
	unittest.main(warnings='ignore')
