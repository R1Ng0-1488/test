from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
	"""new visitor's test"""

	def setUp(self):
		"""installation"""
		self.browser = webdriver.Firefox()

	def tearDown(self):
		"""demontaj"""
		# close browser
		self.browser.quit()

	def wait_for_row_in_list_table(self, row_text):
		"""ожидать строку в таблице списка"""
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def test_can_start_a_list_for_one_user(self):
		'''test: can start a list for one user'''
		# Эдит слышала про крутое новое онлайн-приложение со
		# списком неотложных дел. Она решает оценить его
		# домашнюю страницу
		self.browser.get(self.live_server_url)

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
		# time.sleep(1)
		self.wait_for_row_in_list_table('1: Купить павлиные крылья')

		# table = self.browser.find_element_by_id('id_list_table')
		# rows = table.find_elements_by_tag_name('tr')
		# # self.assertTrue(
		# # 	any(row.text == '1: Купить павлиные крылья' for row in rows),
		# # 	f"New element of list didn't appeare in table. There was\n{table.text}"
		# # )
		# self.assertIn('1: Купить павлиные крылья', [row.text for row in rows])

		#ТЕстовое поле по-прежднему приглашает ее добавить еще один элемент. Она
		# вводит "Сделать мушку из павлиньих перьев" (Эдит очень методична)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Сделать мушку из павлиньих перьев')
		inputbox.send_keys(Keys.ENTER)
		# time.sleep(1)
		self.wait_for_row_in_list_table('1: Купить павлиные крылья')
		self.wait_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')
		# Страница снова обновляется и теперь показывает оба элемента ее списка
		# table = self.browser.find_element_by_id('id_list_table')
		# rows = table.find_elements_by_tag_name('tr')
		# self.assertIn('1: Купить павлиньи крылья', [row.text for row in rows])
		# self.assertIn(
		# 	'2: Сделать мушку из павлиньих перьев',
		# 	[row.text for row in rows]
		# )
		# Эдит интересно, зпомнит ли сайт ее список. Дфлее она видит, что
		# сайт сгенерировал для нее уникальный УРЛ-адресс - по этому поводу
		# выводится небольшой текст с объвлениеями.

		# Она посещает этот УРЛ-адрес - ее список по-моему там.

		#Удовлетворенная, она снова ложиться спать

	def test_multiple_users_can_start_lists_at_different_urls(self):
		'''test: multiple users can start lists at different urls'''
		# Edit starts a new list
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Купить павлиные перья')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Купить павлиные перья')

		# She knows that her list has a unique url-address
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')

		# Now new user Frensis comes to the site

		# We use a new seanse of browser so that we provide that information from Edit won't go through the cookie and ets.
		self.browser.quit()
		self.browser = webdriver.Firefox()

		# Frensis visits home page. There is no an Edit's list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Купить павлиные перья', page_text)
		self.assertNotIn('Сделать мушку', page_text)

		# Frensis starts a new list, entering a new element. Its less interesting, then an Edit's lists
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		# Frensis gets a unique url-address
		frensis_list_url = self.browser.current_url
		self.assertRegex(frensis_list_url, '/lists/.+')
		self.assertNotEqual(frensis_list_url, edith_list_url)

		# again. There is no an Edith's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Купить павлиные перья', page_text)
		self.assertIn('Buy milk', page_text)

		# Both of them are satisfied and they go to sleep
		self.fail('Finish the test!')
