from create_bot import logger
from create_bot import cache

def send_info(request_text, get_info_func, ClassName):
    if cache.is_cached(request_text):
        logger.info(f'{request_text} in cache')
    else:
        logger.info(f'{request_text} load from fantlab')
        cache.save(request_text,get_info_func(request_text,parse_json=0)[0])

    json_ = cache.load(request_text)
    return ClassName(**json_)