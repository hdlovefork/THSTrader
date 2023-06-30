import json


class Storage:
    def __init__(self,filename='cache.json'):
        # 读取Toml文件
        self.filename = filename
        self.cache = self.load_cache()

    def load_cache(self):
        try:
            with open(self.filename, 'r') as f:
                cache_data = json.load(f)
            return cache_data
        except FileNotFoundError:
            return {}

    def save_cache(self):
        with open(self.filename, 'w') as f:
            json.dump(self.cache, f, ensure_ascii=False)

    def __call__(self, *args, **kwargs):
        return self.cache

    def has(self, key):
        return key in self.cache

    def get(self, key, default=None):
        return self.cache.get(key, default)

    def set(self, key, value):
        self.cache[key] = value
        self.save_cache()

    def remove(self, key):
        if key in self.cache:
            del self.cache[key]
            self.save_cache()

    def clear(self):
        self.cache = {}
        self.save_cache()
