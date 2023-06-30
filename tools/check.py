import os
import sys
from collections import OrderedDict
import toml

import click
from pytdx.config.hosts import hq_hosts
from pytdx.hq import TdxHq_API
from pytdx.pool.ippool import AvailableIPPool

if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))


@click.command()
@click.option('--num', default=5, type=click.INT, help='number of ip')
@click.option('--out', default='ips.toml', help='out ips file')
def main(num, out):
    if num < 2:
        click.echo("num must be greater than 1")
        return
    click.echo("get all available ips,please wait...")
    ips = [(v[1], v[2]) for v in hq_hosts]
    available_ips = OrderedDict()
    i = 0
    while i < len(ips):
        click.echo(f"The {i + 1}/{len(ips)} IP address is being tested.")
        # 从hq_hosts中取出1个ip
        ip = ips[i:i + 1]
        # 获取所有可用的连接ip
        ip_pool = AvailableIPPool(TdxHq_API, ip)
        available_ips.update(ip_pool.get_all_available_ips())
        # 已经采集到需要的ip个数则退出
        if len(available_ips) >= num:
            break
        i += 1
    # 将available_ips写入文件中，使用toml格式
    ips = ((v[0],str(v[1])) for v in available_ips.values())
    with open(out, 'w') as f:
        f.write(toml.dumps({'ips': ips}))


if __name__ == '__main__':
    main()
