from create_bot import logger
from create_bot import cache
import json


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
    text = ''
    for num, i in enumerate(ClassName.import_from_fantlab(ClassName, request_text),1):
        name = json.loads(i)[ClassName.name_in_json]
        cache.save(name, i)
        element = ClassName(**cache.load(name))
        text += f'{num}. {element}'
    return text