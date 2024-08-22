import requests
import json
from pprint import pprint

link = 'https://api.fantlab.ru'


def get_info_about_edition_from_isnb(isnb, parse_json = 1):
	editions_id = get_edition_id(isnb)
	return [get_info_from_edition_id(edition_id, parse_json) for edition_id in editions_id]

def get_info_from_edition_id(edition_id, parse_json = 1):
	return get_info_from_fantlab(f'edition/{edition_id}', parse_json)	

def get_edition_id(isnb):
	query = isnb
	editions_id = [edition_id['edition_id'] for edition_id in 
		get_info_from_fantlab(f'search-editions?q={query}&page=1&onlymatches=1')]
	return sorted(editions_id)

def get_info_about_work_from_name(work_name, parse_json = 1):
	works_id = get_work_id(work_name)
	return [get_info_from_work_id(work_id, parse_json) for work_id in works_id]

def get_info_from_work_id(work_id, parse_json = 1):
	return get_info_from_fantlab(f'work/{work_id}', parse_json)

def get_work_id(work_name):
	query = work_name
	works_id = [work['work_id'] for work in
		get_info_from_fantlab(f'search-works?q={query}&page=1&onlymatches=1')]
	return sorted(works_id)


def get_info_about_author_from_name(author_name, parse_json = 1):
	authors_id = get_authors_id(author_name)
	return [get_info_about_author_from_id(author_id, parse_json) for author_id in authors_id]

def get_info_about_author_from_id(author_id, parse_json = 1):
	return get_info_from_fantlab(f'autor/{author_id}', parse_json)

def get_authors_id(author_name):
	query = author_name
	#print(f'search-autors?q={query}')
	authors_id = [author['autor_id'] for author in 
		get_info_from_fantlab(f'search-autors?q={query}&page=1&onlymatches=1')]
	return sorted(authors_id)

def get_info_from_fantlab(request_text,parse_json = 1):
	# Making a GET request 
	#print(f'{link}/{request_text}')
	responce = requests.get(f'{link}/{request_text}') 
	#print(responce)
	#print(responce.content.decode('utf-8'))
	# check status code for response received 
	# success code - 200 
	if responce.status_code == 200:
	# return content of request 
		if parse_json==1:
			return json.loads(responce.content.decode('utf-8'))
		else:
			return responce.content.decode('utf-8')
	else:
		return -1

if __name__=='__main__':
	#assert get_info_from_fantlab('autor') == -1
	#assert json.loads(get_info_from_fantlab('autor/1'))['name'] == 'Дэн Симмонс'
	#pprint(get_authors_id('Абрамов'))
	#pprint(get_info_about_author_from_id(1))
	#pprint(get_info_about_author_from_name('Станислав Лем'))
	#pprint(get_work_id('Властелин колец'))
	#pprint(get_info_from_work_id(1693))
	#pprint(get_info_about_work_from_name('Имя ветра'))
	#pprint(get_edition_id('978-5-699-39937-6'))
	#pprint(get_info_from_edition_id(42271))
	pprint(get_info_about_edition_from_isnb('978-5-699-39937-6'))


