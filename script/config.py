import yaml


class Config(object):
    def __init__(self, file_path='config.yaml'):
        with open(file_path, 'r') as file:
            # 使用 yaml.load 方法将文件内容转换为 Python 对象
            self.config = yaml.load(file, Loader=yaml.FullLoader)

    def __getattr__(self, item):
        return self.config[item]
