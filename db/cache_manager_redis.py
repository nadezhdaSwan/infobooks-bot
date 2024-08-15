import redis
import json

class CacheManager:
	def __init__(self, host='localhost', port=6379, db=0):
		self.redis_db = redis.Redis(host, port, db)

	def is_cached(self, id: str):
		return self.redis_db.exists(id)

	def save(self, id: str, content_json, ex: int = None):
		self.redis_db.set(id, content_json, ex)
#		file_name = self.get_path(id)
#		with open(file_name, 'wb') as file:
#			print('Save to cache: "%s"' % file_name)
#			file.write(content)

	def load(self, id: str, parse_json=1):
		content_json = self.redis_db.get(id).decode('utf-8')
		if parse_json:
			return json.loads(content_json)
		else:
			return content_json			

#		try:
#			with open(file_name, 'r', encoding="utf-8") as file:
#				return file.read()
#		except Exception as ex:
#			print('load_book_content_from_cache("%s"): %s' % (file_name, ex))
#			return None


if __name__=='__main__':
	cache = CacheManager()



