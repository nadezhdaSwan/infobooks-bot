from dataclasses import dataclass
from datetime import date, datetime
from typing import TypedDict, Tuple, Optional

from bibliosites.fantlab import get_info_about_edition_from_isnb

@dataclass(kw_only=True)
class Edition:
	edition_id: int						# id издания
	edition_name: str					# название издания
	edition_type: str					# тип издания
	edition_type_plus: Tuple[str]		# доп. типы издания
	edition_work_id: int|None    		# id произведения, где содержание такое же как в издании (журнал/сборник/антология)
	copies: int = 0						# тираж (0, если неизвестен)
	correct_level: float				# степень проверенности издания (0 - не проверено, 0.5 - не полностью проверено, 1 - проверено)
	cover_type: str						# тип обложки
	creators: TypedDict('creators', {
		'authors': Tuple[				# список авторов
			TypedDict('author', {
				'id': int,					# id автора
				'is_opened': bool,			# открыта ли страница автора
				'name': str,				# имя автора
				'type': str					# тип (autor - автор, art - художник)
			}), ...
		],
		'compilers': Tuple[				# список составителей (если сборник/антология)
			TypedDict('compiler', {
				'id': int,					# id составителя
				'name': str,				# имя составителя (может быть "не указан")
				'type': str					# тип (compiler)
			}), ...
		] | None,
		'publishers': Tuple[			# список издателей
			TypedDict('publisher', {
				'id': int,					# id издателя
				'name': str,				# название издателя
				'type': str					# тип (publisher)
			}), ...
		]
	})
	description: str					# описание
	format: str							# формат издания ("0", если неизвестен)
	format_mm: str						# формат издания (в мм.)
	image: str							# основная обложка издания
	image_preview: str					# превью основной обложки
	isbns: Tuple[str]					# список ISBN
	lang: str							# язык издания
	lang_code: str						# код языка издания
	notes: str							# примечания
	pages: int							# количество страниц
	plan_date: str						# план выхода (дата текстом). если поле не пустое - значит издание еще не вышло
	plan_description: str				# примечание к плану выхода издания
	preread: bool						# есть ли отрывок для чтения
	series: Tuple[						# серии, в которые входит издание
		TypedDict('series', {
			'id': int,						# id серии
			'is_opened': bool,				# открыта ли серия
			'name': str,					# название серии
			'type': str						# тип (series)
		})
	]
	year: int							# год издания
	content: Tuple[str]	| None				# [content] содержание
	images_plus: None
	last_modified: datetime
	type: int
	volume: None

	name_in_json = 'edition_name'

	def __str__(self):
		return f'''{self.edition_name}
ISNB {', '.join(self.isbns)}
Год издания {self.year}
'''

	def import_from_fantlab(self,request_text, parse_json=0):
		return get_info_about_edition_from_isnb(request_text, parse_json)