import os

import toml
from pytdx.hq import TdxHq_API

from THS.AvailableIPPool import AvailableIPPool
from THS.TdxHqPool_API import TdxHqPool_API


def load_ips(path):
    # 判断bin/ips.toml文件是否存在，不存在则抛出文件不存在异常
    if not os.path.exists(path):
        raise FileNotFoundError(f'{path}文件不存在，请先执行check命令')
    # 读取bin/ips.toml文件
    with open(path, 'r') as f:
        config = toml.load(f)
    # 判断config中是否存在ips键，不存在则抛出配置错误异常
    if 'ips' not in config:
        raise ValueError('配置错误，缺少ips配置')
    # 返回ips配置
    return tuple((str(v[0]), int(v[1])) for v in config['ips'])


class THSQuotation:
    def __init__(self,path):
        self.api = None
        ips = load_ips(path)
        # IP 池对象
        pool = AvailableIPPool(TdxHq_API, ips)
        # 选出M, H
        # 生成api对象，第一个参数为TdxHq_API后者 TdxExHq_API里的一个，第二个参数为ip池对象。
        self.api = TdxHqPool_API(TdxHq_API, pool)

        # connect 函数的参数为M, H 两组 (ip, port) 元组
        self.api.connect()

    def close(self):
        if self.api and hasattr(self.api, 'close'):
            self.api.close()

    def __enter__(self):
        return self

    def __delete__(self, instance):
        if self.api and hasattr(self.api, 'close'):
            self.api.close()

    def __del__(self):
        if self.api and hasattr(self.api, 'close'):
            self.api.close()

    def __getattr__(self, item):
        if self.api and hasattr(self.api, item):
            return getattr(self.api, item)
        return None