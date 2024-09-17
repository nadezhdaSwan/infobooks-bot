import unittest
from pprint import pprint

from bibliosites import fantlab
from db.author_class import Author 
from db.work_class import Work
from db.edition_class import Edition

import redis
import json

from create_bot import cache

class DowloadAuthorInfo(unittest.TestCase):
	"""тестирование загрузки информации об авторе"""
	@unittest.skip('Не загружать лишний раз сервер fantlab')
	def test_dowload_json(self):
		'''тест функций загрузки информации об авторах'''
		self.assertTrue(len(fantlab.get_authors_id('Абрамов')) >= 3)
		self.assertEqual(fantlab.get_info_about_author_from_id(1)['name'],'Дэн Симмонс')
		self.assertEqual(fantlab.get_info_about_author_from_name('Станислав Лем')[0]['name'],
			'Станислав Лем')

	@unittest.skip('Проверяется в test_cache')
	def test_recognise_json(self):
		'''тест загрузки json в класс данных Author'''
		try:
			with open('tests/author.json','r') as file:
				author_json = file.read()
				author_turple = json.loads(author_json)
		except:
			author_json = fantlab.get_info_about_author_from_name('Станислав Лем',parse_json=0)[0]
			with open('tests/author.json','w') as file:
				file.write(author_json)
			author_turple = json.loads(author_json)
		author = Author(**author_turple)
		#print(author)
		self.assertEqual(author.name, 'Станислав Лем')

	@unittest.skip('Проверяется в test_cache')
	def test_save_json_to_redis(self):
		'''тест загрузки autor_json в redis'''
		with open('tests/author.json','r') as file:
			author_json = file.read()
		r = redis.Redis(host='localhost', port=6379, db=0)
		r.set('author',author_json,ex=120)
		self.assertEqual(r.get('author').decode('utf-8'),	author_json)

	def test_cache(self):
		'''тест кэша в redis'''
		request_text = 'Станислав Лем'
		cache.save(request_text, Author.import_from_fantlab(Author, request_text)[0], ex=100)
		author = Author(**cache.load(request_text))
		#print(author)
		self.assertEqual(author.name, request_text)
		self.assertTrue(cache.is_cached(request_text)>=1)

	def test_detailed_info(self):
		'''тест кэша в redis'''
		request_text = 'Станислав Лем'
		cache.save(request_text, Author.import_from_fantlab(Author, request_text)[0], ex=100)
		author = Author(**cache.load(request_text))
		print(author.detailed_info())
		#self.assertEqual(author.name, request_text)
		#self.assertTrue(cache.is_cached(request_text)>=1)

	@unittest.skip('Перенесено в функцию author_pagination')
	def test_pagination(self):
		'''тестируем пагинацию списка авторов'''
		request_text = 'Иванов'
		text = ''
		for num, i in enumerate(fantlab.get_info_about_author_from_name(request_text, parse_json=0),1):
			name = json.loads(i)['name']
			cache.save(name,i)
			author = Author(**cache.load(name))
			text += f'{num}. {author}'
		print(text)

			#print(Author(**i))





class DowloadWorkInfo(unittest.TestCase):
	'''тестирование загрузки информации о произведении'''
	@unittest.skip('Не загружать лишний раз сервер fantlab')
	def test_dowload_json(self):
		'''тест функций загрузки информации о произведении'''
		self.assertEqual(fantlab.get_work_id('Властелин колец')[0], 1693)
		self.assertEqual(fantlab.get_info_from_work_id(1693)['work_name'], 'Властелин Колец')
		self.assertEqual(fantlab.get_info_about_work_from_name('Властелин колец')[0]['work_name'], 
			'Властелин Колец')

	@unittest.skip('Проверяется в test_cache')
	def test_recognise_json(self):
		'''тест загрузки json в класс данных Work'''
		try:
			with open('tests/work.json','r') as file:
				work_json = file.read()
				work_turple = json.loads(work_json)
		except:
			work_json = fantlab.get_info_about_work_from_name('Солярис',parse_json=0)[0]
			with open('tests/work.json','w') as file:
				file.write(work_json)
			work_turple = json.loads(work_json)
		work = Work(**work_turple)
		#print(work)
		self.assertEqual(work.work_name, 'Солярис')

	@unittest.skip('Проверяется в test_cache')
	def test_save_json_to_redis(self):
		'''тест загрузки work_json в redis'''
		with open('tests/work.json','r') as file:
			work_json = file.read()
		r = redis.Redis(host='localhost', port=6379, db=0)
		r.set('work',work_json,ex=120)
		self.assertEqual(r.get('work').decode('utf-8'),	work_json)

	def test_cache(self):
		'''тест кэша в redis'''
		request_text = 'Солярис'
		cache.save(request_text, Work.import_from_fantlab(Work, request_text)[0], ex=100)
		work = Work(**cache.load(request_text))
		#print(work)
		self.assertEqual(work.work_name, request_text)
		self.assertTrue(cache.is_cached(request_text)>=1)


	def test_detailed_info(self):
		'''тест кэша в redis'''
		request_text = 'Солярис'
		cache.save(request_text, Work.import_from_fantlab(Work, request_text)[0], ex=100)
		work = Work(**cache.load(request_text))
		print(work.detailed_info())


class DowloadEditionInfo(unittest.TestCase):
	'''тестирование загрузки информации о издании'''
	@unittest.skip('Не загружать лишний раз сервер fantlab')
	def test_dowload_json(self):
		'''тест функций загрузки информации о произведении'''
		self.assertEqual(fantlab.get_edition_id('978-5-699-39937-6')[0], 42271)
		self.assertEqual(fantlab.get_info_from_edition_id(42271)['edition_name'], 'Имя ветра')
		self.assertEqual(fantlab.get_info_about_edition_from_isnb('978-5-699-39937-6')[0]['edition_name'],
			'Имя ветра')

	@unittest.skip('Проверяется в test_cache')
	def test_recognise_edition_json(self):
		'''тест загрузки json в класс данных Edition'''
		try:
			with open('tests/edition.json','r') as file:
				edition_json = file.read()
				edition_turple = json.loads(edition_json)
		except:
			edition_json = fantlab.get_info_about_edition_from_isnb('978-5-699-39937-6',parse_json=0)[0]
			with open('tests/edition.json','w') as file:
				file.write(edition_json)
			edition_turple = json.loads(edition_json)
		edition = Edition(**edition_turple)
		#print(edition)
		self.assertEqual(edition.edition_name, 'Имя ветра')

	@unittest.skip('Проверяется в test_cache')
	def test_save_json_to_redis(self):
		'''тест загрузки edition_json в redis'''
		with open('tests/edition.json','r') as file:
			edition_json = file.read()
		r = redis.Redis(host='localhost', port=6379, db=0)
		r.set('edition',edition_json,ex=120)
		self.assertEqual(r.get('edition').decode('utf-8'),	edition_json)

	def test_cache(self):
		'''тест кэша в redis'''
		request_text = '978-5-699-39937-6'
		cache.save(request_text, Edition.import_from_fantlab(Edition, request_text)[0], ex=100)
		edition = Edition(**cache.load(request_text))
		#print(author)
		self.assertEqual(edition.isbns[0], request_text)
		self.assertTrue(cache.is_cached(request_text)>=1)

	def test_detailed_info(self):
		'''тест кэша в redis'''
		request_text = '978-5-699-39937-6'
		cache.save(request_text, Edition.import_from_fantlab(Edition, request_text)[0], ex=100)
		edition = Edition(**cache.load(request_text))
		print(edition.detailed_info())


if __name__ == '__main__':
	unittest.main(warnings='ignore')

