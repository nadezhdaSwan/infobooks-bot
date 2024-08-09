import unittest
from pprint import pprint
from pickle import dump, load

from bibliosites import fantlab
from db.author_class import Author 
from db.work_class import Work
from db.edition_class import Edition

class DowloadAuthorInfo(unittest.TestCase):
	"""тестирование загрузки информации об авторе"""
	@unittest.skip('Не загружать лишний раз сервер fantlab')
	def test_dowload_json(self):
		'''тест функций загрузки информации об авторах'''
		self.assertTrue(len(fantlab.get_authors_id('Абрамов')) >= 3)
		self.assertEqual(fantlab.get_info_about_author_from_id(1)['name'],'Дэн Симмонс')
		self.assertEqual(fantlab.get_info_about_author_from_name('Станислав Лем')[0]['name'],
			'Станислав Лем')

	def test_recognise_author_json(self):
		'''тест загрузки json в класс данных Author'''
		try:
			with open('tests/author_json.dat','rb') as file:
				author_json = load(file)
		except FileNotFoundError or EOFError:
			author_json = fantlab.get_info_about_author_from_name('Станислав Лем')[0]
			with open('tests/author_json.dat','wb') as file:
				dump(author_json,file)
		author = Author(**author_json)
		print(author)
		self.assertEqual(author.name, 'Станислав Лем')

class DowloadWorkInfo(unittest.TestCase):
	'''тестирование загрузки информации о произведении'''
	@unittest.skip('Не загружать лишний раз сервер fantlab')
	def test_dowload_json(self):
		'''тест функций загрузки информации о произведении'''
		self.assertEqual(fantlab.get_work_id('Властелин колец')[0], 1693)
		self.assertEqual(fantlab.get_info_from_work_id(1693)['work_name'], 'Властелин Колец')
		self.assertEqual(fantlab.get_info_about_work_from_name('Властелин колец')[0]['work_name'], 
			'Властелин Колец')

	def test_recognise_author_json(self):
		'''тест загрузки json в класс данных Work'''
		try:
			with open('tests/work_json.dat','rb') as file:
				work_json = load(file)
		except FileNotFoundError or EOFError:
			work_json = fantlab.get_info_about_work_from_name('Солярис')[0]
			with open('tests/work_json.dat','wb') as file:
				dump(work_json,file)		
		work = Work(**work_json)
		print(work)
		self.assertEqual(work.work_name, 'Солярис')

class DowloadEditionInfo(unittest.TestCase):
	'''тестирование загрузки информации о издании'''
	@unittest.skip('Не загружать лишний раз сервер fantlab')
	def test_dowload_json(self):
		'''тест функций загрузки информации о произведении'''
		self.assertEqual(fantlab.get_edition_id('978-5-699-39937-6')[0], 42271)
		self.assertEqual(fantlab.get_info_from_edition_id(42271)['edition_name'], 'Имя ветра')
		self.assertEqual(fantlab.get_info_about_edition_from_isnb('978-5-699-39937-6')[0]['edition_name'],
			'Имя ветра')

	def test_recognise_edition_json(self):
		try:
			with open('tests/edition_json.dat','rb') as file:
				edition_json = load(file)
		except FileNotFoundError or EOFError:
			edition_json = fantlab.get_info_about_edition_from_isnb('978-5-699-39937-6')[0]
			with open('tests/edition_json.dat','wb') as file:
				dump(edition_json,file)		
		edition = Edition(**edition_json)
		print(edition)
		self.assertEqual(edition.edition_name, 'Имя ветра')


if __name__ == '__main__':
	unittest.main(warnings='ignore')

