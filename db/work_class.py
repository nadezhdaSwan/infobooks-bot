from dataclasses import dataclass
from datetime import date, datetime
from typing import TypedDict, Tuple, Optional, Dict

from redis_om import HashModel

@dataclass(kw_only=True)
class Work:
    work_id: int                        # id произведения
    last_modified: datetime                 # время последнего изменения данных
    last_modified_iso: date | None            # время последнего изменения данных в ISO 8601
    work_name: str                      # название произведения
    work_name_orig: str                 # оригинальное название (анг или родной)
    work_name_alts: Tuple[str]          # массив альтернативных названий произведения
    work_name_bonus: str                # дополнение к названию
    authors: Tuple[
        TypedDict('author', {
            'id': int,                      # id типа персоны ( по формату /{type}/{id} однозначно укажет на нужную персону )
            'is_opened': int,                # открыта ли страница автора (1 - да, 0 - нет)
            'name': str,                    # имя фамилия
            'name_orig': str,               # имя фамилия (анг или родной)
            'type': str,                    # тип персоны (autor, art)
        })
    ]
    work_year: int                      # год публикации произведения
    work_year_of_write: int             # год написания произведения (если указан)
    work_description: str               # аннотация
    work_description_author: str        # автор анотации (может содержать bb-тэги)
    work_notes: str                     # примечание
    lang: str                           # язык написания
    lang_code: str                      # код языка написания
    title: str                          # автор(ы)+название в формате "Дэн Симмонс «Гиперион»"
    image: str                          # ссылка на картинку произведения (обложку по умолчанию)
    image_preview: str                  # ссылка на превью картинки произведения
    publish_statuses: Tuple[str] | Tuple[()]       # для неопубликованных о статусе проивзедения ("не закончено", "в планах", ...)
    work_published: int                 # вышло ли произведени (0 - не опубликовано, 1 - опубликовано)
    work_preparing: int                 # запланированное произведени (1 - "в планах автора")
    work_notfinished: int               # не законченое произведение (1 - "не окончено")
    work_lp: int | None                       # доступен линговоанаолиз произведения (0 - "нет" / 1 - "есть")
    public_download_file: int           # есть файл для скачивания/чтения (1 - "доступно для свободного чтения")
    rating: TypedDict('rating', {
        'rating': float,                    # рейтинг (до сотых, пр.: "8.91")
        'voters': int                       # кол-во оценок
    })
    val_midmark: float                  # рейтинг (дубль)
    val_midmark_by_weight: float        # рейтинг (дубль)
    val_voters: int                     # кол-во оценок (дубль)
    val_responsecount: int              # кол-во отзывов на произведение
    work_type_id: int                   # id типа произведения 
    work_type: str                      # тип провездения (роман, повесть, рассказ & etc)
    work_type_name: str                 # тип произведения на английском
    work_parent: int | None                  # >0 для неактивных частей - если является частью другого произведение, то тут его id
    work_root_saga: Tuple[              # название циклов, куда водит данное произвдеение
        TypedDict('saga', {
            'work_id': int,                   # id цикла (ворка)
            'work_name': str,                 # название 
            'work_type': str,                 # тип произведения на русском
            'work_type_id': int,              # id типа произведния
            'work_year': int                  # год публикации
        })
    ] | None
    work_saga: Tuple[str] | None
    work_type_icon: str


    def __str__(self):
        return f'''
{self.work_name}
{self.work_name_orig}
{self.work_type}, {self.work_year} год
'''