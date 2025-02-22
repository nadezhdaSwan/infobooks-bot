from dataclasses import dataclass
from datetime import date, datetime
from typing import TypedDict, Tuple, Optional, NotRequired

from bibliosites.fantlab import get_info_about_author_from_name

@dataclass(kw_only=True)
class Author:
    type: str                        # тип сегмента (в данном случае всегда autor)
    id: int                          # id автора
    autor_id: int                    # id автора (дубль, название переменной с типом)
    url: str                         # ссылка на страницу автора
    last_modified: datetime              # дата последнего редактирования
    last_modified_iso: Optional[date]          # дата последнего редактирования в ISO 8601
    is_opened: bool                  # открыта ли страница автора
    anons: str                       # краткий анонс биографии
    birthday: date                   # дата рождения
    country_id: int                  # id страны
    country_name: str                # название страны
    deathday: date                   # дата смерти
    fantastic: int                   # ?
    image: str                       # ссылка на основное фото автора
    image_preview: str               # ссылка на превью основного фото автора
    name: str                        # имя на русском языке
    name_orig: str                   # имя в оригинале
    name_pseudonyms: Tuple[          # список псевдонимов
        TypedDict('pseudonym', {        
        'is_real': int, 
        'name': str, 
        'name_orig': str
    }), ...
    ]
    name_rp: str                     # имя на русском языке в родительном падеже
    name_short: str                  # имя на русском языке для перечислений (сначала фамилия, затем имя)
    sex: str                         # пол ("m" - мужской, "f" - женский)
    stat: TypedDict('stat', {        # статистика
        'awardcount': NotRequired[int],              # [any] количество наград
        'editioncount': int,            # количество изданий
        'markcount': int,               # количество поставленных автору оценок
        'moviecount': int,              # количество фильмов (экранизаций и т.д.)
        'responsecount': int,           # количество написанных на произведения автора отзывов
        'workcount': NotRequired[int]   # [any] количество произведений
    })
#    sites: Optional[Tuple[
#        TypedDict('site', {          # [any] сайты автора
#            'descr': str,               # описание ссылки
#            'site': str                 # ссылка
#        })
#    ]] = Tuple[{}]
    
    name_in_json = 'autor'


    def __str__(self):
        return f'''{self.name}
{self.name_orig}
Родился: {self.birthday}
Умер: {self.deathday}
Страна: {self.country_name}

'''
    def detailed_info(self):
        return f'''{self.name} ({self.name_orig})
Родился: {self.birthday}
Умер: {self.deathday}
Страна: {self.country_name}
url: {self.url[6:]}
'''
    
    def import_from_fantlab(self,request_text, parse_json=0):
        return get_info_about_author_from_name(request_text, parse_json)
