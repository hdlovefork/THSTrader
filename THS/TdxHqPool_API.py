import time

from pytdx.pool.hqpool import TdxHqPool_API as BaseTdxHqPool_API, TdxHqApiCallMaxRetryTimesReachedException
from pytdx.log import DEBUG, log


class TdxHqPool_API(BaseTdxHqPool_API):
    def __init__(self,hq_cls, ippool, max_retry_times=3):
        super(TdxHqPool_API, self).__init__(hq_cls, ippool)
        self.api_call_max_retry_times = max_retry_times

    def connect(self):
        log.debug("setup ip pool")
        self.ippool.setup()
        log.debug("connecting to primary api")
        ipandport = self.ippool.get_next_ip()
        self.api.connect(*ipandport)
        log.debug("connecting to hot backup api")
        hot_failover_ipandport = self.ippool.get_next_ip()
        self.hot_failover_api.connect(*hot_failover_ipandport)
        return self

    def do_hq_api_call(self, method_name, *args, **kwargs):
        """
        代理发送请求到实际的客户端
        :param method_name: 调用的方法名称
        :param args: 参数
        :param kwargs: kv参数
        :return: 调用结果
        """
        try:
            result = getattr(self.api, method_name)(*args, **kwargs)
            if result is None:
                log.info("api(%s) call return None" % (method_name,))
        except Exception as e:
            log.info("api(%s) call failed, Exception is %s" % (method_name, str(e)))
            result = None

        # 如果无法获取信息，则进行重试
        if result is None:
            if self.api_call_retry_times > self.api_call_max_retry_times:
                log.info("(method_name=%s) max retry times(%d) reached" % (method_name, self.api_call_max_retry_times))
                raise TdxHqApiCallMaxRetryTimesReachedException("(method_name=%s) max retry times reached" % method_name)
            old_api_ip = self.api.ip
            new_api_ip = None
            if self.hot_failover_api:
                new_api_ip = self.hot_failover_api.ip
                log.info("api call from init client (ip=%s) err, perform rotate to (ip =%s)..." %(old_api_ip, new_api_ip))
                self.api.disconnect()
                self.api = self.hot_failover_api
            log.info("retry times is " + str(self.api_call_max_retry_times))
            choise_ip = self.ippool.get_next_ip()
            if choise_ip:
                self.hot_failover_api = self.hq_cls(multithread=True, heartbeat=True)
                self.hot_failover_api.connect(*choise_ip)
            else:
                self.hot_failover_api = None
            # 阻塞0.2秒，然后递归调用自己
            time.sleep(self.api_retry_interval)
            self.api_call_retry_times += 1
            result = self.do_hq_api_call(method_name, *args, **kwargs)
        else:
            self.api_call_retry_times = 0

        return result
