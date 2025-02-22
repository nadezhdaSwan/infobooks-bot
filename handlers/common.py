from create_bot import logger
from create_bot import cache
import json


def cache_request_list(request_text, ClassName):
    request_text_list_name = f'{request_text}_request_{ClassName.name_in_json}'
    if cache.is_cached(request_text_list_name):
        logger.info(f'{request_text_list_name} in cache')
    else:
        logger.info(f'{request_text_list_name} load from fantlab')
        cache.save_list(request_text_list_name, ClassName.import_from_fantlab(ClassName, request_text, parse_json=0), ClassName.name_in_json)
    return cache.load_list(request_text_list_name)


def cache_request(request_text, ClassName):
    if cache.is_cached(request_text):
        logger.info(f'{request_text} in cache')
        return cache.load(request_text)
    else:
        logger.info(f'no {request_text} in cache')
    

def send_info(request_text, get_info_func, ClassName):
    if cache.is_cached(request_text):
        logger.info(f'{request_text} in cache')
    else:
        logger.info(f'{request_text} load from fantlab')
        cache.save(request_text,get_info_func(request_text,parse_json=0)[0])

    json_ = cache.load(request_text)
    return ClassName(**json_)

def pagination(request_text, ClassName):
    '''пагинация списков'''
    book_list: dict[int, str] = {}

    json_list = cache_request_list(request_text, ClassName)
    for num, name in enumerate(json_list,1):
        book_list[num] = f'{num}. {ClassName(**cache_request(name, ClassName))}'
    return book_list

def send_detailed_info(request_text, ClassName, num_list):
    json_ = list(cache_request_list(request_text, ClassName))[num_list-1]
    return f'{ClassName(**cache_request(json_, ClassName)).detailed_info()}'

